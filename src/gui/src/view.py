import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.ticker import MaxNLocator

class View():
    def __init__(self, callbacks: list):
        self.fig, self.ax = plt.subplots(3, 3, figsize=(14, 10))
        plt.subplots_adjust(wspace=0.4, hspace=0.4)

        titles = np.array([["", "ILD condition and t. outcome", "Outcome with abort tags"], ["Running average performance and abort rate", "Performance and abort rate for all ILD conditions", "Time to central nose poke"], ["Reaction Time", "Movement time", ""]])
        xlabels = np.array([["", "Trial", "Trial"], ["Trial", "ILD step", "Trial"], ["Trial", "Trial", ""]])
        ylabels = np.array([["", "Left    ILD (dB SPL)    Right", "Outcome"], ["Proportion", "Proportion", "log Time (s)"], ["Time (ms)", "Time (ms)", ""]])
        for i in range(3):
            for j in range(3):
                self.ax[i, j].set_title(titles[i, j], fontsize = 8, fontweight="bold")
                self.ax[i, j].set_xlabel(xlabels[i, j], fontsize = 8)
                self.ax[i, j].set_ylabel(ylabels[i, j], fontsize = 8)
                self.ax[i, j].xaxis.set_major_locator(MaxNLocator(integer=True))
                self.ax[i, j].tick_params(axis="both", labelsize=8)

                if (i, j) in [(2, 2)]:
                    self.ax[i, j].axis('off')
                else:
                    # Hide the spines for the used subplots
                    self.ax[i, j].spines['top'].set_visible(False)
                    self.ax[i, j].spines['right'].set_visible(False)

        self.ax[0, 0].set_yticks([])
        self.ax[0, 0].set_xticks([])

        self.ax[0, 2].set_yticks(range(2, -8, -1), ['Trial +', 'Trial -', '', 'CNP', 'CNP fix', 'RT', 'MT+', 'MT-', 'LNP fix', 'IO crash'])

        self.ax[0, 1].axhline(y = 0, color='black')
        self.ax[0, 2].axhline(y = 0, color='black')
        self.ax[1, 1].axhline(y = 0.5, color='black', linestyle = ':')

        self.ax[0, 1].set_ylim(-60, 60)
        self.ax[0, 2].set_ylim(-8, 2)
        self.ax[1, 0].set_ylim(0, 1)
        self.ax[1, 1].set_ylim(0, 1)

        self.plots = np.zeros((3, 3), dtype=np.ndarray)

        colors_outcome = ["green", "red", "black"]
        self.plots[0, 1] = np.array([PlotStruct() for i in range(3)])
        for i in range(self.plots[0, 1].size):
            self.plots[0, 1][i].plot, = self.ax[0, 1].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_outcome[i], markeredgewidth=1.5)

        colors_aborts = plt.cm.hsv(np.linspace(0.75, 0, 9))
        self.plots[0, 2] = np.array([PlotStruct() for i in range(11)])
        self.plots[0, 2][0].plot, = self.ax[0, 2].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_aborts[0], markeredgewidth=1.5)
        self.plots[0, 2][1].plot, = self.ax[0, 2].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_aborts[0], markeredgewidth=1.5)
        self.plots[0, 2][2].plot, = self.ax[0, 2].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_aborts[1], markeredgewidth=1.5)
        self.plots[0, 2][3].plot, = self.ax[0, 2].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_aborts[1], markeredgewidth=1.5)
        for i in range(4, self.plots[0, 2].size):
            self.plots[0, 2][i].plot, = self.ax[0, 2].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_aborts[i - 2], markeredgewidth=1.5)

        self.plots[1, 0] = np.array([PlotStruct() for i in range(3)])
        self.plots[1, 0][0].plot, = self.ax[1, 0].plot([], [], 'o', color="grey", markeredgewidth=1.5)
        self.plots[1, 0][1].plot, = self.ax[1, 0].plot([], [], '.', color=colors_outcome[0], markeredgewidth=1.5)
        self.plots[1, 0][2].plot, = self.ax[1, 0].plot([], [], '.', color=colors_outcome[2], markeredgewidth=1.5)
        
        self.plots[1, 1] = np.array([PlotStruct() for i in range(2)])
        self.plots[1, 1][0].plot, = self.ax[1, 1].plot([], [], 'o-', markerfacecolor='none', color=colors_outcome[0], markeredgewidth=1.5)
        self.plots[1, 1][1].plot, = self.ax[1, 1].plot([], [], 'o-', markerfacecolor='none', color=colors_outcome[2], markeredgewidth=1.5)
        
        self.plots[1, 2] = np.array([PlotStruct() for i in range(5)])
        self.plots[1, 2][0].plot, = self.ax[1, 2].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[1, 2][1].plot, = self.ax[1, 2].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[1, 2][2].plot, = self.ax[1, 2].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[1, 2][3].plot, = self.ax[1, 2].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[1, 2][4].plot, = self.ax[1, 2].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_outcome[2], markeredgewidth=1.5)
        
        self.plots[2, 0] = np.array([PlotStruct() for i in range(5)])
        self.plots[2, 0][0].plot, = self.ax[2, 0].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[2, 0][1].plot, = self.ax[2, 0].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[2, 0][2].plot, = self.ax[2, 0].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[2, 0][3].plot, = self.ax[2, 0].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[2, 0][4].plot, = self.ax[2, 0].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_outcome[2], markeredgewidth=1.5)
        
        self.plots[2, 1] = np.array([PlotStruct() for i in range(5)])
        self.plots[2, 1][0].plot, = self.ax[2, 1].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[2, 1][1].plot, = self.ax[2, 1].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[2, 1][2].plot, = self.ax[2, 1].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[2, 1][3].plot, = self.ax[2, 1].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[2, 1][4].plot, = self.ax[2, 1].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_outcome[2], markeredgewidth=1.5)

        # Display buttons
        button_ax = np.zeros(6, dtype=object)
        self.buttons = np.zeros(6, dtype=object)
        button_labels = ["Next trial left", " Next trial right", "Reward left", "Reward right", "Repeat errors", "Stop session"]
        button_ypos = [0.25, 0.25, 0.2, 0.2, 0.15, 0.15]
        for i in range(6):
            if i % 2 != 0:
                x = 0.8
            else:
                x = 0.69
            button_ax[i] = self.fig.add_axes([x, button_ypos[i], 0.1, 0.03])
            self.buttons[i] = Button(button_ax[i], button_labels[i], hovercolor='0.975')
            self.buttons[i].label.set_fontsize(9)
            self.buttons[i].on_clicked(callbacks[i])
        # buttons[0].on_clicked(self.hell)

        self.text = plt.text(self.ax[0, 0].get_position().x0 + 0.005, self.ax[0, 0].get_position().y0 + 0.01, "", transform=self.fig.transFigure, fontsize = 8, linespacing = 1.5)

    def show(self):
        plt.show()

class PlotStruct:
    def __init__(self, plot = None):
        self.x = []
        self.y = []
        self.plot = plot

    def update(self):
        if self.plot is not None:
            self.plot.set_xdata(self.x)
            self.plot.set_ydata(self.y)

    def add_data(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.update()

    def reset(self):
        self.x = []
        self.y = []
        self.update()