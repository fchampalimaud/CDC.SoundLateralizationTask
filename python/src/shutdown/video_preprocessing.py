import json
from pathlib import Path

import harp
import numpy as np
import pandas as pd


def add_frame_numbers(out: pd.DataFrame, path: Path):
    """
    Adds the frame numbers to the out structure for the following events: trial start, CNP start, sound (RT) start, MT start and MT end (or LNP start)

    Parameters
    ----------
    out : pd.DataFrame
        The out DataFrame structure without the frame data.
    path : Path
        The path to the camera metadata file.

    Returns
    -------
    out : pd.DataFrame
        The final out DataFrame structure.
    """
    # Synchronize the camera frames with the Harp timestamps
    strobe = synch_camera(path)
    strobe = strobe[strobe["Timestamp"] >= 0]

    # Create a temporary copy of the out structure
    temp_out = out.copy()
    temp_out["mt_end"] = temp_out["mt_start"] + temp_out["timed_mt"]

    # Convert the type of the relevant columns to float
    temp_out["trial_start"] = temp_out["trial_start"].astype(float)
    temp_out["cnp_start"] = temp_out["cnp_start"].astype(float)
    temp_out["rt_start"] = temp_out["rt_start"].astype(float)
    temp_out["mt_start"] = temp_out["mt_start"].astype(float)
    temp_out["mt_end"] = temp_out["mt_end"].astype(float)

    # Get the frame number of the start of each trial
    df = pd.merge_asof(
        left=temp_out[temp_out["trial_start"].notna()],
        right=strobe,
        left_on="trial_start",
        right_on="Timestamp",
        direction="forward",
    )
    df = df.rename(columns={"FrameID": "trial_start_frame"})
    df = df[["trial", "trial_start_frame"]]
    out = out.merge(df, how="left", on="trial")

    # Get the frame number of the CNP events for each trial
    df = pd.merge_asof(
        left=temp_out[temp_out["cnp_start"].notna()],
        right=strobe,
        left_on="cnp_start",
        right_on="Timestamp",
        direction="forward",
    )
    df = df.rename(columns={"FrameID": "cnp_start_frame"})
    df = df[["trial", "cnp_start_frame"]]
    out = out.merge(df, how="left", on="trial")

    # Get the frame number of the sound start for each trial
    df = pd.merge_asof(
        left=temp_out[temp_out["rt_start"].notna()],
        right=strobe,
        left_on="rt_start",
        right_on="Timestamp",
        direction="forward",
    )
    df = df.rename(columns={"FrameID": "rt_start_frame"})
    df = df[["trial", "rt_start_frame"]]
    out = out.merge(df, how="left", on="trial")

    # Get the frame number of the moment the animal leaves the central port for each trial
    df = pd.merge_asof(
        left=temp_out[temp_out["mt_start"].notna()],
        right=strobe,
        left_on="mt_start",
        right_on="Timestamp",
        direction="forward",
    )
    df = df.rename(columns={"FrameID": "mt_start_frame"})
    df = df[["trial", "mt_start_frame"]]
    out = out.merge(df, how="left", on="trial")

    # FIXME: find out why some data is not being saved correctly
    # Get the frame number of the moment the animal enters one of the lateral pokes for each trial
    try:
        df = pd.merge_asof(
            left=temp_out[(temp_out["mt_end"].notna())],
            right=strobe,
            left_on="mt_end",
            right_on="Timestamp",
            direction="forward",
        )
        df = df.rename(columns={"FrameID": "mt_end_frame"})
        df = df[["trial", "mt_end_frame"]]
        out = out.merge(df, how="left", on="trial")
    except Exception:
        print("It was not possible to add the mt_end_frame column")

    return out


