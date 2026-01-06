from pathlib import Path

import yaml

from shutdown.utils import convert_output


def main():
    # Open config.yml file
    with open("../src/config/config.yml", "r") as file:
        config = yaml.safe_load(file)

    # Open animal.yml file
    with open(config["paths"]["animal"], "r") as file:
        animal_config = yaml.safe_load(file)

    animal_dir = (
        Path(config["paths"]["output"])
        / animal_config["batch"]
        / animal_config["animal_id"]
    )

    if config["paths"]["output_backup"] == "":
        animal_backup_dir = None
    else:
        animal_backup_dir = (
            Path(config["paths"]["output_backup"])
            / animal_config["batch"]
            / animal_config["animal_id"]
        )

    # Get all of the directories inside the animal directory
    session_dir = [entry for entry in animal_dir.iterdir() if entry.is_dir()][-1]
    if animal_backup_dir is not None:
        session_backup_dir = animal_backup_dir / session_dir.name

    convert_output(session_dir, session_backup_dir)
