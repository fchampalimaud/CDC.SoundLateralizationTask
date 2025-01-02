import pandas as pd
import json
import os

def generate_csv(output_filename: str, read_filename: str):
    # Open json file
    with open(read_filename, 'r') as file:
        lines = [line.strip() for line in file]

    # Converts to real "json"
    for i in range(len(lines) - 1):
        lines[i] += ','
    lines.insert(0, '[')
    lines.append(']')
    text = '\n'.join(lines)

    # Loads the real json string
    data = json.loads(text)

    # Create a DataFrame
    df = pd.json_normalize(data)

    # Convert DataFrame to CSV
    df.to_csv(output_filename, index=False)

def append_json(output_filename: str, read_directory: str):
    all_data = ""  # List to hold the combined data

    # Walk through the directory
    for root, dirs, files in os.walk(read_directory):
        for file in files:
            if file.endswith('.json'):  # Check if the file is a JSON file
                file_path = os.path.join(root, file)  # Get the full file path
                with open(file_path, 'r') as json_file:
                    try:
                        text = json_file.read()  # Load the JSON data
                        all_data += text  # Append the data to the list
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file {file_path}: {e}")

    with open (output_filename, 'w', encoding='utf-8') as file:
        file.write(all_data)
