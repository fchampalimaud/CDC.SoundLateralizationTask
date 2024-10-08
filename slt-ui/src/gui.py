import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

fig, ax = plt.subplots(3, 3)

ax[0, 0].axis('off')
ax[2, 2].axis('off')

titles = np.array([["", "ILD condition and t. outcome", "Outcome with abort tags"], ["Running average performance and abort rate", "Performance and abort rate for all ILD conditions", "Time to central nose poke"], ["Reaction Time", "Movement time", ""]])
xlabels = np.array([["", "Trial", "Trial"], ["Trial", "ILD step", "Trial"], ["Trial", "Trial", ""]])
ylabels = np.array([["", "Left    ILD (dB SPL)    Right", "Outcome"], ["Proportion", "Proportion", "log Time (s)"], ["Time (ms)", "Time (ms)", ""]])
for i in range(3):
    for j in range(3):
        ax[i, j].set_title(titles[i, j])
        ax[i, j].set_ylabel(ylabels[i, j])
        ax[i, j].xaxis.set_major_locator(MaxNLocator(integer=True))

        if (i, j) in [(0, 0), (2, 2)]:
            ax[i, j].axis('off')  # Turn off the axis for unused subplots
        else:
            # Hide the spines for the used subplots
            ax[i, j].spines['top'].set_visible(False)
            ax[i, j].spines['right'].set_visible(False)

ax[0, 2].set_yticks(range(10, 0, -1), ['Trial +', 'Trial -', '', 'CNP', 'CNP fix', 'RT', 'MT+', 'MT-', 'LNP fix', 'IO crash'])

ax[0, 1].axhline(y = 0, color='black')
ax[0, 2].axhline(y = 8, color='black')
ax[1, 1].axhline(y = 0.5, color='black', linestyle = ':')

ax[0, 1].set_ylim(-60, 60)
ax[0, 2].set_ylim(0, 10)
ax[1, 0].set_ylim(0, 1)
ax[1, 1].set_ylim(0, 1)

# Plot
ax[0, 2].scatter(2, 5)

ax[0, 2].set_xlim(left=0)

plt.show()