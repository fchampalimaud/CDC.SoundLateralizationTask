import json
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd
import yaml

from startup.utils import YamlFile


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.bool):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def unflatten_json(json_dict: dict):
    """
    Unflattens a JSON dictionary object, with keys like 'a.b.c'.

    Parameters
    ----------
    json_dict : dict
        the dictionary containing the JSON object.
    """
    result_dict = {}

    for k, v in json_dict.items():
        *nested_parts, field_name = k.split(".")

        obj = result_dict
        for p in nested_parts:
            obj = obj.setdefault(p, {})

        obj[field_name] = v

    return result_dict


def from_csv_to_json(filepath: Path, *, type: Literal["setup", "training"]):
    """
    Converts a CSV config file into a JSON file so that Bonsai is able to read it.

    Parameters
    ----------
    filepath : Path
        the path to the file being converted.
    filetype : Literal["setup", "training"]
        indicates whether the file being converted is the setup.csv or training.csv.
    """
    df = pd.read_csv(filepath)
    headers = df.columns.tolist()

    # Add the respective header to the JSON file
    if type == "setup":
        header = """{
    "$schema": "https://raw.githubusercontent.com/fchampalimaud/CDC.SoundLateralizationTask/refs/heads/main/src/config/schemas/setup-schema.json",
    "setups": ["""

        footer = """    ]
}"""
    elif type == "training":
        header = """{
    "$schema": "https://raw.githubusercontent.com/fchampalimaud/CDC.SoundLateralizationTask/refs/heads/main/src/config/schemas/training-schema.json",
    "levels": ["""

        footer = """    ]
}"""

    lines = []
    for i in range(df.shape[0]):
        values = df.iloc[i].tolist()
        if type == "setup":
            values[1] = json.loads(values[1].replace("'", '"'))
        else:
            values[6] = json.loads(values[6])
        dictionary = dict(zip(headers, values))
        nested_dict = unflatten_json(dictionary)
        lines.append(nested_dict)

    # Save the JSON file
    with open("../src/config/" + type + ".json", "w") as f:
        f.write(header + "\n")
        for i in range(len(lines)):
            json_line = json.dumps(lines[i], cls=NpEncoder)
            if i == len(lines) - 1:
                f.write("        " + json_line + "\n")
            else:
                f.write("        " + json_line + ",\n")
        f.write(footer + "\n")


def save_setup(filepath: str, index: int):
    df = pd.read_csv(filepath)
    setup_dict = df.to_dict(orient="records")[index]
    setup_dict["sounds"] = json.loads(setup_dict["sounds"].replace("'", '"'))
    setup_dict = unflatten_json(setup_dict)

    # Save file
    with open("../src/config/setup.json", "w") as file:
        json.dump(setup_dict, file, indent=4)


def save_yaml(data: dict, filepath: Path, *, type: YamlFile):
    # Store schema path according to file type
    match type:
        case YamlFile.CONFIG:
            schema = "# yaml-language-server: $schema=schemas/config-schema.json\n"
        case YamlFile.ANIMAL:
            schema = "# yaml-language-server: $schema=https://raw.githubusercontent.com/fchampalimaud/CDC.SoundLateralizationTask/refs/heads/main/src/config/schemas/animal-schema.json\n"

    # Add JSON schema to yaml structure
    yaml_string = schema + yaml.safe_dump(
        data, default_flow_style=False, sort_keys=False
    )

    # Save file
    with open(filepath, "w") as file:
        file.write(yaml_string)
