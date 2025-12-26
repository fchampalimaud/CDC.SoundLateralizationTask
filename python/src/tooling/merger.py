import re
from pathlib import Path
from tkinter import filedialog

import pandas as pd


def main():
    animal_dir = Path(filedialog.askdirectory())

    if _check_animal(animal_dir):
        for entry in animal_dir.iterdir():
            if not entry.is_file() and _check_session(entry):
                out_path = entry / (
                    "out_" + animal_dir.name + "_" + entry.name + ".csv"
                )
                if out_path.is_file():
                    df = pd.read_csv(out_path, na_values=["NaN"])
                    if "out" not in locals():
                        out = df.copy()
                    else:
                        out = pd.concat([out, df], ignore_index=True)

        out.to_csv(animal_dir / "out.csv", index=False)

    print("Merge completed!")


def _check_session(dir: Path) -> bool:
    return re.fullmatch(r"^\d{6}", dir.name)


def _check_animal(dir: Path) -> bool:
    return re.fullmatch(r"^[A-Z]{2,6}\d{4}$", dir.name)
