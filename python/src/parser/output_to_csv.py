import os
from parser.generate_csv import generate_csv
import re
import yaml


def convert_output():
    with open("../src/config/config.yml", "r") as file:
        config = yaml.safe_load(file)

    # Walks through the directory
    for root, dirs, files in os.walk(config["output_path"]):
        for file in files:
            # Checks if the file is a JSON file
            if re.match(r"^out_\d+\.json$", file):
                # Gets the full file path
                file_path = os.path.join(root, file)
                desired_file = file_path.replace(".json", ".csv")
                if not os.path.isfile(desired_file):
                    generate_csv(file_path, desired_file)


if __name__ == "__main__":
    convert_output()
