import os

import numpy as np
import pandas as pd
import yaml

# from shutdown.plotting import generate_plots, generate_plots_refactored
from shutdown.block_plots import generate_plots
from shutdown.utils import append_json, generate_csv


class Shutdown:
    def __init__(self):
        # Open config.yml file
        with open("../src/config/config.yml", "r") as file:
            self.config = yaml.safe_load(file)

        # Open animal.yml file
        with open(self.config["paths"]["animal"], "r") as file:
            self.animal_config = yaml.safe_load(file)

        # Get the animal output directory
        self.animal_dir = (
            self.config["paths"]["output"]
            + "/"
            + self.animal_config["batch"]
            + "/"
            + self.animal_config["animal_id"]
        )

        # Get all of the directories inside the animal directory
        entries = os.listdir(self.animal_dir)
        self.dirs = [
            entry
            for entry in entries
            if os.path.isdir(os.path.join(self.animal_dir, entry))
        ]

        self.convert_output()
        # self.merge_output()

    def convert_output(self):
        for i in range(len(self.dirs)):
            # Get unparsed out directory path
            out_dir = os.path.join(self.animal_dir, self.dirs[i], "unparsed_out")

            # Concatenate the data from every output JSON file in the last session directory
            out_dict = append_json(out_dir)

            # Set the session output file path
            out_name = "out_" + self.dirs[i] + ".csv"
            out_path = os.path.join(self.animal_dir, self.dirs[i], out_name)

            # Generate the out.csv file from the JSON structure if the file doesn't already exists or if it corresponds to the last session
            if not os.path.isfile(out_path) or (i == len(self.dirs) - 1):
                df = generate_csv(out_dict, out_path)
                # df = pd.read_csv(out_path, na_values=["NaN"])
                df.replace("NaN", np.nan, inplace=True)

                # Generate plots with some metrics for the each block of the current session
                plot_path = os.path.join(self.animal_dir, self.dirs[i], "plots")
                os.makedirs(plot_path, exist_ok=True)
                generate_plots(df, plot_path)

    def merge_output(self):
        out_path = os.path.join(self.animal_dir, self.dirs[0], "out.csv")
        out = pd.read_csv(out_path, na_values=["NaN"])

        for i in range(1, len(self.dirs)):
            out_path = os.path.join(
                self.animal_dir, self.dirs[i], "out_" + self.dirs[i] + ".csv"
            )
            df = pd.read_csv(out_path, na_values=["NaN"])

            out = pd.concat([out, df], axis=0, ignore_index=True)

        out.to_csv(os.path.join(self.animal_dir, "out.csv"), index=False)
