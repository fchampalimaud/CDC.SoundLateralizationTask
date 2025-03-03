import os
from generate_csv import generate_csv


def func(input_directory):
    # Walks through the directory
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            # Checks if the file is a JSON file
            if file.endswith(".json"):
                # Gets the full file path
                file_path = os.path.join(root, file)
                desired_file = file_path.replace(".json", ".csv")
                if not os.path.isfile(desired_file):
                    generate_csv(file_path, desired_file)


if __name__ == "__main__":
    func("../src/output")
