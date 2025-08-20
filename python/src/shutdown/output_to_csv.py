import os

import pandas as pd
import yaml

from shutdown.plotting import generate_plots
from shutdown.utils import append_json, generate_csv


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

    # Get all of the directories inside the animal directory
    entries = os.listdir(animal_dir)
    dirs = [
        entry for entry in entries if os.path.isdir(os.path.join(animal_dir, entry))
    ]

    for i in range(len(dirs)):
        # Get unparsed out directory path
        out_dir = os.path.join(animal_dir, dirs[i], "unparsed_out")

        # Concatenate the data from every output JSON file in the last session directory
        out_dict = append_json(out_dir)

        # Set the session output file path
        out_name = "out_" + dirs[i] + ".csv"
        out_path = os.path.join(animal_dir, dirs[i], out_name)

        # Generate the out.csv file from the JSON structure if the file doesn't already exists or if it corresponds to the last session
        if not os.path.isfile(out_path) or (i == len(dirs) - 1):
            df = generate_csv(out_dict, out_path)
            # df = pd.read_csv(out_path, na_values=["NaN"])

            # Generate plots with some metrics for the each block of the current session
            plot_path = os.path.join(animal_dir, dirs[i], "plots")
            os.makedirs(plot_path, exist_ok=True)
            generate_plots(df, plot_path)


def merge_output():
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

    out_path = os.path.join(animal_dir, dirs[0], "out.csv")
    out = pd.read_csv(out_path, na_values=["NaN"])

    for i in range(1, len(dirs)):
        out_path = os.path.join(animal_dir, dirs[i], "out_" + dirs[i] + ".csv")
        df = pd.read_csv(out_path, na_values=["NaN"])

        out = pd.concat([out, df], axis=0, ignore_index=True)

    out.to_csv(out_path=os.path.join(animal_dir, "out.csv"), index=False)
