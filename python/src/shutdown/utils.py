import glob
import json
import os

import pandas as pd

from shutdown.video_preprocessing import add_frame_numbers


def append_json(dir: str):
    """
    Appends all of the "fake" JSON files inside the input directory.

    Parameters
    ----------
    dir : str
        the path to the input directory.

    Returns
    -------
    data : dict
        the appended JSON string from every unparsed output file.
    """
    # Initialize the final string object
    json_string = ""

    # Walk through the directory
    for root, _, files in os.walk(dir):
        for file in files:
            # Check if the file is a JSON file
            if file.endswith(".json"):
                # Get the full file path
                path = os.path.join(root, file)

                # Load the JSON data
                with open(path, "r") as json_file:
                    try:
                        text = json_file.read()
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file {path}: {e}")

                # Delete file if empty
                if text == "":
                    os.remove(path)
                else:
                    # Append the data to the string
                    json_string += text

    # Split the JSON object into lines
    lines = json_string.splitlines()

    # Convert to real JSON
    for i in range(len(lines) - 1):
        lines[i] += ","
    lines.insert(0, "[")
    lines.append("]")
    text = "\n".join(lines)

    # Load the real JSON string
    data = json.loads(text)

    return data


def generate_csv(data: dict, path: str):
    """
    Generates a CSV file from a JSON object.

    Parameters
    ----------
    data : str
        the JSON object to convert to CSV.
    path : str
        the path to the output file.

    Returns
    -------
    df : DataFrame
        the output structure pandas DataFrame.
    """

    # Create a DataFrame from a dictionary
    df = pd.json_normalize(data)

    # Rename the columns to shorter and more intuitive names
    df = df.rename(columns=COLUMN_RENAMES)

    dir = os.path.dirname(path)
    if glob.glob(os.path.join(dir, "cam_metadata_*.csv")):
        # df = add_frame_numbers(df, dir)
        try:
            df = add_frame_numbers(df, dir)
        except Exception:
            print("It was not possible to process the camera metadata.")

    # Save the DataFrame to CSV
    df.to_csv(path, index=False)

    return df


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
    "optogenetics.opto_trial": "opto_trial",
    "optogenetics.duration": "opto_duration",
    "optogenetics.mode": "opto_mode",
    "optogenetics.led0_voltage": "led0_voltage",
    "optogenetics.led0_power": "led0_power",
    "optogenetics.led1_voltage": "led1_voltage",
    "optogenetics.led1_power": "led1_power",
}
