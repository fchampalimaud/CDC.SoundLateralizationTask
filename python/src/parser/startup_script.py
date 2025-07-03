import os
from datetime import datetime
from parser.config_to_json import converter

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

    # Update block_number, trial_number and starting_training_level
    animal_config["session"]["block_number"] = 1
    animal_config["session"]["starting_trial_number"] = int(
        output_data.loc[output_data.index[-1], "trial"] + 1
    )
    animal_config["session"]["starting_training_level"] = int(
        output_data.loc[output_data.index[-1], "training_level"]
    )


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
            "Get parameters from last session (fixation time, reaction time and lnp_time)? [y/n] "
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
            break
        elif update_lower == "n":
            break
        else:
            print("Not a valid input.")


def startup():
    """
    This function executes before the session starts in order to ensure the configuration files are correctly updated.
    """
    # Load config.yml
    with open("../src/config/config.yml", "r") as file:
        config = yaml.safe_load(file)

    # Convert the setup.csv and training.csv into JSON files so that Bonsai is able to read them
    converter(config["paths"]["setup"], "setup")
    converter(config["paths"]["training"], "training")

    # Load the animal.yml config file
    with open(config["paths"]["animal"], "r") as file:
        animal_config = yaml.safe_load(file)

    # Possible path to the current animal output directory
    animal_dir = (
        config["paths"]["output"]
        + "/"
        + animal_config["batch"]
        + "/"
        + animal_config["animal_id"]
    )

    # If the animal output directory exists
    if os.path.isdir(animal_dir):
        entries = os.listdir(animal_dir)
        dirs = [
            entry for entry in entries if os.path.isdir(os.path.join(animal_dir, entry))
        ]
        dir_path = os.path.join(animal_dir, dirs[-1])

        # Try to read the last out.csv file and return from function if something goes wrong
        try:
            df = pd.read_csv(os.path.join(dir_path, "out.csv"))
        except:
            return

        # Ask for user input to update animal.yml file
        verify_session(animal_config, df, dirs[-1])
        ask_time_parameters(animal_config, df)

        # Add JSON schema
        yaml_string = (
            "# yaml-language-server: $schema=https://raw.githubusercontent.com/fchampalimaud/CDC.SoundLateralizationTask/refs/heads/main/src/config/schemas/animal-schema.json\n"
            + yaml.dump(animal_config, default_flow_style=False)
        )

        # Write new animal.yml file
        with open(config["paths"]["animal"], "w") as file:
            file.write(yaml_string)
