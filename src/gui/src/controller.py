from speaker import Speaker
from listener import Listener
from view import View

from threading import Thread
import os
import json
from datetime import datetime
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator

class Controller:
    def __init__(self):
        self.information = {
            "Rat": 0,
            "Trial": 0,
            "Trials completed": 0,
            "Block" : 0,
            "ILD": 0,
            "ABL": 0,
            "Training level": 0,
            "Performance": 0,
            "Abort rate": 0,
            "Fixation time": 0,
            "ITI": 0,
            "Time elapsed": 0
            }

        self.initialization()

        # UDP Client
        self.client = Speaker()

        # MatPlotLib Figure
        self.view = View([self.client.next_left,
                          self.client.next_right,
                          self.client.left_reward,
                          self.client.right_reward,
                          self.client.repeat_errors,
                          self.client.stop_session])

        messages = {"/beginning": self.new_trial, "/plots": self.update_plots, "/block": self.new_block}

        # UDP Server
        self.listener = Listener(messages)

        self.view.fig.canvas.mpl_connect('close_event', self.listener.shutdown)

        self.units = ["", "", "", "", "dB", "dB", "", "", "", "s", "s", ""]

        self.last_aborts = []
        self.last_right = []

        self.generate_text()

        self.bonsai_thread = Thread(target=self.bonsai)
        self.bonsai_thread.start()
        # self.bonsai()

        self.view.show()

    def bonsai(self):
        os.system(r"..\\..\\bonsai\\Bonsai.exe ..\\sound_lateralization_task.bonsai --start")

    # FIXME
    def initialization(self):
        # FIXME
        df = pd.read_csv("../output/Rat001/241017/out.csv")
        df = df.iloc[-1]

        file = open("../config/animal.json",)

        animal = json.load(file)

        while True:
            animal_number = input("Animal number: ")
            try:
                self.information["Rat"] = int(animal_number)
                animal["Animal"] = int(animal_number)
                break
            except:
                print("Not a valid input. Please enter an integer.")

        while True:
            setup = input("Setup number: ")
            try:
                animal["Box"] = int(setup)
                break
            except:
                print("Not a valid input. Please enter an integer.")

        while True:
            new_session = input("New session? (blank or 1 = yes, 0 = no) ")
            if new_session == "" or new_session == "1":
                animal["Session"] = int(df["Session"] + 1)
                loop = True
                break
            elif new_session == "0":
                animal["Session"] = int(df["Session"])
                animal["SessionType"] = int(df["SessionType"])
                animal["StartingTrainingLevel"] = int(df["TrainingLevel"])
                self.information["Training level"] = int(df["TrainingLevel"])
                loop = False
                break
            else:
                print("Not a valid input.")

        while loop:
            session_type = input("Type of session: ")
            if session_type == "":
                animal["SessionType"] = int(df["SessionType"])
                break
            else:
                try:
                    animal["SessionType"] = int(session_type)
                    break
                except:
                    print("Not a valid input. Please enter an integer.")

        while loop:
            training_level = input("Training level to start from (leave blank = start from previous): ")
            if training_level == "":
                animal["StartingTrainingLevel"] = int(df["TrainingLevel"])
                self.information["Training level"] = int(df["TrainingLevel"])
                break
            else:
                try:
                    self.information["Training level"] = int(training_level)
                    animal["StartingTrainingLevel"] = int(training_level)
                    break
                except:
                    print("Not a valid input. Please enter an integer.")

        while True:
            last_training_level = input("Training level to stop progressing (leave blank = final level): ")
            if last_training_level == "":
                # FIXME
                df2 = pd.read_csv("../config/training.csv")
                df2 = df2.iloc[-1]
                animal["LastTrainingLevel"] = int(df2["Level"])
                break
            else:
                try:
                    animal["LastTrainingLevel"] = int(last_training_level)
                    break
                except:
                    print("Not a valid input. Please enter an integer.")

        while True:
            duration = input("Time of the session (in hh:mm:ss format): ")
            try:
                datetime.strptime(duration, "%H:%M:%S")
                animal["SessionDuration"] = duration
                break
            except:
                print("Not a valid input. Please enter the duration in the hh:mm:ss format.")

        file.close()

        with open("../config/animal.json", "w") as file:
            json.dump(animal, file, indent=4)

    def new_block(self, address, *args):
        if args[0] == 0:
            for i in range(self.view.plots[1, 1].size):
                self.view.plots[1, 1][i].x = np.zeros(int(args[1]))
                self.view.plots[1, 1][i].y = np.zeros(int(args[1]))
        else:
            for i in range(self.view.plots[1, 1].size):
                self.view.plots[1, 1][i].x[int(args[0]) - 1] = args[1]

        if args[0] == self.view.plots[1, 1][0].x.size:
            for i in range(3):
                for j in range(3):
                    if (i, j) in [(1, 1)]:
                        for k in range(self.view.plots[1, 1].size):
                            self.view.plots[1, 1][k].update()
                        self.view.ax[1, 1].relim()
                        self.view.ax[1, 1].autoscale_view()
                    elif (i, j) not in [(0, 0), (1, 1), (2, 2)]:
                        for k in range(self.view.plots[i, j].size):
                            self.view.plots[i, j][k].reset()
                        
            self.view.fig.canvas.draw()

    def new_trial(self, address, *args):
        self.information["Trial"] = args[0]
        self.information["ILD"] = args[1]
        self.information["ABL"] = args[2]
        self.information["Fixation time"] = args[3]
        self.information["ITI"] = args[4]

        self.generate_text()
        self.view.fig.canvas.draw()

    def update_plots(self, address, *args):
        self.last_ten(args[0])

        if args[0] > 0:
            if self.information["ILD"] >= 0:
                self.view.plots[0, 2][2 * args[0] - 2].add_data(self.information["Trial"], args[0])
                self.view.plots[1, 2][2 * args[0] - 2].add_data(self.information["Trial"], args[1])
                self.view.plots[2, 0][2 * args[0] - 2].add_data(self.information["Trial"], args[2])
                self.view.plots[2, 1][2 * args[0] - 2].add_data(self.information["Trial"], args[3])
            else:
                self.view.plots[0, 2][2 * args[0] - 1].add_data(self.information["Trial"], args[0])
                self.view.plots[1, 2][2 * args[0] - 1].add_data(self.information["Trial"], args[1])
                self.view.plots[2, 0][2 * args[0] - 1].add_data(self.information["Trial"], args[2])
                self.view.plots[2, 1][2 * args[0] - 1].add_data(self.information["Trial"], args[3])
            if args[0] == 1:
                self.view.plots[0, 1][1].add_data(self.information["Trial"], self.information["ILD"])
            else:
                self.view.plots[0, 1][0].add_data(self.information["Trial"], self.information["ILD"])
        else:
            self.view.plots[0, 1][2].add_data(self.information["Trial"], self.information["ILD"])
            self.view.plots[0, 2][-args[0] + 3].add_data(self.information["Trial"], args[0])

            if args[1] > 0:
                self.view.plots[1, 2][4].add_data(self.information["Trial"], args[1])
            if args[2] > 0:
                self.view.plots[2, 0][4].add_data(self.information["Trial"], args[2])
            if args[3] > 0:
                self.view.plots[2, 1][4].add_data(self.information["Trial"], args[3])

        self.view.plots[1, 0][0].add_data(self.information["Trial"], args[4])

        self.view.ax[0, 1].set_ylim(-60, 60)
        self.view.ax[0, 2].set_ylim(-8, 2)
        self.view.ax[1, 0].set_ylim(0, 1)
        self.view.ax[1, 1].set_ylim(0, 1)

        for i in range(3):
            for j in range(3):
                self.view.ax[i, j].xaxis.set_major_locator(MaxNLocator(integer=True))
                self.view.ax[i, j].relim()
                self.view.ax[i, j].autoscale_view()
        self.view.fig.canvas.draw()

    def last_ten(self, outcome):
        if outcome == 2:
            self.last_right.append(True)
            self.last_aborts.append(False)
        elif outcome == 1:
            self.last_right.append(False)
            self.last_aborts.append(False)
        else:
            self.last_aborts.append(True)

        if len(self.last_aborts) == 11:
            self.last_aborts.pop(0)
        if len(self.last_right) == 11:
            self.last_right.pop(0)

        count = 0
        for i in range(len(self.last_right)):
            if self.last_right[i]:
                count += 1

        self.view.plots[1, 0][1].add_data(self.information["Trial"], float(count) / len(self.last_right))
        
        count = 0
        for i in range(len(self.last_aborts)):
            if self.last_aborts[i]:
                count += 1

        self.view.plots[1, 0][2].add_data(self.information["Trial"], float(count) / len(self.last_aborts))

    def generate_text(self):
        keys = list(self.information.keys())
        values = list(self.information.values())

        string = ""

        for i in range(len(keys)):
            string += keys[i] + ": " + str(values[i]) + " " + self.units[i]
            if i != (len(keys) - 1):
                string += "\n"

        self.view.text.set_text(string)