import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

from startup.file_conversion import from_csv_to_json, save_setup, save_yaml
from startup.prompts import (
    ask_animal,
    ask_batch,
    ask_experimenter,
    ask_last_training_level,
    ask_starting_training_level,
    ask_time_parameters,
    verify_session,
)
from startup.utils import YamlFile


def main():
    """
    This startup script is run before Bonsai is opened in order to make some pre-session configurations.
    """
    # Load config.yml
    with open("../src/config/config.yml", "r") as file:
        config = yaml.safe_load(file)

    # Convert the setup.csv and training.csv into JSON files so that Bonsai is able to read them
    from_csv_to_json(Path(config["paths"]["training"]), type="training")

    # Ask user for some informations from prompts
    experimenter = ask_experimenter()
    batch = ask_batch()
    animal = ask_animal()

    # Change animal file path according to the previous inputs
    config["paths"]["animal"] = (
        config["paths"]["animal_dir"] + "/" + batch + "/" + animal + ".yml"
    )

    # Choose which animal file to open according to whether the animal-specific file already exists or not
    if os.path.isfile(config["paths"]["animal"]):
        animal_file = Path() / config["paths"]["animal"]
    else:
        animal_file = Path() / config["paths"]["animal_dir"] / "template.yml"

    # Load the animal.yml config file
    with open(animal_file, "r") as file:
        animal_config = yaml.safe_load(file)

    animal_out_dir = Path() / config["paths"]["output"] / batch / animal
    last_dir = get_last_dir(animal_out_dir)
    animal_out_backup = Path() / config["paths"]["output_backup"] / batch / animal
    last_backup_dir = get_last_dir(animal_out_backup)

    if datetime.strptime(str(last_dir), "%y%m%d") >= datetime.strptime(
        str(last_backup_dir), "%y%m%d"
    ):
        out_name = (
            animal_out_dir / last_dir / ("out_" + animal + "_" + str(last_dir) + ".csv")
        )
    else:
        out_name = (
            animal_out_backup
            / last_backup_dir
            / ("out_" + animal + "_" + str(last_backup_dir) + ".csv")
        )

    # Try to read the last out.csv file and return from function if something goes wrong
    try:
        df = pd.read_csv(out_name)  # Ask for user input to update animal.yml file
        verify_session(animal_config, df, str(last_dir))
        ask_time_parameters(animal_config, df)
        animal_config["session"]["starting_trial_number"] = int(
            df.loc[df.index[-1], "trial"] + 1
        )
    except Exception:
        animal_config["session"]["block_number"] = 1

    # Update animal, batch, experimenter and block_number
    animal_config["animal_id"] = animal
    animal_config["batch"] = batch
    animal_config["session"]["experimenter"] = experimenter
    starting_level = ask_starting_training_level()
    if starting_level != -1:
        animal_config["session"]["starting_training_level"] = starting_level
    animal_config["session"]["last_training_level"] = ask_last_training_level(
        Path(config["paths"]["training"])
    )

    # Save animal and config files
    os.makedirs(config["paths"]["animal_dir"] + "/" + batch, exist_ok=True)
    save_yaml(animal_config, config["paths"]["animal"], type=YamlFile.ANIMAL)
    save_yaml(config, "../src/config/config.yml", type=YamlFile.CONFIG)
    save_setup(config["paths"]["setup"], config["setup"])


def get_last_dir(path: Path) -> str:
    if path.is_dir():
        dirs = [entry.name for entry in path.iterdir() if (path / entry).is_dir()]

    if not path.is_dir() or dirs == []:
        return "200101"
    return dirs[-1]
