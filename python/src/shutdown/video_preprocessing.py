import os

import harp
import pandas as pd


def add_frame_numbers(out: pd.DataFrame, path):
    datestr = [
        f.split("_")[1].split(".")[0]
        for f in os.listdir(path)
        if f.startswith("cam_metadata_") and f.endswith(".csv")
    ]

    for date in datestr:
        events_path = path / "events" / date / "behavior"
        reader = harp.create_reader(events_path)

        strobe = reader.DigitalInputState.read(events_path / "behavior_32.bin")
        strobe = strobe[(not strobe["DI3"]) & (strobe["DI3"].shift(1))]
        strobe = strobe[["DI3", "DIPort1"]]

        metadata = pd.read_csv(
            path / ("cam_metadata_" + date + ".csv"),
            header=None,
            names=["Timestamp", "FrameID", "GPIO"],
        )

    # TODO: align the 2 dataframes and add None's for the rows that remain (in case of DataFrames of different sizes)

