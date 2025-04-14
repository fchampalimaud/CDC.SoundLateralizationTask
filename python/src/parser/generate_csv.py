import json
import os

import pandas as pd


def generate_csv(data: str, filepath: str):
    """
    Generates a CSV file from a JSON object.

    Parameters
    ----------
    data: str
        the JSON object to convert to CSV.
    filepath: str
        the path to the output file.
    """

    # Split the JSON object into
    lines = data.splitlines()

    # Convert to real JSON
    for i in range(len(lines) - 1):
        lines[i] += ","
    lines.insert(0, "[")
    lines.append("]")
    text = "\n".join(lines)

    # Load the real JSON string
    data = json.loads(text)

    # Create a DataFrame
    df = pd.json_normalize(data)

    # Convert the DataFrame to CSV
    df.to_csv(filepath, index=False)


def append_json(input_directory: str):
    """
    Appends all of the "fake" JSON files inside the input directory.

    Parameters
    ----------
    input_directory: str
        the path to the input directory.
    """
    # Initialize the final string object
    all_data = ""

    # Walk through the directory
    for root, _, files in os.walk(input_directory):
        for file in files:
            # Check if the file is a JSON file
            if file.endswith(".json"):
                # Get the full file path
                file_path = os.path.join(root, file)

                # Load the JSON data
                with open(file_path, "r") as json_file:
                    try:
                        text = json_file.read()
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file {file_path}: {e}")

                # Delete file if empty
                if text == "":
                    os.remove(file_path)
                else:
                    # Append the data to the string
                    all_data += text

    return all_data
