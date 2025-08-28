import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import LogFormatter, MaxNLocator


def _apply_common_axis_style(
    ax,
    title="",
    xlabel="",
    ylabel="",
    fontsize=8,
    hide_spines=True,
    integer_x=True,
    tick_labelsize=8,
    hide_ticks=False,
    yscale=None,
    ylim=None,
    hline=None,
):
    """
    Apply common styling to a single axis.
    - title/xlabel/ylabel/fontsize: text formatting
    - hide_spines: remove top/right spines (keeps left/bottom)
    - integer_x: use integer locator on x axis
    - hide_ticks: remove both x and y ticks (used for the info cell)
    - yscale: 'log' or None
    - ylim: tuple for y-limits
    - hline: dict like {'y': value, 'color': 'black', 'linestyle': ':'}
    """
    ax.set_title(title, fontsize=fontsize, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    if integer_x:
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.tick_params(axis="both", labelsize=tick_labelsize)

    if hide_ticks:
        ax.set_yticks([])
        ax.set_xticks([])

    if hide_spines:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    if yscale == "log":
        ax.set_yscale("log")
        # Keep minor ticks readable on log scale using LogFormatter
        formatter = LogFormatter(base=10, labelOnlyBase=False)
        ax.yaxis.set_minor_formatter(formatter)

    if ylim is not None:
        ax.set_ylim(*ylim)

    if hline is not None:
        # plot horizontal line if requested
        ax.axhline(
            y=hline.get("y", 0),
            color=hline.get("color", "black"),
            linestyle=hline.get("linestyle", "-"),
        )


def _scatter_by_conditions(ax, df, x_col, y_col, combos, y_mult=1.0, markerface="none"):
    """
    Generic scatter helper to plot multiple condition combos on the same axes.
    - combos: list of dicts with keys:
        - 'mask': boolean mask (same length as df) OR callable(df)->mask
        - 'marker': marker symbol
        - 'edgecolor': color
        - 'edgewidth': linewidth (optional, default 1.5)
        - 'y_const': if provided, plot a constant y value instead of y_col (useful for outcome panel)
        - 'mult': multiplier for y values (overrides y_mult for that combo)
    """
    for c in combos:
        # derive boolean mask
        mask = c["mask"](df) if callable(c["mask"]) else c["mask"]
        if mask.sum() == 0:
            continue

        edgewidth = c.get("edgewidth", 1.5)
        mult = c.get("mult", y_mult)

        if "y_const" in c:
            yvals = np.full(mask.sum(), c["y_const"])
        else:
            yvals = df.loc[mask, y_col] * mult

        ax.plot(
            df.loc[mask, x_col],
            yvals,
            c.get("marker", "o"),
            markerfacecolor=markerface,
            markeredgecolor=c.get("edgecolor", "black"),
            markeredgewidth=edgewidth,
        )


def _build_text_block(df):
    """
    Build the top-left info text block used in the first subplot.
    """
    # take first row values for textual metadata
    animal = df["animal"].to_numpy()[0]
    batch = df["batch"].to_numpy()[0]
    block = df["block"].to_numpy()[0]
    level = df["training_level"].to_numpy()[0]
    box = df["box"].to_numpy()[0]

    txt = f"Animal: {animal}\nBatch: {batch}\nBlock: {block}\nLearning Stage: {level}\nSetup: {box}\n"
    return txt


def generate_plots(data: pd.DataFrame, path):
    """
    Refactored plotting function that produces the same 3x3 layout per block
    but with much less repeated code. Save each block to path/block_<n>.png
    """
    # Precompute and map some commonly used items to avoid recomputing repeatedly.
    colors_success = {
        1: "green",
        -1: "red",
        0: "black",
    }

    # colors for abort types (preserve approximate mapping to your original HSV)
    abort_types = ["CNP", "Fixation", "RT+", "RT-", "MT+", "MT-", "LNP", "IO"]
    colors_aborts = plt.cm.hsv(np.linspace(0.75, 0, len(abort_types) + 2))

    # Multiply times once (avoid repeated multiplications in loops)
    data = data.copy()
    data["timed_rt_ms"] = data["timed_rt"] * 1000
    data["timed_mt_ms"] = data["timed_mt"] * 1000

    block_nums = data["block"].unique()

    for block_num in block_nums:
        df = data[data["block"] == block_num]

        # Create figure and 3x3 axes
        fig, ax = plt.subplots(3, 3, figsize=(14, 10))
        plt.subplots_adjust(wspace=0.4, hspace=0.4)

        # Titles/labels arrays (kept from original)
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
        xlabels = np.array(
            [
                ["", "Trial", "Trial"],
                ["Trial", "ILD step", "Trial"],
                ["Trial", "Trial", ""],
            ]
        )
        ylabels = np.array(
            [
                ["", "Left    ILD (dB SPL)    Right", "Outcome"],
                ["Proportion", "Proportion", "Time (s)"],
                ["Time (ms)", "Time (ms)", ""],
            ]
        )

        # Apply styles and metadata for each axis using the helper
        for i in range(3):
            for j in range(3):
                hide_ticks = i == 0 and j == 0  # top-left cell used for text
                # The bottom-right (2,2) is turned off in original
                if (i, j) == (2, 2):
                    ax[i, j].axis("off")
                    continue

                # Set axis properties (including special yscale/ylim/hlines for certain cells)
                yscale = None
                ylim = None
                hline = None
                if (i, j) == (0, 1):
                    ylim = (-1.1 * max(np.abs(df["ILD"])), 1.1 * max(np.abs(df["ILD"])))
                    hline = {"y": 0, "color": "black"}
                elif (i, j) == (0, 2):
                    ylim = (-9, 3)
                    hline = {"y": 0, "color": "black"}
                elif (i, j) == (1, 1):
                    ylim = (0, 1)
                    hline = {"y": 0.5, "color": "black", "linestyle": ":"}
                elif (i, j) == (1, 2):
                    # Time to CNP uses log scale in your original code
                    yscale = "log"
                elif (i, j) == (1, 0):
                    ylim = (0, 1)
                elif (i, j) == (2, 0) or (i, j) == (2, 1):
                    # Reaction and movement time panels will be in ms; no special ylim set
                    pass

                _apply_common_axis_style(
                    ax[i, j],
                    title=titles[i, j],
                    xlabel=xlabels[i, j],
                    ylabel=ylabels[i, j],
                    hide_spines=True,
                    hide_ticks=hide_ticks,
                    yscale=yscale,
                    ylim=ylim,
                    hline=hline,
                )

        # Add informative text in top-left cell position (uses figure coordinates)
        info_text = _build_text_block(df)
        plt.text(
            ax[0, 0].get_position().x0 + 0.005,
            ax[0, 0].get_position().y0 + 0.06,
            info_text,
            transform=fig.transFigure,
            fontsize=8,
            linespacing=1.5,
        )

        # ------- Panel (0,1): ILD condition and trial outcome markers -------
        # For ILD we plot three success categories with different edge colors
        combos_ild = []
        for succ_val, color in colors_success.items():
            combos_ild.append(
                {
                    "mask": df["success"] == succ_val,
                    "marker": "o",
                    "edgecolor": color,
                    "edgewidth": 1.5,
                }
            )
        _scatter_by_conditions(
            ax[0, 1], df, x_col="trial", y_col="ILD", combos=combos_ild
        )

        # ------- Panel (0,2): Outcome with abort tags -------
        # Build combos for success & ILD sign using left "<" and right ">" markers and two levels (success:1, -1)
        outcome_combos = []
        # Success correct (1): left if ILD<0, right if ILD>0 (use same color)
        outcome_combos.append(
            {
                "mask": (df["success"] == 1) & (df["ILD"] < 0),
                "marker": "<",
                "edgecolor": colors_aborts[0],
                "y_const": 2,
            }
        )
        outcome_combos.append(
            {
                "mask": (df["success"] == 1) & (df["ILD"] > 0),
                "marker": ">",
                "edgecolor": colors_aborts[0],
                "y_const": 2,
            }
        )
        # Incorrect (-1)
        outcome_combos.append(
            {
                "mask": (df["success"] == -1) & (df["ILD"] < 0),
                "marker": "<",
                "edgecolor": colors_aborts[1],
                "y_const": 1,
            }
        )
        outcome_combos.append(
            {
                "mask": (df["success"] == -1) & (df["ILD"] > 0),
                "marker": ">",
                "edgecolor": colors_aborts[1],
                "y_const": 1,
            }
        )

        # Add abort type markers at fixed negative y positions (matching original mapping)
        for idx, atype in enumerate(abort_types):
            y_const = -(idx + 1)  # maps CNP->-1, Fixation->-2, ...
            color = colors_aborts[idx + 2]
            outcome_combos.append(
                {
                    "mask": df["abort_type"] == atype,
                    "marker": "o",
                    "edgecolor": color,
                    "y_const": y_const,
                }
            )

        _scatter_by_conditions(
            ax[0, 2], df, x_col="trial", y_col="trial", combos=outcome_combos
        )

        # Adjust explicit y-ticks labels for outcome panel to match original mapping
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

        # ------- Panel (1,0): Running average performance (block_perf vs trial) -------
        perf_combo = [
            {
                "mask": np.ones(df.shape[0], dtype=bool),
                "marker": "o",
                "edgecolor": "green",
                "edgewidth": 1.5,
            }
        ]
        _scatter_by_conditions(
            ax[1, 0], df, x_col="trial", y_col="block_perf", combos=perf_combo
        )

        # ------- Panel (1,1): Performance per ILD (calls get_performance_by_ild) -------
        perf = get_performance_by_ild(
            df
        )  # expected shape (n_steps, 3): [ild, perf_correct, perf_total?]
        # Plot perf[:,1] and perf[:,2] as in original
        if perf is not None and perf.size:
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

        # ------- Panel (1,2): Time to central nose poke (cnp_time) -------
        # Use the same pattern as ILD/time panels: different markers for success/ILD sign
        cnp_combos = []
        cnp_combos.append(
            {
                "mask": (df["success"] == 1) & (df["ILD"] < 0),
                "marker": "<",
                "edgecolor": "green",
            }
        )
        cnp_combos.append(
            {
                "mask": (df["success"] == 1) & (df["ILD"] > 0),
                "marker": ">",
                "edgecolor": "green",
            }
        )
        cnp_combos.append(
            {
                "mask": (df["success"] == -1) & (df["ILD"] < 0),
                "marker": "<",
                "edgecolor": "red",
            }
        )
        cnp_combos.append(
            {
                "mask": (df["success"] == -1) & (df["ILD"] > 0),
                "marker": ">",
                "edgecolor": "red",
            }
        )
        cnp_combos.append(
            {"mask": (df["success"] == 0), "marker": "o", "edgecolor": "black"}
        )
        _scatter_by_conditions(
            ax[1, 2], df, x_col="trial", y_col="cnp_time", combos=cnp_combos
        )

        # ------- Panel (2,0): Reaction time (timed_rt_ms) -------
        rt_combos = []
        rt_combos.append(
            {
                "mask": (df["success"] == 1) & (df["ILD"] < 0),
                "marker": "<",
                "edgecolor": "green",
            }
        )
        rt_combos.append(
            {
                "mask": (df["success"] == 1) & (df["ILD"] > 0),
                "marker": ">",
                "edgecolor": "green",
            }
        )
        rt_combos.append(
            {
                "mask": (df["success"] == -1) & (df["ILD"] < 0),
                "marker": "<",
                "edgecolor": "red",
            }
        )
        rt_combos.append(
            {
                "mask": (df["success"] == -1) & (df["ILD"] > 0),
                "marker": ">",
                "edgecolor": "red",
            }
        )
        rt_combos.append(
            {"mask": (df["success"] == 0), "marker": "o", "edgecolor": "black"}
        )
        _scatter_by_conditions(
            ax[2, 0], df, x_col="trial", y_col="timed_rt_ms", combos=rt_combos
        )

        # ------- Panel (2,1): Movement time (timed_mt_ms) -------
        mt_combos = []
        mt_combos.append(
            {
                "mask": (df["success"] == 1) & (df["ILD"] < 0),
                "marker": "<",
                "edgecolor": "green",
            }
        )
        mt_combos.append(
            {
                "mask": (df["success"] == 1) & (df["ILD"] > 0),
                "marker": ">",
                "edgecolor": "green",
            }
        )
        mt_combos.append(
            {
                "mask": (df["success"] == -1) & (df["ILD"] < 0),
                "marker": "<",
                "edgecolor": "red",
            }
        )
        mt_combos.append(
            {
                "mask": (df["success"] == -1) & (df["ILD"] > 0),
                "marker": ">",
                "edgecolor": "red",
            }
        )
        mt_combos.append(
            {"mask": (df["success"] == 0), "marker": "o", "edgecolor": "black"}
        )
        _scatter_by_conditions(
            ax[2, 1], df, x_col="trial", y_col="timed_mt_ms", combos=mt_combos
        )

        # Save figure
        fig_path = os.path.join(path, f"block_{block_num}.png")
        fig.savefig(fig_path)
        plt.close(fig)  # close to free memory


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
        except Exception:
            array[i, 1] = 0

    return array
