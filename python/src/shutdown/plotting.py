import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import LogFormatter, MaxNLocator


class Plotting:
    def __init__(self):
        pass


TITLES = np.array(
    [
        ["", "ILD condition and t. outcome", "Outcome with abort tags"],
        [
            "Running average performance and abort rate",
            "Performance and abort rate for all ILD conditions",
            "Time to central nose poke",
        ],
        ["Reaction Time", "Movement time", ""],
    ]
)

XLABELS = np.array(
    [
        ["", "Trial", "Trial"],
        ["Trial", "ILD step", "Trial"],
        ["Trial", "Trial", ""],
    ]
)

YLABELS = np.array(
    [
        ["", "Left    ILD (dB SPL)    Right", "Outcome"],
        ["Proportion", "Proportion", "Time (s)"],
        ["Time (ms)", "Time (ms)", ""],
    ]
)


def generate_plots(data: pd.DataFrame, path):
    block_nums = data["block"].unique()

    for block_num in block_nums:
        df = data[data["block"] == block_num]

        fig, ax = plt.subplots(3, 3, figsize=(14, 10))
        plt.subplots_adjust(wspace=0.4, hspace=0.4)

        # Axes titles
        titles = np.array(
            [
                ["", "ILD condition and t. outcome", "Outcome with abort tags"],
                [
                    "Running average performance and abort rate",
                    "Performance and abort rate for all ILD conditions",
                    "Time to central nose poke",
                ],
                ["Reaction Time", "Movement time", ""],
            ]
        )
        # Axes x-labels
        xlabels = np.array(
            [
                ["", "Trial", "Trial"],
                ["Trial", "ILD step", "Trial"],
                ["Trial", "Trial", ""],
            ]
        )
        # Axes y-labels
        ylabels = np.array(
            [
                ["", "Left    ILD (dB SPL)    Right", "Outcome"],
                ["Proportion", "Proportion", "Time (s)"],
                ["Time (ms)", "Time (ms)", ""],
            ]
        )
        # Applies some configurations to the axes
        for i in range(3):
            for j in range(3):
                ax[i, j].set_title(titles[i, j], fontsize=8, fontweight="bold")
                ax[i, j].set_xlabel(xlabels[i, j], fontsize=8)
                ax[i, j].set_ylabel(ylabels[i, j], fontsize=8)
                ax[i, j].xaxis.set_major_locator(MaxNLocator(integer=True))
                ax[i, j].tick_params(axis="both", labelsize=8)

                if (i, j) in [(2, 2)]:
                    ax[i, j].axis("off")
                else:
                    # Hide the spines for the used subplots
                    ax[i, j].spines["top"].set_visible(False)
                    ax[i, j].spines["right"].set_visible(False)

        # Deletes ticks from first plot
        ax[0, 0].set_yticks([])
        ax[0, 0].set_xticks([])

        text = "Animal: " + df["animal"].to_numpy()[0] + "\n"
        text += "Batch: " + df["batch"].to_numpy()[0] + "\n"
        text += "Block: " + str(df["block"].to_numpy()[0]) + "\n"
        text += "Learning Stage: " + str(df["training_level"].to_numpy()[0]) + "\n"
        text += "Setup: " + str(df["box"].to_numpy()[0]) + "\n"

        # Informative text
        plt.text(
            ax[0, 0].get_position().x0 + 0.005,
            ax[0, 0].get_position().y0 + 0.06,
            text,
            transform=fig.transFigure,
            fontsize=8,
            linespacing=1.5,
        )

        # Changes the labels of the y-ticks in the outcome plot
        ax[0, 2].set_yticks(
            range(3, -9, -1),
            [
                "",
                "Trial +",
                "Trial -",
                "",
                "CNP",
                "Fixation",
                "RT+",
                "RT-",
                "MT+",
                "MT-",
                "LNP",
                "IO",
            ],
        )

        # Add horizontal lines in some plots
        ax[0, 1].axhline(y=0, color="black")
        ax[0, 2].axhline(y=0, color="black")
        ax[1, 1].axhline(y=0.5, color="black", linestyle=":")

        # Applies limits in the y-axis for some plots
        ax[0, 1].set_ylim(-60, 60)
        ax[0, 2].set_ylim(-9, 3)
        ax[1, 0].set_ylim(0, 1)
        ax[1, 1].set_ylim(0, 1)
        ax[1, 2].set_yscale("log")
        formatter = LogFormatter(base=10, labelOnlyBase=False)
        ax[1, 2].yaxis.set_minor_formatter(formatter)

        # ILD plot
        df2 = df[df["success"] == 1]
        ax[0, 1].plot(
            df2["trial"],
            df2["ILD"],
            "o",
            markerfacecolor="none",
            markeredgecolor="green",
            markeredgewidth=1.5,
        )
        df2 = df[df["success"] == -1]
        ax[0, 1].plot(
            df2["trial"],
            df2["ILD"],
            "o",
            markerfacecolor="none",
            markeredgecolor="red",
            markeredgewidth=1.5,
        )
        df2 = df[df["success"] == 0]
        ax[0, 1].plot(
            df2["trial"],
            df2["ILD"],
            "o",
            markerfacecolor="none",
            markeredgecolor="black",
            markeredgewidth=1.5,
        )
        ax[0, 1].set_ylim(-1.1 * max(np.abs(df["ILD"])), 1.1 * max(np.abs(df["ILD"])))

        colors_aborts = plt.cm.hsv(np.linspace(0.75, 0, 10))
        # Outcome plot
        df2 = df[(df["success"] == 1) & (df["ILD"] < 0)]
        ax[0, 2].plot(
            df2["trial"],
            2 * np.ones(df2.shape[0]),
            "<",
            markerfacecolor="none",
            markeredgecolor=colors_aborts[0],
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == 1) & (df["ILD"] > 0)]
        ax[0, 2].plot(
            df2["trial"],
            2 * np.ones(df2.shape[0]),
            ">",
            markerfacecolor="none",
            markeredgecolor=colors_aborts[0],
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == -1) & (df["ILD"] < 0)]
        ax[0, 2].plot(
            df2["trial"],
            np.ones(df2.shape[0]),
            "<",
            markerfacecolor="none",
            markeredgecolor=colors_aborts[1],
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == -1) & (df["ILD"] > 0)]
        ax[0, 2].plot(
            df2["trial"],
            np.ones(df2.shape[0]),
            ">",
            markerfacecolor="none",
            markeredgecolor=colors_aborts[1],
            markeredgewidth=1.5,
        )
        df2 = df[df["abort_type"] == "CNP"]
        ax[0, 2].plot(
            df2["trial"],
            -1 * np.ones(df2.shape[0]),
            "o",
            markerfacecolor="none",
            markeredgecolor=colors_aborts[2],
            markeredgewidth=1.5,
        )
        df2 = df[df["abort_type"] == "Fixation"]
        ax[0, 2].plot(
            df2["trial"],
            -2 * np.ones(df2.shape[0]),
            "o",
            markerfacecolor="none",
            markeredgecolor=colors_aborts[3],
            markeredgewidth=1.5,
        )
        df2 = df[df["abort_type"] == "RT+"]
        ax[0, 2].plot(
            df2["trial"],
            -3 * np.ones(df2.shape[0]),
            "o",
            markerfacecolor="none",
            markeredgecolor=colors_aborts[4],
            markeredgewidth=1.5,
        )
        df2 = df[df["abort_type"] == "RT-"]
        ax[0, 2].plot(
            df2["trial"],
            -4 * np.ones(df2.shape[0]),
            "o",
            markerfacecolor="none",
            markeredgecolor=colors_aborts[5],
            markeredgewidth=1.5,
        )
        df2 = df[df["abort_type"] == "MT+"]
        ax[0, 2].plot(
            df2["trial"],
            -5 * np.ones(df2.shape[0]),
            "o",
            markerfacecolor="none",
            markeredgecolor=colors_aborts[6],
            markeredgewidth=1.5,
        )
        df2 = df[df["abort_type"] == "MT-"]
        ax[0, 2].plot(
            df2["trial"],
            -6 * np.ones(df2.shape[0]),
            "o",
            markerfacecolor="none",
            markeredgecolor=colors_aborts[7],
            markeredgewidth=1.5,
        )
        df2 = df[df["abort_type"] == "LNP"]
        ax[0, 2].plot(
            df2["trial"],
            -7 * np.ones(df2.shape[0]),
            "o",
            markerfacecolor="none",
            markeredgecolor=colors_aborts[8],
            markeredgewidth=1.5,
        )
        df2 = df[df["abort_type"] == "IO"]
        ax[0, 2].plot(
            df2["trial"],
            -8 * np.ones(df2.shape[0]),
            "o",
            markerfacecolor="none",
            markeredgecolor=colors_aborts[9],
            markeredgewidth=1.5,
        )

        # Performance plot
        ax[1, 0].plot(
            df["trial"],
            df["block_perf"],
            "o",
            # markerfacecolor="none",
            markeredgecolor="green",
            markeredgewidth=1.5,
        )

        # Performance per ILD plot
        perf = get_performance_by_ild(df)
        ax[1, 1].plot(
            perf[:, 0],
            perf[:, 1],
            "o-",
            markerfacecolor="none",
            markeredgecolor="green",
            markeredgewidth=1.5,
            color="green",
        )
        ax[1, 1].plot(
            perf[:, 0],
            perf[:, 2],
            "o-",
            markerfacecolor="none",
            markeredgecolor="black",
            markeredgewidth=1.5,
            color="black",
        )

        # Time to CNP plot
        df2 = df[(df["success"] == 1) & (df["ILD"] < 0)]
        ax[1, 2].plot(
            df2["trial"],
            df2["cnp_time"],
            "<",
            markerfacecolor="none",
            markeredgecolor="green",
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == 1) & (df["ILD"] > 0)]
        ax[1, 2].plot(
            df2["trial"],
            df2["cnp_time"],
            ">",
            markerfacecolor="none",
            markeredgecolor="green",
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == -1) & (df["ILD"] < 0)]
        ax[1, 2].plot(
            df2["trial"],
            df2["cnp_time"],
            "<",
            markerfacecolor="none",
            markeredgecolor="red",
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == -1) & (df["ILD"] > 0)]
        ax[1, 2].plot(
            df2["trial"],
            df2["cnp_time"],
            ">",
            markerfacecolor="none",
            markeredgecolor="red",
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == 0)]
        ax[1, 2].plot(
            df2["trial"],
            df2["cnp_time"],
            "o",
            markerfacecolor="none",
            markeredgecolor="black",
            markeredgewidth=1.5,
        )
        # ax[1, 2].set_ylim(0.9 * min(df["cnp_time"]), 1.1 * max(df["cnp_time"]))

        # Reaction time plot
        df2 = df[(df["success"] == 1) & (df["ILD"] < 0)]
        ax[2, 0].plot(
            df2["trial"],
            df2["timed_rt"] * 1000,
            "<",
            markerfacecolor="none",
            markeredgecolor="green",
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == 1) & (df["ILD"] > 0)]
        ax[2, 0].plot(
            df2["trial"],
            df2["timed_rt"] * 1000,
            ">",
            markerfacecolor="none",
            markeredgecolor="green",
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == -1) & (df["ILD"] < 0)]
        ax[2, 0].plot(
            df2["trial"],
            df2["timed_rt"] * 1000,
            "<",
            markerfacecolor="none",
            markeredgecolor="red",
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == -1) & (df["ILD"] > 0)]
        ax[2, 0].plot(
            df2["trial"],
            df2["timed_rt"] * 1000,
            ">",
            markerfacecolor="none",
            markeredgecolor="red",
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == 0)]
        ax[2, 0].plot(
            df2["trial"],
            df2["timed_rt"] * 1000,
            "o",
            markerfacecolor="none",
            markeredgecolor="black",
            markeredgewidth=1.5,
        )

        # Movement time plot
        df2 = df[(df["success"] == 1) & (df["ILD"] < 0)]
        ax[2, 1].plot(
            df2["trial"],
            df2["timed_mt"] * 1000,
            "<",
            markerfacecolor="none",
            markeredgecolor="green",
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == 1) & (df["ILD"] > 0)]
        ax[2, 1].plot(
            df2["trial"],
            df2["timed_mt"] * 1000,
            ">",
            markerfacecolor="none",
            markeredgecolor="green",
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == -1) & (df["ILD"] < 0)]
        ax[2, 1].plot(
            df2["trial"],
            df2["timed_mt"] * 1000,
            "<",
            markerfacecolor="none",
            markeredgecolor="red",
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == -1) & (df["ILD"] > 0)]
        ax[2, 1].plot(
            df2["trial"],
            df2["timed_mt"] * 1000,
            ">",
            markerfacecolor="none",
            markeredgecolor="red",
            markeredgewidth=1.5,
        )
        df2 = df[(df["success"] == 0)]
        ax[2, 1].plot(
            df2["trial"],
            df2["timed_mt"] * 1000,
            "o",
            markerfacecolor="none",
            markeredgecolor="black",
            markeredgewidth=1.5,
        )

        fig_path = os.path.join(path, f"block_{block_num}.png")
        fig.savefig(fig_path)


def get_performance_by_ild(df):
    ilds = np.sort(df["ILD"].unique())
    array = np.zeros((ilds.size, 3))

    for i in range(ilds.size):
        df2 = df[df["ILD"] == ilds[i]]
        array[i, 0] = ilds[i]
        array[i, 2] = df2[df2["success"] == 0].shape[0] / float(df2.shape[0])
        try:
            array[i, 1] = (
                float(df2[df2["success"] == 1].shape[0])
                / df2[(df2["success"] == 1) | (df2["success"] == -1)].shape[0]
            )
        except:
            array[i, 1] = 0

    return array
