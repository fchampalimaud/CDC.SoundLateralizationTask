import pandas as pd
import json
import numpy as np
from typing import Literal
import yaml


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
    """Unflatten a JSON dictionary object, with keys like 'a.b.c'"""
    result_dict = {}

    for k, v in json_dict.items():
        *nested_parts, field_name = k.split(".")

        obj = result_dict
        for p in nested_parts:
            obj = obj.setdefault(p, {})

        obj[field_name] = v

    return result_dict


def converter(filepath: str, filetype: Literal["setup", "training"]):
    df = pd.read_csv(filepath)
    headers = df.columns.tolist()

    if filetype == "setup":
        header = """{
    "$schema": "https://raw.githubusercontent.com/fchampalimaud/CDC.SoundLateralizationTask/refs/heads/main/src/config/schemas/setup-list-schema.json",
    "setups": ["""

        footer = """    ]
}"""
    elif filetype == "training":
        header = """{
    "$schema": "https://raw.githubusercontent.com/fchampalimaud/CDC.SoundLateralizationTask/refs/heads/main/src/config/schemas/training-schema.json",
    "levels": ["""

        footer = """    ]
}"""

    lines = []
    for i in range(df.shape[0]):
        values = df.iloc[i].tolist()
        if filetype == "setup":
            values[1] = json.loads(values[1].replace("'", '"'))
        dictionary = dict(zip(headers, values))
        nested_dict = unflatten_json(dictionary)
        lines.append(nested_dict)

    with open("../src/config/" + filetype + ".json", "w") as f:
        f.write(header + "\n")
        for i in range(len(lines)):
            json_line = json.dumps(lines[i], cls=NpEncoder)
            if i == len(lines) - 1:
                f.write("        " + json_line + "\n")
            else:
                f.write("        " + json_line + ",\n")
        f.write(footer + "\n")
