import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.ticker import MaxNLocator

class View():
    """
    A class that connects the matplotlib figure to the Python-side OSC server and client.

    Attributes
    ----------
    fig : matplotlib.figure.Figure
        the matplotlib figure object.
    ax : numpy.ndarray
        an array containing the 9 main axes that compose the figure.
    plots : numpy.ndarray
        an array containing 9 arrays containing the PlotStruct instances that compose each of the axes.
    buttons : numpy.ndarray
        an array containing the buttons that are part of the figure.
    text : matplotlib.text.Text
        the text object that will present informative text in the figure.
    """
    def __init__(self, callbacks: list):
        # Creation of the figure
        self.fig, self.ax = plt.subplots(3, 3, figsize=(14, 10))
        # Increase the space between subplots
        plt.subplots_adjust(wspace=0.4, hspace=0.4)

        # Axes titles
        titles = np.array([["", "ILD condition and t. outcome", "Outcome with abort tags"], ["Running average performance and abort rate", "Performance and abort rate for all ILD conditions", "Time to central nose poke"], ["Reaction Time", "Movement time", ""]])
        # Axes x-labels
        xlabels = np.array([["", "Trial", "Trial"], ["Trial", "ILD step", "Trial"], ["Trial", "Trial", ""]])
        # Axes y-labels
        ylabels = np.array([["", "Left    ILD (dB SPL)    Right", "Outcome"], ["Proportion", "Proportion", "log Time (s)"], ["Time (ms)", "Time (ms)", ""]])
        # Applies some configurations to the axes
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

        # Deletes ticks from first plot
        self.ax[0, 0].set_yticks([])
        self.ax[0, 0].set_xticks([])

        # Changes the labels of the y-ticks in the outcome plot
        self.ax[0, 2].set_yticks(range(3, -8, -1), ['', 'Trial +', 'Trial -', '', 'CNP', 'CNP fix', 'RT', 'MT+', 'MT-', 'LNP fix', 'IO crash'])

        # Add horizontal lines in some plots
        self.ax[0, 1].axhline(y = 0, color='black')
        self.ax[0, 2].axhline(y = 0, color='black')
        self.ax[1, 1].axhline(y = 0.5, color='black', linestyle = ':')

        # Applies limits in the y-axis for some plots
        self.ax[0, 1].set_ylim(-60, 60)
        self.ax[0, 2].set_ylim(-8, 3)
        self.ax[1, 0].set_ylim(0, 1)
        self.ax[1, 1].set_ylim(0, 1)

        # Initialization of the plots array
        self.plots = np.zeros((3, 3), dtype=np.ndarray)

        # List with colors for outcome
        colors_outcome = ["green", "red", "black"]
        # Initialization of the plots for the ILD axes
        self.plots[0, 1] = np.array([PlotStruct() for i in range(3)])
        for i in range(self.plots[0, 1].size):
            self.plots[0, 1][i].plot, = self.ax[0, 1].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_outcome[i], markeredgewidth=1.5)

        colors_aborts = plt.cm.hsv(np.linspace(0.75, 0, 9))
        # Initialization of the plots for the outcome axes
        self.plots[0, 2] = np.array([PlotStruct() for i in range(11)])
        self.plots[0, 2][0].plot, = self.ax[0, 2].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_aborts[0], markeredgewidth=1.5)
        self.plots[0, 2][1].plot, = self.ax[0, 2].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_aborts[0], markeredgewidth=1.5)
        self.plots[0, 2][2].plot, = self.ax[0, 2].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_aborts[1], markeredgewidth=1.5)
        self.plots[0, 2][3].plot, = self.ax[0, 2].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_aborts[1], markeredgewidth=1.5)
        for i in range(4, self.plots[0, 2].size):
            self.plots[0, 2][i].plot, = self.ax[0, 2].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_aborts[i - 2], markeredgewidth=1.5)

        # Initialization of the plots for the performance axes
        self.plots[1, 0] = np.array([PlotStruct() for i in range(3)])
        self.plots[1, 0][0].plot, = self.ax[1, 0].plot([], [], 'o', color="grey", markeredgewidth=1.5)
        self.plots[1, 0][1].plot, = self.ax[1, 0].plot([], [], '.', color=colors_outcome[0], markeredgewidth=1.5)
        self.plots[1, 0][2].plot, = self.ax[1, 0].plot([], [], '.', color=colors_outcome[2], markeredgewidth=1.5)
        
        # Initialization of the plots for the performance by ILD axes
        self.plots[1, 1] = np.array([PlotStruct() for i in range(2)])
        self.plots[1, 1][0].plot, = self.ax[1, 1].plot([], [], 'o-', markerfacecolor='none', color=colors_outcome[0], markeredgewidth=1.5)
        self.plots[1, 1][1].plot, = self.ax[1, 1].plot([], [], 'o-', markerfacecolor='none', color=colors_outcome[2], markeredgewidth=1.5)
        
        # Initialization of the plots for the CNP time axes
        self.plots[1, 2] = np.array([PlotStruct() for i in range(5)])
        self.plots[1, 2][0].plot, = self.ax[1, 2].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[1, 2][1].plot, = self.ax[1, 2].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[1, 2][2].plot, = self.ax[1, 2].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[1, 2][3].plot, = self.ax[1, 2].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[1, 2][4].plot, = self.ax[1, 2].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_outcome[2], markeredgewidth=1.5)
        
        # Initialization of the plots for the reaction time axes
        self.plots[2, 0] = np.array([PlotStruct() for i in range(5)])
        self.plots[2, 0][0].plot, = self.ax[2, 0].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[2, 0][1].plot, = self.ax[2, 0].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[2, 0][2].plot, = self.ax[2, 0].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[2, 0][3].plot, = self.ax[2, 0].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[2, 0][4].plot, = self.ax[2, 0].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_outcome[2], markeredgewidth=1.5)
        
        # Initialization of the plots for the movement time axes
        self.plots[2, 1] = np.array([PlotStruct() for i in range(5)])
        self.plots[2, 1][0].plot, = self.ax[2, 1].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[2, 1][1].plot, = self.ax[2, 1].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[2, 1][2].plot, = self.ax[2, 1].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[2, 1][3].plot, = self.ax[2, 1].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[2, 1][4].plot, = self.ax[2, 1].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_outcome[2], markeredgewidth=1.5)

        # Display buttons
        button_ax = np.zeros(6, dtype=object)
        self.buttons = np.zeros(6, dtype=object)
        # Buttons labels
        button_labels = ["Next trial left", " Next trial right", "Reward left", "Reward right", "Repeat errors", "Stop session"]
        # Buttons y positions
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

        # Informative text
        self.text = plt.text(self.ax[0, 0].get_position().x0 + 0.005, self.ax[0, 0].get_position().y0 + 0.01, "", transform=self.fig.transFigure, fontsize = 8, linespacing = 1.5)

    def show(self):
        """
        Shows the matplotlib figure. This is a helper function to be called by the Controller object.
        """
        plt.show()

class PlotStruct:
    """
    A class containing the matplotlib plot object itself and the x and y data. It is meant to be a helper class for some common operations (add new data to the plot or reset it, for example).

    Attributes
    ----------
    x : list
        the x values.
    y : list
        the y values
    plot : Line2D, optional
        the plot object itself.
    """
    def __init__(self, plot = None):
        self.x = []
        self.y = []
        self.plot = plot

    def update(self):
        """
        Updates the plot with the current x and y data.
        """
        if self.plot is not None:
            self.plot.set_xdata(self.x)
            self.plot.set_ydata(self.y)

    def add_data(self, x: float, y: float):
        """
        Adds a new (x, y) point to the respective lists and updates the plot data.

        Parameters
        ----------
        x : float
            the x coordinate of the new data point.
        y : float
            the y coordinate of the new data point.
        """
        self.x.append(x)
        self.y.append(y)
        self.update()

    def reset(self):
        """
        Resets the x and y lists and updates the plot data accordingly.
        """
        self.x = []
        self.y = []
        self.update()