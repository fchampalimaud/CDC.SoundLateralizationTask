import json
import os
from pathlib import Path

import harp
import numpy as np
import pandas as pd


def add_frame_numbers(out: pd.DataFrame, path):
    strobe = synch_camera(Path(path))

    strobe = strobe[strobe["Timestamp"] >= 0]
    df = pd.DataFrame(
        columns=np.array(
            [
                "trial_frame_start",
                "trial_frame_cnp",
                "trial_frame_rt",
                "trial_frame_mt",
            ]
        )
    )

    for i in range(out.shape[0]):
        row = out.iloc[i]
        ts_mask = strobe["Timestamp"] >= row["trial_start"]
        ts_frame = strobe.loc[ts_mask, "FrameID"].iloc[0]

        if np.isnan(row["cnp_start"]):
            cnp_frame = np.nan
        else:
            cnp_mask = strobe["Timestamp"] >= row["cnp_start"]
            cnp_frame = strobe.loc[cnp_mask, "FrameID"].iloc[0]

        if np.isnan(row["rt_start"]):
            rt_frame = np.nan
        else:
            rt_mask = strobe["Timestamp"] >= row["rt_start"]
            rt_frame = strobe.loc[rt_mask, "FrameID"].iloc[0]

        if np.isnan(row["mt_start"]):
            mt_frame = np.nan
        else:
            mt_mask = strobe["Timestamp"] >= row["mt_start"]
            mt_frame = strobe.loc[mt_mask, "FrameID"].iloc[0]

        new_row = pd.Series(
            [ts_frame, cnp_frame, rt_frame, mt_frame],
            index=[
                "trial_frame_start",
                "trial_frame_cnp",
                "trial_frame_rt",
                "trial_frame_mt",
            ],
        )

        df = df._append(new_row, ignore_index=True)

    final_out = pd.concat([out, df], axis=1)

    return final_out


def synch_camera(path):
    datestr = [
        f.split("_")[2].split(".")[0]
        for f in os.listdir(path)
        if f.startswith("cam_metadata_") and f.endswith(".csv")
    ]

    synched_data = pd.DataFrame(
        columns=np.array(["Timestamp", "DI3", "DIPort1", "FrameID", "GPIO"])
    )

    for date in datestr:
        events_path = path / "events" / date / "behavior"
        reader = harp.create_reader(events_path)

        strobe = reader.DigitalInputState.read(events_path / "behavior_32.bin")
        strobe = strobe[(strobe["DI3"] == False) & (strobe["DI3"].shift(1))]
        strobe = strobe[["DI3", "DIPort1"]]
        timestamps = strobe.index.to_numpy()
        strobe = strobe.reset_index(drop=True)
        strobe["Timestamp"] = timestamps

        metadata = pd.read_csv(
            path / ("cam_metadata_" + date + ".csv"),
            header=None,
            names=["Timestamp", "FrameID", "GPIO"],
        )
        metadata["FrameID"] -= metadata["FrameID"].to_numpy()[0] + 1

        si_mask = (strobe["DIPort1"]) & (strobe["DIPort1"].shift(1) == False)
        strobe_index = strobe[si_mask].index.to_numpy()[-1]

        setup_path = path / "config" / ("setup_" + date + ".json")
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
        if sl_after > ml_after:
            new_row = pd.Series([0, 0, 0], index=["Timestamp", "FrameID", "GPIO"])
            for i in range(sl_after - ml_after):
                metadata = metadata._append(new_row, ignore_index=True)
        elif sl_after < ml_after:
            new_row = pd.Series([0, 0, 0], index=["DI3", "DIPort1", "Timestamp"])
            for i in range(ml_after - sl_after):
                strobe = strobe._append(new_row, ignore_index=True)

        sl_before = strobe.iloc[:strobe_index].shape[0]
        ml_before = metadata.iloc[:metadata_index].shape[0]
        if sl_before > ml_before:
            new_row = pd.DataFrame({"Timestamp": [0], "FrameID": [0], "GPIO": [0]})
            for i in range(sl_before - ml_before):
                metadata = pd.concat([new_row, metadata], ignore_index=True)
        elif sl_before < ml_before:
            new_row = pd.DataFrame({"Timestamp": [0], "FrameID": [0], "GPIO": [0]})
            for i in range(ml_before - sl_before):
                strobe = pd.concat([new_row, strobe], ignore_index=True)

        df = pd.DataFrame(
            {
                "Timestamp": strobe["Timestamp"].to_numpy(),
                "DI3": strobe["DI3"].to_numpy(),
                "DIPort1": strobe["DIPort1"].to_numpy(),
                "FrameID": metadata["FrameID"].to_numpy(),
                "GPIO": metadata["GPIO"].to_numpy(),
            }
        )

        synched_data = pd.concat([synched_data, df], ignore_index=True)

    return synched_data