def synch_camera(path: Path):
    """
    Synchronizes the camera data with the Harp timestamps.

    Parameters
    ----------
    path : Path
        The path to the camera metadata file.

    Returns
    -------
    synched_data : pd.DataFrame
        A pandas DataFrame containing a Harp timestamp for every frame, as well as the state of the camera GPIOs and the relevant Harp Behavior GPIOs.
    """

    # Get all of the time strings that correspond to a camera metadata file
    timestr_array = [
        f.name.split("_")[2].split(".")[0]
        for f in path.iterdir()
        if f.name.startswith("cam_metadata_") and f.name.endswith(".csv")
    ]

    # Initialize a DataFrame for the synched data between the camera and the Harp
    synched_data = pd.DataFrame(
        columns=np.array(["Timestamp", "DI3", "DIPort1", "FrameID", "GPIO"])
    )

    for timestr in timestr_array:
        events_path = path / "events" / timestr / "behavior"
        reader = harp.create_reader(events_path)

        strobe = reader.DigitalInputState.read(events_path / "behavior_32.bin")
        strobe = strobe[(~strobe["DI3"]) & (strobe["DI3"].shift(1))]
        strobe = strobe[["DI3", "DIPort1"]]
        timestamps = strobe.index.to_numpy()
        strobe = strobe.reset_index(drop=True)
        strobe["Timestamp"] = timestamps

        metadata = pd.read_csv(
            path / ("cam_metadata_" + timestr + ".csv"),
            header=None,
            names=["Timestamp", "FrameID", "GPIO"],
        )
        metadata["FrameID"] = metadata.index.to_numpy() + 1

        si_mask = (~strobe["DIPort1"]) & (strobe["DIPort1"].shift(1))
        strobe_index = strobe[si_mask].index.to_numpy()[-1]

        setup_path = path / "config" / ("setup_" + timestr + ".json")
        with open(setup_path, "r") as file:
            setup = json.load(file)

        if setup["camera"]["type"] == "FLIR":
            mi_mask = (metadata["GPIO"] == 12) & (metadata["GPIO"].shift(1) == 13)
        else:
            mi_mask = (metadata["GPIO"] == 805306368) & (
                metadata["GPIO"].shift(1) == 2952790016
            )
        metadata_index = metadata[mi_mask].index.to_numpy()[-1]

        sl_after = strobe.iloc[strobe_index:].shape[0]
        ml_after = metadata.iloc[metadata_index:].shape[0]
        zeros = np.zeros(max(0, ml_after - sl_after), dtype=int)
        pos_strobe = pd.DataFrame({"Timestamp": zeros, "FrameID": zeros, "GPIO": zeros})
        zeros = np.zeros(max(0, sl_after - ml_after), dtype=int)
        pos_metadata = pd.DataFrame(
            {"DI3": zeros, "DIPort1": zeros, "Timestamp": zeros}
        )

        sl_before = strobe.iloc[:strobe_index].shape[0]
        ml_before = metadata.iloc[:metadata_index].shape[0]
        zeros = np.zeros(max(0, ml_before - sl_before), dtype=int)
        pre_strobe = pd.DataFrame({"Timestamp": zeros, "FrameID": zeros, "GPIO": zeros})
        zeros = np.zeros(max(0, sl_before - ml_before), dtype=int)
        pre_metadata = pd.DataFrame(
            {"DI3": zeros, "DIPort1": zeros, "Timestamp": zeros}
        )

        strobe = pd.concat([pre_strobe, strobe, pos_strobe], ignore_index=True)
        metadata = pd.concat([pre_metadata, metadata, pos_metadata], ignore_index=True)

        df = pd.DataFrame(
            {
                "Timestamp": strobe["Timestamp"].to_numpy(),
                "DI3": strobe["DI3"].to_numpy(),
                "DIPort1": strobe["DIPort1"].to_numpy(),
                "FrameID": metadata["FrameID"].to_numpy(),
                "GPIO": metadata["GPIO"].to_numpy(),
            }
        )

        synched_data = pd.concat(
            [i.dropna(axis=1, how="all") for i in [synched_data, df]], ignore_index=True
        )

    return synched_data
