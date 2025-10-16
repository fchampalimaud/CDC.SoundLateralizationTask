import os
from datetime import datetime

import pandas as pd
import yaml

from startup.config_to_json import converter, save_setup
from startup.startup import (
    ask_animal,
    ask_batch,
    ask_experimenter,
    ask_last_training_level,
    ask_starting_training_level,
    ask_time_parameters,
    save_yaml,
    verify_session,
)


def main():
    """
    This startup script is run before Bonsai is opened in order to make some pre-session configurations.
    """
    # Load config.yml
    with open("../src/config/config.yml", "r") as file:
        config = yaml.safe_load(file)

    # Convert the setup.csv and training.csv into JSON files so that Bonsai is able to read them
    converter(config["paths"]["training"], "training")

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
        animal_file = config["paths"]["animal"]
    else:
        animal_file = config["paths"]["animal_dir"] + "/template.yml"

    # Load the animal.yml config file
    with open(animal_file, "r") as file:
        animal_config = yaml.safe_load(file)

    # Possible path to the current animal output directory
    animal_out_dir = config["paths"]["output"] + "/" + batch + "/" + animal
    dirs = ["200101"]
    if os.path.isdir(animal_out_dir):
        entries = os.listdir(animal_out_dir)
        dirs = [
            entry
            for entry in entries
            if os.path.isdir(os.path.join(animal_out_dir, entry))
        ]

    animal_out_backup = config["paths"]["output_backup"] + "/" + batch + "/" + animal
    output_dirs = ["200101"]
    if os.path.isdir(animal_out_backup):
        entries = os.listdir(animal_out_backup)
        output_dirs = [
            entry
            for entry in entries
            if os.path.isdir(os.path.join(animal_out_backup, entry))
        ]

    if datetime.strptime(dirs[-1], "%y%m%d") >= datetime.strptime(
        output_dirs[-1], "%y%m%d"
    ):
        animal_out = os.path.join(animal_out_dir, dirs[-1])
    else:
        animal_out = os.path.join(animal_out_backup, output_dirs[-1])

    # Try to read the last out.csv file and return from function if something goes wrong
    try:
        out_name = "out_" + animal + "_" + str(dirs[-1]) + ".csv"
        df = pd.read_csv(os.path.join(animal_out, out_name))
        # Ask for user input to update animal.yml file
        verify_session(animal_config, df, dirs[-1])
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
    animal_config["session"]["last_training_level"] = ask_last_training_level()

    # Save animal and config files
    os.makedirs(config["paths"]["animal_dir"] + "/" + batch, exist_ok=True)
    save_yaml(animal_config, config["paths"]["animal"], type="animal")
    save_yaml(config, "../src/config/config.yml", type="config")
    save_setup(config["paths"]["setup"], config["setup"])
