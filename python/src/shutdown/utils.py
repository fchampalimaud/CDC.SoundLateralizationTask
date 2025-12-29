import json
import os
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from shutdown.block_plots import generate_plots
from shutdown.video_preprocessing import add_frame_numbers


def read_out_json(file: Path):
    """
    Reads a `out.json` file, formats it to be a real JSON and returns a dictionary.

    Parameters
    ----------
    file : Path
        path of the JSON file to be read.

    Returns
    -------
    dict
        Dictionary containing the data parsed from the JSON file.
    """
    # Read the fake JSON file
    with open(file, "r") as f:
        text = f.read()

    # Delete file if empty
    if text == "":
        os.remove(file)
        return

    # Delete last line if it doesn't end in '\n'
    if text[-1] != "\n":
        idx = text.rfind("\n")
        text = text[: idx + 1]

    # Split the JSON object into lines
    lines = text.splitlines()

    # Convert to real JSON
    for i in range(len(lines) - 1):
        lines[i] += ","
    lines.insert(0, "[")
    lines.append("]")
    text = "\n".join(lines)

    # Load the real JSON string
    return json.loads(text)


def convert_output(session_dir: Path, backup_dir: Optional[Path] = None):
    """
    Converts the out structure from JSON to CSV.

    Parameters
    ----------
    session_dir : Path
        the path to the session directory
    backup_dir : Path, optional
        the path to the backup directory
    """
    # Pandas config to get rid of warnings
    pd.set_option("future.no_silent_downcasting", True)

    # Get all of the out.json files
    out_files = [p for p in (session_dir / "unparsed_out").iterdir() if p.is_file()]

    # Convert every JSON file to Pandas DataFrame and add them to the final DataFrame
    for i in range(len(out_files)):
        # Load the real JSON string
        out_json = read_out_json(out_files[i])

        # Continue to next file if current one was empty
        if out_json is None:
            continue

        # Convert JSON to pandas DataFrame, rename the columns to shorter and more intuitive names and replace "NaN" strings
        df = pd.json_normalize(out_json)
        df = df.rename(columns=COLUMN_RENAMES)
        df.replace("NaN", np.nan, inplace=True)

        # Declare expected camera metadata file
        time_str = out_files[i].name.split("_")[1].split(".")[0]
        cam_metadata_path = session_dir / ("cam_metadata_" + time_str + ".csv")

        # Create columns of the frame numbers that correspond to specific events of a trial if camera metadata exists
        if cam_metadata_path.is_file():
            try:
                df = add_frame_numbers(df, session_dir, time_str)
            except Exception:
                print("It was not possible to process the camera metadata")

        # If variable containing out structure already exists, append data to it, otherwise create it
        if "out" not in locals():
            out = df.copy()
        else:
            out = pd.concat([out, df], ignore_index=True)

    # Save out structure to CSV
    out_name = "out_" + session_dir.parent.name + "_" + session_dir.name + ".csv"
    out_path = session_dir / out_name
    out.to_csv(out_path, index=False)
    if backup_dir is not None:
        out_backup_path = backup_dir / out_name
        out.to_csv(out_backup_path, index=False)

    # Declare path to the directory where the plots will be saved
    plot_path = session_dir / "plots"
    os.makedirs(plot_path, exist_ok=True)
    plot_backup_path = None
    if backup_dir is not None:
        plot_backup_path = backup_dir / "plots"
        os.makedirs(plot_backup_path, exist_ok=True)

    # Generate plots with some metrics for the each block of the current session
    generate_plots(out, plot_path, plot_backup_path)


COLUMN_RENAMES = {
    "animal_id": "animal",
    "trial.number": "trial",
    "trial.start_time": "trial_start",
    "trial.tared_start_time": "tared_trial_start",
    "trial.end_time": "trial_end",
    "trial.duration": "trial_duration",
    "block.number": "block",
    "block.training_level": "training_level",
    "block.trials_per_block": "trials_per_block",
    "session.number": "session",
    "session.type": "session_type",
    "session.box": "box",
    "sound.abl": "ABL",
    "sound.ild": "ILD",
    "sound.sound_index": "sound_index",
    "sound.left_amp": "left_amp",
    "sound.right_amp": "right_amp",
    "iti.intended_duration": "intended_iti",
    "iti.start_time": "iti_start",
    "iti.end_time": "iti_end",
    "iti.timed_duration": "iti_duration",
    "cnp.start_time": "cnp_start",
    "cnp.timed_value": "cnp_time",
    "cnp.max_duration": "max_cnp",
    "fixation_time.opto_onset_time.base_time": "base_ft_oot",
    "fixation_time.opto_onset_time.exp_mean": "ft_oot_exp",
    "fixation_time.opto_onset_time.intended_duration": "intended_ft_oot",
    "fixation_time.opto_onset_time.timed_duration": "timed_ft_oot",
    "fixation_time.sound_onset_time.base_time": "base_ft_sot",
    "fixation_time.sound_onset_time.exp_mean": "ft_sot_exp",
    "fixation_time.sound_onset_time.intended_duration": "intended_ft_sot",
    "fixation_time.sound_onset_time.timed_duration": "duration_ft_sot",
    "fixation_time.intended_duration": "intended_fix_time",
    "fixation_time.timed_duration": "fix_time",
    "fixation_time.total_duration": "total_fix_time",
    "reaction_time.base_time": "base_rt",
    "reaction_time.max_duration": "max_rt",
    "reaction_time.start_time": "rt_start",
    "reaction_time.timed_duration": "timed_rt",
    "movement_time.max_duration": "max_mt",
    "movement_time.start_time": "mt_start",
    "movement_time.timed_duration": "timed_mt",
    "lnp_time.intended_duration": "intended_lnp",
    "lnp_time.start_time": "lnp_start",
    "lnp_time.timed_duration": "timed_lnp",
    "outcome.response_poke": "response_poke",
    "outcome.success": "success",
    "outcome.abort_type": "abort_type",
    "outcome.block_performance": "block_perf",
    "outcome.block_abort_ratio": "block_abort_ratio",
    "penalty_times.incorrect": "incorrect_penalty",
    "penalty_times.abort": "abort_penalty",
    "penalty_times.fixation_abort": "ft_abort_penalty",
    "reward.left": "reward_left",
    "reward.right": "reward_right",
    "reward.delivered": "reward_delivered",
    "optogenetics.opto_trial": "opto_trial",
    "optogenetics.duration": "opto_duration",
    "optogenetics.mode": "opto_mode",
    "optogenetics.led0_voltage": "led0_voltage",
    "optogenetics.led0_power": "led0_power",
    "optogenetics.led1_voltage": "led1_voltage",
    "optogenetics.led1_power": "led1_power",
}
