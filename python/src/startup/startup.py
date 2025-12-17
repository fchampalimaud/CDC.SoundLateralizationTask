import os
import re
from datetime import datetime
from typing import Literal

import pandas as pd
import yaml


def verify_session(animal_config: dict, output_data: pd.DataFrame, last_dir: str):
    """
    Asks the user whether it should start a new session or not and updates the animal.yml file accordingly.

    Parameters
    ----------
    animal_config : dict
        the dictionary containing the parameters from the animal.yml file.
    output_data : pd.DataFrame
        the dataframe containing the data from the last session out.csv.
    last_dir : str
        the name of the directory from last session, which is in the format `YYMMDD`
    """

    last_session_date = datetime.strptime(last_dir, "%y%m%d").date()

    if last_session_date == datetime.today().date():
        animal_config["session"]["number"] = int(
            output_data.loc[output_data.index[-1], "session"]
        )
        animal_config["session"]["block_number"] = int(
            output_data.loc[output_data.index[-1], "block"] + 1
        )
    else:
        animal_config["session"]["number"] = int(
            output_data.loc[output_data.index[-1], "session"] + 1
        )
        animal_config["session"]["block_number"] = 1


def ask_time_parameters(animal_config: dict, df: pd.DataFrame):
    """
    Asks the user whether it should update the time-related parameters (fixation time, reaction time and lnp time) in the animal.yml file.

    Parameters
    ----------
    animal_config : dict
        the dictionary containing the parameters from the animal.yml file.
    output_data : pd.DataFrame
        the dataframe containing the data from the last session out.csv.
    """
    while True:
        # Ask for user input
        update = input(
            "Get parameters from last session (fixation time, reaction time, lnp_time and training_level)? [y/n] "
        )
        update_lower = update.lower()

        if update_lower == "y" or update_lower == "":
            animal_config["fixation_time"]["opto_onset_time"]["min_value"] = float(
                df.loc[df.index[-1], "base_ft_oot"]
            )
            animal_config["fixation_time"]["sound_onset_time"]["min_value"] = float(
                df.loc[df.index[-1], "base_ft_sot"]
            )
            animal_config["reaction_time"]["min_value"] = float(
                df.loc[df.index[-1], "base_rt"]
            )
            animal_config["lnp_time"]["min_value"] = float(
                df.loc[df.index[-1], "intended_lnp"]
            )
            animal_config["session"]["starting_training_level"] = int(
                df.loc[df.index[-1], "training_level"]
            )
            break
        elif update_lower == "n":
            break
        else:
            print("Not a valid input.")


def ask_experimenter():
    while True:
        experimenter = input("Hello! :) Let me know who you are, please: ")

        if not bool(re.fullmatch(r"^[A-Z]([a-zA-Z -])*[a-zA-Z]$", experimenter)):
            print(
                "This is not a valid name! The name must start with a capital letter and end with a letter. Warning: numbers, punctuation and unicode characters (such as accented characters) can't be used."
            )
            continue

        break

    if os.path.exists("./assets/users.yml"):
        with open("./assets/users.yml", "r") as file:
            users = yaml.safe_load(file)
        for user in users:
            if experimenter == user:
                print("Welcome back! :)")
                return experimenter
        users.append(experimenter)
    else:
        users = [experimenter]

    print("Welcome! :)")

    with open("./assets/users.yml", "w") as file:
        yaml.safe_dump(users, file, default_flow_style=False, sort_keys=False)

    return experimenter


def ask_batch():
    while True:
        batch = input("Are you training an animal from which batch? ")

        if not re.fullmatch(r"^[a-zA-Z0-9][a-zA-Z0-9_]*[a-zA-Z0-9]$", batch):
            print(
                "This is not a valid batch name! You can only use ASCII letters and numbers. Additionally, you can use underscores (_) in the middle of the name."
            )
            continue

        return batch


def ask_animal():
    while True:
        # Animal prompt
        animal = input("Which furry friend is going to be joining us? ")

        # Check if the animal ID is valid
        if not re.fullmatch(r"^[A-Z]{2,6}\d{4}$", animal):
            print(
                "This is not a valid animal ID! The animal ID must be composed by 2 to 6 letters followed by 4 digits (ex: ANIMAL0000)."
            )
            continue

        return animal


def ask_starting_training_level():
    while True:
        # Starting training level prompt
        starting_training_level = input(
            "What is the training level you want the animal to start in? (You can leave blank to keep the current value) "
        )

        # Check if the animal ID is valid
        if not re.fullmatch(r"^(?:\d{1,2})?$", starting_training_level):
            print(
                "This is not a valid training level! Leave the prompt blank or write up to 2 digits."
            )
            continue
        elif starting_training_level != "" and int(starting_training_level) > 16:
            print(
                "This is not a valid training level! There are only 16 training levels."
            )
            continue

        if starting_training_level == "":
            return -1
        else:
            return int(starting_training_level)


def ask_last_training_level():
    while True:
        # Last training level prompt
        last_training_level = input(
            "What is the training level the animal should stop progressing? (You can leave blank if the animal can progress until the last level) "
        )

        # Check if the animal ID is valid
        if not re.fullmatch(r"^(?:\d{1,2})?$", last_training_level):
            print(
                "This is not a valid training level! Leave the prompt blank or write up to 2 digits."
            )
            continue

        if last_training_level == "":
            return 16  # FIXME
        else:
            return int(last_training_level)


def save_yaml(data: dict, filepath: str, type: Literal["animal", "config"]):
    # Store schema path according to file type
    if type == "animal":
        schema = "# yaml-language-server: $schema=https://raw.githubusercontent.com/fchampalimaud/CDC.SoundLateralizationTask/refs/heads/main/src/config/schemas/animal-schema.json\n"
    else:
        schema = "# yaml-language-server: $schema=schemas/config-schema.json\n"

    # Add JSON schema to yaml structure
    yaml_string = schema + yaml.safe_dump(
        data, default_flow_style=False, sort_keys=False
    )

    # Save file
    with open(filepath, "w") as file:
        file.write(yaml_string)
