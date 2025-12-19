import re
from pathlib import Path
from tkinter import filedialog

from shutdown.utils import convert_output


def convert_tool():
    session_dir = filedialog.askdirectory()
    recursive_convert(Path(session_dir))
    print("Conversion completed!")


def recursive_convert(dir: Path):
    if _check_session(dir) and _check_unparsed_out(dir):
        convert_output(dir)
    elif _check_animal(dir):
        for entry in dir.iterdir():
            if not entry.is_file() and _check_session(entry):
                recursive_convert(entry)
    elif _check_batch(dir):
        for entry in dir.iterdir():
            if not entry.is_file() and _check_animal(entry):
                recursive_convert(entry)


def _check_unparsed_out(dir: Path) -> bool:
    for entry in dir.iterdir():
        if not entry.is_file() and entry.name == "unparsed_out":
            return True
    return False


def _check_session(dir: Path) -> bool:
    return re.fullmatch(r"^\d{6}", dir.name)


def _check_animal(dir: Path) -> bool:
    return re.fullmatch(r"^[A-Z]{2,6}\d{4}$", dir.name)


def _check_batch(dir: Path) -> bool:
    return re.fullmatch(r"^[a-zA-Z0-9][a-zA-Z0-9_]*[a-zA-Z0-9]$", dir.name)
