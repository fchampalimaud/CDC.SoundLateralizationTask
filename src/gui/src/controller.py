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
    """
    A class that connects the matplotlib figure to the Python-side OSC server and client.

    Attributes
    ----------
    last_aborts : list
        a list containing the a maximum of 10 elements (the last 10 trials) where True is an aborted trial and False is a completed trial.
    last_right : list
        a list containing the a maximum of 10 elements (the last 10 completed trials) where True is an successful and False is an incorrect trial.
    information : dict
        the dict containing the text information shown in the view.
    units : list
        a list containing the units of the text information shown in the view.
    client : Speaker
        the OSC client object.
    listener : Listener
        the OSC server object.
    view : View
        the matplotlib GUI.
    bonsai_thread : Thread
        the thread that launches the Bonsai task.
    """
    def __init__(self):
        # Initializes the list containing information regarding the last 10 trials
        self.last_aborts = []
        self.last_right = []

        # Initializes the text information dictionary
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
        self.units = ["", "", "", "", "dB", "dB", "", "", "", "s", "s", ""]

        # Initial prompts
        self.initialization()

        # Initializes the OSC client
        self.client = Speaker()

        # Creates the message address-callback pairs
        messages = {"/beginning": self.new_trial, "/plots": self.update_plots, "/block": self.new_block}

        # Initializes the OSC server
        self.listener = Listener(messages)

        # Initializes the matplotlib interface
        self.view = View([self.client.next_left,
                          self.client.next_right,
                          self.client.left_reward,
                          self.client.right_reward,
                          self.client.repeat_errors,
                          self.client.stop_session])
        
        # Shows the text information in the figure
        self.generate_text()

        # Opens and runs the Bonsai task
        self.bonsai_thread = Thread(target=self.bonsai)
        self.bonsai_thread.start()

        # Kills the OSC server when the matplotlib figure is closed
        self.view.fig.canvas.mpl_connect('close_event', self.listener.shutdown)

        self.view.show()

    def bonsai(self):
        """
        Opens and runs the Bonsai task.
        """
        os.system(r"..\\..\\bonsai\\Bonsai.exe ..\\sound_lateralization_task.bonsai --start")

    # FIXME
    def initialization(self):
        """
        Asks a bunch of initial prompts useful for the task execution.
        """
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
        """
        This is the callback function for when the Python OSC server receives a message under the "/block" address. It resets the plots and part of the informative text.

        Parameters
        ----------
        address : str
            the message address.
        args : list
            the message itself. For the "/block" address, the message is composed by: [int index, (float ild_value if index != 0, float ild_array_length if index == 0)].
        """
        # If the first argument is 0, reset the ILD array
        if args[0] == 0:
            for i in range(self.view.plots[1, 1].size):
                self.view.plots[1, 1][i].x = np.zeros(int(args[1]))
                self.view.plots[1, 1][i].y = np.zeros(int(args[1]))
        # Otherwise, fill in the ILD array
        else:
            for i in range(self.view.plots[1, 1].size):
                self.view.plots[1, 1][i].x[int(args[0]) - 1] = args[1]

        # When the new ILD array is completed, reset all of the plots
        if args[0] == self.view.plots[1, 1][0].x.size:
            for i in range(3):
                for j in range(3):
                    # Resets the plot which has the ILD array in the x-axis
                    if (i, j) in [(1, 1)]:
                        for k in range(self.view.plots[1, 1].size):
                            self.view.plots[1, 1][k].update()
                        self.view.ax[1, 1].relim()
                        self.view.ax[1, 1].autoscale_view()
                    # Resets the remaining plots
                    elif (i, j) not in [(0, 0), (1, 1), (2, 2)]:
                        for k in range(self.view.plots[i, j].size):
                            self.view.plots[i, j][k].reset()
                        
            self.view.fig.canvas.draw()

    def new_trial(self, address, *args):
        """
        This is the callback function for when the Python OSC server receives a message under the "/beginning" address.

        Parameters
        ----------
        address : str
            the message address.
        args : list
            the message itself. For the "/beginning" address, the message is composed by: [int trial, float ild, float abl, float fixation_time, float inter_trial_interval].
        """
        # Updates some entries of the dictionary
        self.information["Trial"] = args[0]
        self.information["ILD"] = args[1]
        self.information["ABL"] = args[2]
        self.information["Fixation time"] = args[3]
        self.information["ITI"] = args[4]

        # Updates the informative text displayed
        self.generate_text()
        self.view.fig.canvas.draw()

    def update_plots(self, address, *args):
        """
        This is the callback function for when the Python OSC server receives a message under the "/plots" address. It updates the plots.

        Parameters
        ----------
        address : str
            the message address.
        args : list
            the message itself. For the "/plots" address, the message is composed by: [int outcome, float cnp_time, float reaction_time, float movement_time, float performance, float abort_rate].
        """
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
        """
        Calculates the performance and the abort_rate for the last 10 trials.

        Parameters
        ----------
        outcome : int
            a number between 2 and -7 (excluding 0) encoding the result of the last trial.
        """
        # Adds the outcome from the last trial to the last_right and last_aborts lists
        if outcome == 2:
            self.last_right.append(True)
            self.last_aborts.append(False)
        elif outcome == 1:
            self.last_right.append(False)
            self.last_aborts.append(False)
        else:
            self.last_aborts.append(True)

        # Removes the first element of the lists if their lengths are equal to 11
        if len(self.last_aborts) == 11:
            self.last_aborts.pop(0)
        if len(self.last_right) == 11:
            self.last_right.pop(0)

        # Counts the number of successful trials among the last 10 completed trials
        count = 0
        for i in range(len(self.last_right)):
            if self.last_right[i]:
                count += 1
        # Adds a new data point with the performance of the last 10 completed trials
        self.view.plots[1, 0][1].add_data(self.information["Trial"], float(count) / len(self.last_right))
        
        # Counts the number of aborted trials among the last 10 trials
        count = 0
        for i in range(len(self.last_aborts)):
            if self.last_aborts[i]:
                count += 1
        # Adds a new data point with the abort rate of the last 10 trials
        self.view.plots[1, 0][2].add_data(self.information["Trial"], float(count) / len(self.last_aborts))

    def generate_text(self):
        """
        Displays some informative text in the matplotlib figure based on the self.information dict.
        """
        # Initializes the string to be displayed in the figure
        string = ""

        # Extracts the keys and values of the dict to different lists
        keys = list(self.information.keys())
        values = list(self.information.values())

        # Iteratively adds the lines with the formatted information to be displayed
        for i in range(len(keys)):
            string += keys[i] + ": " + str(values[i]) + " " + self.units[i]
            if i != (len(keys) - 1):
                string += "\n"

        # Sets the string created as the new informative text of the figure
        self.view.text.set_text(string)