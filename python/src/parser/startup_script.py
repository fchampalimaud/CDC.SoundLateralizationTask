import yaml
import pandas as pd
import os
import re
from parser.config_to_json import converter


def startup():
    with open("../src/config/config.yml", "r") as file:
        config = yaml.safe_load(file)

    with open(config["animal_path"], "r") as file:
        animal_config = yaml.safe_load(file)

    while True:
        update = input(
            "Do you want to update animal.yml based on the last session? [y/n] "
        )
        update_lower = update.lower()
        if update_lower == "y" or update_lower == "n":
            break

    if update_lower == "y":
        animal_dir = config["output_path"] + "/Rat" + f"{animal_config["animal_id"]:03}"
        if os.path.isdir(animal_dir):
            entries = os.listdir(animal_dir)
            dirs = [
                entry
                for entry in entries
                if os.path.isdir(os.path.join(animal_dir, entry))
            ]
            dir_path = os.path.join(animal_dir, dirs[-1])
            entries = os.listdir(dir_path)
            last_csv = [
                entry
                for entry in entries
                if os.path.isfile(os.path.join(dir_path, entry))
                and re.match(r"^out_\d+\.csv$", entry)
            ][-1]

            df = pd.read_csv(os.path.join(dir_path, last_csv))

            animal_config["session"]["number"] = int(
                df.loc[df.index[-1], "session.number"] + 1
            )
            animal_config["session"]["starting_trial_number"] = int(
                df.loc[df.index[-1], "trial.number"] + 1
            )
            animal_config["session"]["starting_block_number"] = int(
                df.loc[df.index[-1], "block.number"] + 1
            )
            animal_config["fixation_time"]["opto_onset_time"]["min_value"] = float(
                df.loc[df.index[-1], "fixation_time.opto_onset_time.base_time"]
            )
            animal_config["fixation_time"]["sound_onset_time"]["min_value"] = float(
                df.loc[df.index[-1], "fixation_time.sound_onset_time.base_time"]
            )
            animal_config["reaction_time"]["min_value"] = float(
                df.loc[df.index[-1], "reaction_time.base_time"]
            )
            animal_config["lnp_time"]["min_value"] = float(
                df.loc[df.index[-1], "lnp_time.intended_duration"]
            )

            yaml_string = (
                "# yaml-language-server: $schema=schemas/animal-schema.json\n"
                + yaml.dump(animal_config, default_flow_style=False)
            )
            with open(config["animal_path"], "w") as file:
                file.write(yaml_string)

    converter(config["setup_path"], "setup")
    converter(config["training_path"], "training")
