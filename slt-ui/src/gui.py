import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from matplotlib.widgets import Button, Slider
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import argparse
from threading import Thread

class UserInterface:
    def __init__(self):

        # UDP Client
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default="127.0.0.1",
            help="The ip of the OSC server")
        parser.add_argument("--port", type=int, default=1,
            help="The port the OSC server is listening on")
        args = parser.parse_args()

        self.client = udp_client.SimpleUDPClient(args.ip, args.port)

        # UDP Server
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip",
            default="127.0.0.1", help="The ip to listen on")
        parser.add_argument("--port",
            type=int, default=2, help="The port to listen on")
        args = parser.parse_args()

        dispatcher = Dispatcher()
        dispatcher.map("/beginning", self.update_plots)
        dispatcher.map("/plots", self.update_plots)

        server = osc_server.ThreadingOSCUDPServer(
            (args.ip, args.port), dispatcher)

        server_thread = Thread(target=server.serve_forever)
        server_thread.start()


        # Matplotlib GUI
        fig, self.ax = plt.subplots(3, 3, figsize=(14, 10))
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
        self.plot_data = np.zeros((3, 3), dtype=np.ndarray)

        colors_outcome = ["green", "red", "black"]
        self.plots[0, 1] = np.zeros(3, dtype=object)
        self.plot_data[0, 1] = np.zeros((3, 2), dtype=list)
        for i in range(self.plots[0, 1].size):
            self.plots[0, 1][i], = self.ax[0, 1].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_outcome[i], markeredgewidth=1.5)
            self.plot_data[0, 1][i, 0] = []
            self.plot_data[0, 1][i, 1] = []

        colors_aborts = plt.cm.hsv(np.linspace(0.75, 0, 9))
        self.plots[0, 2] = np.zeros(11, dtype=object)
        self.plot_data[0, 2] = np.zeros((11, 2), dtype=list)
        self.plots[0, 2][0], = self.ax[0, 2].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_aborts[0], markeredgewidth=1.5)
        self.plots[0, 2][1], = self.ax[0, 2].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_aborts[0], markeredgewidth=1.5)
        self.plots[0, 2][2], = self.ax[0, 2].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_aborts[1], markeredgewidth=1.5)
        self.plots[0, 2][3], = self.ax[0, 2].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_aborts[1], markeredgewidth=1.5)
        for i in range(4, self.plots[0, 2].size):
            self.plots[0, 2][i], = self.ax[0, 2].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_aborts[i - 2], markeredgewidth=1.5)
        for i in range(self.plots[0, 2].size):
            self.plot_data[0, 2][i, 0] = []
            self.plot_data[0, 2][i, 1] = []

        self.plots[1, 0] = np.zeros(3, dtype=object)
        self.plot_data[1, 0] = np.zeros((3, 2), dtype=list)
        self.plots[1, 0][0], = self.ax[1, 0].plot([], [], 'o', color="grey", markeredgewidth=1.5)
        self.plots[1, 0][1], = self.ax[1, 0].plot([], [], '.', color=colors_outcome[0], markeredgewidth=1.5)
        self.plots[1, 0][2], = self.ax[1, 0].plot([], [], '.', color=colors_outcome[2], markeredgewidth=1.5)
        for i in range(self.plots[1, 0].size):
            self.plot_data[1, 0][i, 0] = []
            self.plot_data[1, 0][i, 1] = []
        
        self.plots[1, 1] = np.zeros(2, dtype=object)
        self.plot_data[1, 1] = np.zeros((2, 2), dtype=list)
        self.plots[1, 1][0], = self.ax[1, 1].plot([], [], 'o-', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[1, 1][1], = self.ax[1, 1].plot([], [], 'o-', markerfacecolor='none', markeredgecolor=colors_outcome[2], markeredgewidth=1.5)
        for i in range(self.plots[1, 1].size):
            self.plot_data[1, 1][i, 0] = []
            self.plot_data[1, 1][i, 1] = []
        
        self.plots[1, 2] = np.zeros(5, dtype=object)
        self.plot_data[1, 2] = np.zeros((5, 2), dtype=list)
        self.plots[1, 2][0], = self.ax[1, 2].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[1, 2][1], = self.ax[1, 2].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[1, 2][2], = self.ax[1, 2].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[1, 2][3], = self.ax[1, 2].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[1, 2][4], = self.ax[1, 2].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_outcome[2], markeredgewidth=1.5)
        for i in range(self.plots[1, 2].size):
            self.plot_data[1, 2][i, 0] = []
            self.plot_data[1, 2][i, 1] = []
        
        self.plots[2, 0] = np.zeros(5, dtype=object)
        self.plot_data[2, 0] = np.zeros((5, 2), dtype=list)
        self.plots[2, 0][0], = self.ax[2, 0].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[2, 0][1], = self.ax[2, 0].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[2, 0][2], = self.ax[2, 0].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[2, 0][3], = self.ax[2, 0].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[2, 0][4], = self.ax[2, 0].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_outcome[2], markeredgewidth=1.5)
        for i in range(self.plots[2, 0].size):
            self.plot_data[2, 0][i, 0] = []
            self.plot_data[2, 0][i, 1] = []
        
        self.plots[2, 1] = np.zeros(5, dtype=object)
        self.plot_data[2, 1] = np.zeros((5, 2), dtype=list)
        self.plots[2, 1][0], = self.ax[2, 1].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[2, 1][1], = self.ax[2, 1].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[0], markeredgewidth=1.5)
        self.plots[2, 1][2], = self.ax[2, 1].plot([], [], '<', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[2, 1][3], = self.ax[2, 1].plot([], [], '>', markerfacecolor='none', markeredgecolor=colors_outcome[1], markeredgewidth=1.5)
        self.plots[2, 1][4], = self.ax[2, 1].plot([], [], 'o', markerfacecolor='none', markeredgecolor=colors_outcome[2], markeredgewidth=1.5)
        for i in range(self.plots[2, 1].size):
            self.plot_data[2, 1][i, 0] = []
            self.plot_data[2, 1][i, 1] = []

        self.ax[0, 2].set_xlim(left=0)

        # Display buttons
        button_ax = np.zeros(9, dtype=object)
        buttons = np.zeros(9, dtype=object)
        button_labels = ["Next trial left", " Next trial right", "Reward left", "Reward right", "Light flashes", "Go to next block", "Repeat errors", "Fix block", "Stop session"]
        button_ypos = [0.3, 0.3, 0.25, 0.25, 0.15, 0.15, 0.1, 0.1, 0.05]
        for i in range(9):
            if i % 2 != 0 or i == 8:
                x = 0.8
            else:
                x = 0.69
            button_ax[i] = fig.add_axes([x, button_ypos[i], 0.1, 0.03])
            buttons[i] = Button(button_ax[i], button_labels[i], hovercolor='0.975')
            buttons[i].label.set_fontsize(9)
        buttons[0].on_clicked(self.click)
        buttons[1].on_clicked(self.update_plots)

        # Slider
        axfreq = fig.add_axes([0.69, 0.2, 0.21, 0.03])
        freq_slider = Slider(
            ax=axfreq,
            label='ILD Bias',
            valmin=-1,
            valmax=1,
            valinit=0,
        )
        
        freq_slider.on_changed(self.foo)
        freq_slider.label.set_size(9)


        t = ("Rat: \n"
            "Trial: \n"
            "Trials completed: \n"
            "Block: \n"
            "ILD: \n"
            "ABL: \n"
            "Bias: \n"
            "Learning stage: \n"
            "Current performance: \n"
            "Current abort rate: \n"
            "Current fixation time: \n"
            "Current ITI: \n"
            "Time elapsed: ")
        plt.text(self.ax[0, 0].get_position().x0 + 0.005, self.ax[0, 0].get_position().y0 + 0.01, t, transform=fig.transFigure, fontsize = 8, linespacing = 1.5)

        # fig.canvas.mpl_connect('close_event', on_close)

        self.trial = 0
        self.ild = 0
        self.abl = 0
        self.bias = 0
        self.ft = 0
        self.iti = 0

        plt.show()

    def new_trial(self, address, *args):
        self.trial = args[0]
        self.ild = args[1]

    # TODO: plots 1, 3, 4, 5, 6, 7
    def update_plots(self, address, *args):
        print(args[0])
        if args[0] > 0:
            if self.ild >= 0:
                self.plot_data[0, 2][2 * args[0] - 2, 0].append(self.trial)
                self.plot_data[0, 2][2 * args[0] - 2, 1].append(2 * args[0] - 2)
                self.plots[0, 2][2 * args[0] - 2].set_xdata(self.plot_data[0, 2][2 * args[0] - 2, 0])
                self.plots[0, 2][2 * args[0] - 2].set_ydata(self.plot_data[0, 2][2 * args[0] - 2, 1])

                self.plot_data[1, 2][2 * args[0] - 2, 0].append(self.trial)
                self.plot_data[1, 2][2 * args[0] - 2, 1].append(args[1])
                self.plots[1, 2][2 * args[0] - 2].set_xdata(self.plot_data[1, 2][2 * args[0] - 2, 0])
                self.plots[1, 2][2 * args[0] - 2].set_ydata(self.plot_data[1, 2][2 * args[0] - 2, 1])

                self.plot_data[2, 0][2 * args[0] - 2, 0].append(self.trial)
                self.plot_data[2, 0][2 * args[0] - 2, 1].append(args[2])
                self.plots[2, 0][2 * args[0] - 2].set_xdata(self.plot_data[2, 0][2 * args[0] - 2, 0])
                self.plots[2, 0][2 * args[0] - 2].set_ydata(self.plot_data[2, 0][2 * args[0] - 2, 1])

                self.plot_data[2, 1][2 * args[0] - 2, 0].append(self.trial)
                self.plot_data[2, 1][2 * args[0] - 2, 1].append(args[3])
                self.plots[2, 1][2 * args[0] - 2].set_xdata(self.plot_data[2, 1][2 * args[0] - 2, 0])
                self.plots[2, 1][2 * args[0] - 2].set_ydata(self.plot_data[2, 1][2 * args[0] - 2, 1])
            else:
                self.plot_data[0, 2][2 * args[0] - 1, 0].append(self.trial)
                self.plot_data[0, 2][2 * args[0] - 1, 1].append(2 * args[0] - 1)
                self.plots[0, 2][2 * args[0] - 1].set_xdata(self.plot_data[0, 2][2 * args[0] - 1, 0])
                self.plots[0, 2][2 * args[0] - 1].set_ydata(self.plot_data[0, 2][2 * args[0] - 1, 1])
                
                self.plot_data[1, 2][2 * args[0] - 1, 0].append(self.trial)
                self.plot_data[1, 2][2 * args[0] - 1, 1].append(args[1])
                self.plots[1, 2][2 * args[0] - 1].set_xdata(self.plot_data[1, 2][2 * args[0] - 1, 0])
                self.plots[1, 2][2 * args[0] - 1].set_ydata(self.plot_data[1, 2][2 * args[0] - 1, 1])
                
                self.plot_data[2, 0][2 * args[0] - 1, 0].append(self.trial)
                self.plot_data[2, 0][2 * args[0] - 1, 1].append(args[2])
                self.plots[2, 0][2 * args[0] - 1].set_xdata(self.plot_data[2, 0][2 * args[0] - 1, 0])
                self.plots[2, 0][2 * args[0] - 1].set_ydata(self.plot_data[2, 0][2 * args[0] - 1, 1])
                
                self.plot_data[2, 1][2 * args[0] - 1, 0].append(self.trial)
                self.plot_data[2, 1][2 * args[0] - 1, 1].append(args[3])
                self.plots[2, 1][2 * args[0] - 1].set_xdata(self.plot_data[2, 1][2 * args[0] - 1, 0])
                self.plots[2, 1][2 * args[0] - 1].set_ydata(self.plot_data[2, 1][2 * args[0] - 1, 1])
        else:
            self.plot_data[0, 2][-args[0] + 3, 0].append(self.trial)
            self.plot_data[0, 2][-args[0] + 3, 1].append(args[0])
            self.plots[0, 2][-args[0] + 3].set_xdata(self.plot_data[0, 2][-args[0] + 3, 0])
            self.plots[0, 2][-args[0] + 3].set_ydata(self.plot_data[0, 2][-args[0] + 3, 1])

            if args[1] > 0:
                self.plot_data[1, 2][4, 0].append(self.trial)
                self.plot_data[1, 2][4, 1].append(args[1])
                self.plots[1, 2][4].set_xdata(self.plot_data[1, 2][4, 0])
                self.plots[1, 2][4].set_ydata(self.plot_data[1, 2][4, 1])
            if args[2] > 0:
                self.plot_data[2, 0][4, 0].append(self.trial)
                self.plot_data[2, 0][4, 1].append(args[2])
                self.plots[2, 0][4].set_xdata(self.plot_data[2, 0][4, 0])
                self.plots[2, 0][4].set_ydata(self.plot_data[2, 0][4, 1])
            if args[3] > 0:
                self.plot_data[2, 1][4, 0].append(self.trial)
                self.plot_data[2, 1][4, 1].append(args[3])
                self.plots[2, 1][4].set_xdata(self.plot_data[2, 1][4, 0])
                self.plots[2, 1][4].set_ydata(self.plot_data[2, 1][4, 1])

        self.ax[0, 1].set_ylim(-60, 60)
        self.ax[0, 2].set_ylim(-8, 2)
        self.ax[1, 0].set_ylim(0, 1)
        self.ax[1, 1].set_ylim(0, 1)

        self.ax[0, 2].set_xlim(left=0)
        self.ax[1, 2].set_xlim(left=0)
        self.ax[2, 0].set_xlim(left=0)
        self.ax[2, 1].set_xlim(left=0)

        for i in range(3):
            for j in range(3):
                self.ax[i, j].xaxis.set_major_locator(MaxNLocator(integer=True))
                plt.draw()
        
    def click(self, event):
        self.client.send_message("/commands", "hello")

    def foo(self, val):
        print(val)

if __name__ == "__main__":
    UserInterface()