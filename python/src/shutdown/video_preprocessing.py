from pathlib import Path

import harp
import numpy as np
import pandas as pd


def add_frame_numbers(out: pd.DataFrame, path: Path, time_str: str):
    """
    Adds the frame numbers to the out structure for the following events: trial start, CNP start, sound (RT) start, MT start and MT end (or LNP start)

    Parameters
    ----------
    out : pd.DataFrame
        the out DataFrame structure without the frame data
    path : Path
        the path to the camera metadata file
    time_str : str
        the string of the time the session began in the "hhmmss" format

    Returns
    -------
    pd.DataFrame
        the final out DataFrame structure
    """
    # Synchronize the camera frames with the Harp timestamps
    strobe = synch_camera(path, time_str)
    strobe = strobe[strobe["Timestamp"] >= 0]

    # Create a temporary copy of the out structure
    temp_out = out.copy()

    # Convert the type of the relevant columns to float
    temp_out["trial_start"] = temp_out["trial_start"].astype(float)
    temp_out["cnp_start"] = temp_out["cnp_start"].astype(float)
    temp_out["rt_start"] = temp_out["rt_start"].astype(float)
    temp_out["mt_start"] = temp_out["mt_start"].astype(float)
    temp_out["lnp_start"] = temp_out["lnp_start"].astype(float)

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
            left=temp_out[(temp_out["lnp_start"].notna())],
            right=strobe,
            left_on="lnp_start",
            right_on="Timestamp",
            direction="forward",
        )
        df = df.rename(columns={"FrameID": "lnp_start_frame"})
        df = df[["trial", "lnp_start_frame"]]
        out = out.merge(df, how="left", on="trial")
    except Exception:
        print("It was not possible to add the lnp_start_frame column")

    return out


def synch_camera(path: Path, time_str: str):
    """
    Synchronizes the camera data with the Harp timestamps.

    Parameters
    ----------
    path : Path
        the path to the camera metadata file
    time_str : str
        the string of the time the session began in the "hhmmss" format

    Returns
    -------
    pd.DataFrame
        a pandas DataFrame containing a Harp timestamp for every frame, as well as the state of the camera GPIOs and the relevant Harp Behavior GPIOs
    """
    # for timestr in timestr_array:
    events_path = path / "events" / time_str / "behavior"
    reader = harp.create_reader(events_path)

    strobe = reader.DigitalInputState.read(events_path / "behavior_32.bin")
    strobe = strobe[(~strobe["DI3"]) & (strobe["DI3"].shift(1))]
    strobe = strobe[["DI3", "DIPort1"]]
    timestamps = strobe.index.to_numpy()
    strobe = strobe.reset_index(drop=True)
    strobe["Timestamp"] = timestamps

    metadata = pd.read_csv(
        path / ("cam_metadata_" + time_str + ".csv"),
        header=None,
        names=["Timestamp", "FrameID", "GPIO"],
    )
    metadata["FrameID"] = metadata.index.to_numpy() + 1

    # FIXME: there's an edge case that is not being dealt with when the animal never pokes in the central port
    si_mask = (~strobe["DIPort1"]) & (strobe["DIPort1"].shift(1))
    strobe_index = strobe[si_mask].index.to_numpy()[0]

    # Check the state of the camera GPIO0 (0x1)
    mi_mask = (~(metadata["GPIO"].fillna(-1).astype(int) & 0x1)) & (
        metadata["GPIO"].shift(1).fillna(-1).astype(int) & 0x1
    )
    metadata_index = metadata[mi_mask.astype(bool)].index.to_numpy()[0]

    sl_after = strobe.iloc[strobe_index:].shape[0]
    ml_after = metadata.iloc[metadata_index:].shape[0]
    if (sl_after - ml_after) > 0:
        strobe = strobe.iloc[: -(sl_after - ml_after)]
    elif (ml_after - sl_after) > 0:
        metadata = metadata.iloc[: -(ml_after - sl_after)]

    sl_before = strobe.iloc[:strobe_index].shape[0]
    ml_before = metadata.iloc[:metadata_index].shape[0]
    zeros = np.zeros(max(0, ml_before - sl_before), dtype=int)
    pre_strobe = pd.DataFrame({"Timestamp": zeros, "FrameID": zeros, "GPIO": zeros})
    zeros = np.zeros(max(0, sl_before - ml_before), dtype=int)
    pre_metadata = pd.DataFrame({"DI3": zeros, "DIPort1": zeros, "Timestamp": zeros})

    strobe = pd.concat([pre_strobe, strobe], ignore_index=True)
    metadata = pd.concat([pre_metadata, metadata], ignore_index=True)

    synched_data = pd.DataFrame(
        {
            "Timestamp": strobe["Timestamp"].to_numpy(),
            "DI3": strobe["DI3"].to_numpy(),
            "DIPort1": strobe["DIPort1"].to_numpy(),
            "FrameID": metadata["FrameID"].to_numpy(),
            "GPIO": metadata["GPIO"].to_numpy(),
        }
    )

    return synched_data
