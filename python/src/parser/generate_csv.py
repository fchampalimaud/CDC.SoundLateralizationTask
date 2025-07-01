import json
import os

import pandas as pd

COLUMN_RENAMES = {
    "animal_id": "animal",
    "trial.number": "trial",
    "trial.computer_start_time": "computer_trial_start",
    "trial.computer_end_time": "computer_trial_end",
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
    "time_to_cnp.timed_value": "max_cnp",
    "time_to_cnp.max_duration": "cnp_time",
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
    "reaction_time.timed_duration": "timed_rt",
    "movement_time.max_duration": "max_mt",
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

    df = df.rename(columns=COLUMN_RENAMES)

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
