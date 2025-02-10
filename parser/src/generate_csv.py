import pandas as pd
import json
import os

def generate_csv(input_file: str, output_file: str):
    """
    Generates a CSV file from a "fake" JSON file.

    Parameters
    ----------
    input_file: str
        the path to the input file.
    output_file: str
        the path to the output file.
    """
    # Opens JSON file as text and separates its lines
    with open(input_file, 'r') as file:
        lines = [line.strip() for line in file]

    # Converts to real JSON
    for i in range(len(lines) - 1):
        lines[i] += ','
    lines.insert(0, '[')
    lines.append(']')
    text = '\n'.join(lines)

    # Loads the real JSON string
    data = json.loads(text)

    # Creates a DataFrame
    df = pd.json_normalize(data)

    # Converts DataFrame to CSV
    df.to_csv(output_file, index=False)

def append_json(input_directory: str, output_file: str):
    """
    Appends all of the "fake" JSON files inside the input directory.

    Parameters
    ----------
    input_directory: str
        the path to the input directory.
    output_file: str
        the path to the output file.
    """
    # Initializes the final string object
    all_data = "" 

    # Walks through the directory
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            # Checks if the file is a JSON file
            if file.endswith('.json'): 
                # Gets the full file path
                file_path = os.path.join(root, file) 
                with open(file_path, 'r') as json_file:
                    try:
                        # Loads the JSON data
                        text = json_file.read() 
                        # Appends the data to the string
                        all_data += text  
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file {file_path}: {e}")

    # Generates the final "fake" JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(all_data)
