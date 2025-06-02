import os
from parser.generate_csv import append_json, generate_csv

import yaml


def convert_output():
    """
    Converts the output files from one day (which should correspond to a session) for an animal into a single CSV file.
    """
    # Open config.yml file
    with open("../src/config/config.yml", "r") as file:
        config = yaml.safe_load(file)

    # Open animal.yml file
    with open(config["paths"]["animal"], "r") as file:
        animal_config = yaml.safe_load(file)

    # Get the animal output directory
    animal_dir = (
        config["paths"]["output"]
        + "/"
        + animal_config["batch"]
        + "/"
        + animal_config["animal_id"]
    )

    # Get the directory from last session
    entries = os.listdir(animal_dir)
    dirs = [
        entry for entry in entries if os.path.isdir(os.path.join(animal_dir, entry))
    ]
    dir_path = os.path.join(animal_dir, dirs[-1], "outs")

    # Concatenate the data from every output JSON file in the last session directory
    all_data = append_json(dir_path)

    # Generate the out.csv file from the JSON structure
    generate_csv(all_data, os.path.join(animal_dir, dirs[-1], "out.csv"))
