from speaker import Speaker
from listener import Listener
from view import View


import shutil
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
            "Trial": 1,
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

    def initialization(self):
        """
        Asks a bunch of initial prompts useful for the task execution.
        """
        # File paths used
        startup_path = "../config/startup.json"
        with open(startup_path, "r") as file:
            paths = json.load(file)

        # Read animal.json
        with open(correct_path(paths["AnimalFile"]), "r") as file:
            animal = json.load(file)

        # Animal number
        self.information["Rat"] = get_animal_number()
        animal["Animal"] = self.information["Rat"]

        self.output_dir = correct_path(paths["OutputDir"])
        df, is_new_animal = get_latest_file(self.output_dir, animal["Animal"])

        # Setup number
        animal["Box"] = get_setup_number()
        # Asks whether this is a new session
        if is_new_animal or is_new_session():
            # Session number
            if is_new_animal:
                animal["Session"] = 1
                self.information["Block"] = 1
            else:
                animal["Session"] = int(df["Session"] + 1)
                self.information["Block"] = int(df["Block"] + 1)
                
            # Session type
            animal["SessionType"] = get_session_type(df, is_new_animal)
            # Initial training level
            animal["StartingTrainingLevel"] = get_initial_level(df, is_new_animal)
            self.information["Training level"] = animal["StartingTrainingLevel"]
        else:
            # Session number
            animal["Session"] = int(df["Session"])
            # Session type
            animal["SessionType"] = int(df["SessionType"])
            # Initial training level
            animal["StartingTrainingLevel"] = int(df["TrainingLevel"])
            self.information["Training level"] = int(df["TrainingLevel"])
            self.information["Block"] = int(df["Block"])

        animal["StartingBlockNumber"] = self.information["Block"]
        # Last training level
        animal["LastTrainingLevel"] = get_last_level(correct_path(paths["TrainingFile"]))
        # Session duration
        animal["SessionDuration"] = get_session_duration()

        # Write new animal.json
        with open(correct_path(paths["AnimalFile"]), "w") as file:
            json.dump(animal, file, indent=4)

        rat_path = correct_path(paths["OutputDir"]) + "/Rat" + str(animal["Animal"]).zfill(3)
        if os.path.isdir(rat_path):
            folders = [name for name in os.listdir(rat_path) if os.path.isdir(os.path.join(rat_path, name))]
            if folders[-1] != datetime.now().strftime('%y%m%d'):
                new_csv = pd.read_csv(rat_path + '/' + folders[-1] + "/out.csv")
                os.makedirs(rat_path + '/' + datetime.now().strftime('%y%m%d'), exist_ok=True)
                new_csv.to_csv(rat_path + '/' + datetime.now().strftime('%y%m%d') + "/out.csv", index=False)
        else:
            os.makedirs(rat_path + '/' + datetime.now().strftime('%y%m%d'), exist_ok=True)
            header = ["Animal", "Session", "SessionType", "Trial", "Block", "TrialsPerBlock", "TrainingLevel", "ABL", "ILD", "Bias", "LeftAmp", "RightAmp", "WaveformL", "WaveformR", "TrialStart", "TrialEnd", "TrialDuration", "IntendedITI", "ITIStart", "ITIEnd", "TimedITI", "MaxWait", "TimeToCNP", "BaseFix", "ExpFixMean", "IntendedFix", "TimedFix", "BaseRT", "MaxRT", "TimedRT", "MaxMT", "TimedMT", "IntendedLNP", "TimedLNP", "ResponsePoke", "Outcome", "RepeatTrial", "BlockPerformance", "BlockAbortRatio", "LEDTrial", "TimedLED", "LEDPowerL", "LEDPowerR", "Box"]
            new_csv = pd.DataFrame(columns=header)
            new_csv.to_csv(rat_path + '/' + datetime.now().strftime('%y%m%d') + "/out.csv", index=False)

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
            self.ild_aborts = np.zeros(int(args[1]))
            self.ild_correct = np.zeros(int(args[1]))
            self.ild_trials = np.zeros(int(args[1]))
            self.ild_completed = np.zeros(int(args[1]))

        # Otherwise, fill in the ILD array
        else:
            for i in range(self.view.plots[1, 1].size):
                self.view.plots[1, 1][i].x[int(args[0]) - 1] = args[1]

        # When the new ILD array is completed, reset all of the plots
        if args[0] == self.view.plots[1, 1][0].x.size:
            directory = self.output_dir + "/Rat" + str(self.information["Rat"]).zfill(3) + '/' + datetime.now().strftime('%y%m%d')
            png_names = [os.path.splitext(file)[0] for file in os.listdir(directory) if file.endswith('.png')]
            if len(png_names) == 0:
                new_png = directory + '/' + str(0).zfill(3) + ".png"
            else:
                new_png = directory + '/' + str(int(png_names[-1]) + 1).zfill(3) + ".png"

            self.view.fig.savefig(new_png)
            
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
        # Updates the data structures related to the last 10 trials
        self.last_ten(args[0])
        # Updates the performance plot
        self.view.plots[1, 0][0].add_data(self.information["Trial"], args[4])

        ild_index = np.where(self.view.plots[1, 1][0].x == self.information["ILD"])[0]
        self.ild_trials[ild_index] += 1

        # If trial was completed
        if args[0] > 0:
            # If "Right" would be the correct answer
            if self.information["ILD"] >= 0:
                self.view.plots[0, 2][2 * args[0] - 2].add_data(self.information["Trial"], args[0])
                self.view.plots[1, 2][2 * args[0] - 2].add_data(self.information["Trial"], args[1])
                self.view.plots[2, 0][2 * args[0] - 2].add_data(self.information["Trial"], args[2])
                self.view.plots[2, 1][2 * args[0] - 2].add_data(self.information["Trial"], args[3])
            # If "Left" would be the correct answer
            else:
                self.view.plots[0, 2][2 * args[0] - 1].add_data(self.information["Trial"], args[0])
                self.view.plots[1, 2][2 * args[0] - 1].add_data(self.information["Trial"], args[1])
                self.view.plots[2, 0][2 * args[0] - 1].add_data(self.information["Trial"], args[2])
                self.view.plots[2, 1][2 * args[0] - 1].add_data(self.information["Trial"], args[3])
            # If the animal didn't answer correctly
            if args[0] == 1:
                self.view.plots[0, 1][1].add_data(self.information["Trial"], self.information["ILD"])
            # If the animal answered correctly
            else:
                self.view.plots[0, 1][0].add_data(self.information["Trial"], self.information["ILD"])
                self.ild_correct[ild_index] += 1
            self.ild_completed[ild_index] += 1
            self.view.plots[1, 1][0].y[ild_index] = float(self.ild_correct[ild_index]) / self.ild_completed [ild_index]
            self.view.plots[1, 1][0].update()
        # If trial was aborted
        else:
            self.ild_aborts[ild_index] += 1
            self.view.plots[0, 1][2].add_data(self.information["Trial"], self.information["ILD"])
            self.view.plots[0, 2][-args[0] + 3].add_data(self.information["Trial"], args[0])

            # If the animal "produced" a CNP time, a reaction time or a movement time in this aborted trial
            if args[1] > 0:
                self.view.plots[1, 2][4].add_data(self.information["Trial"], args[1])
            if args[2] > 0:
                self.view.plots[2, 0][4].add_data(self.information["Trial"], args[2])
            if args[3] > 0:
                self.view.plots[2, 1][4].add_data(self.information["Trial"], args[3])

        self.view.plots[1, 1][1].y[ild_index] = float(self.ild_aborts[ild_index]) / self.ild_trials[ild_index]
        self.view.plots[1, 1][1].update()
        # Applies y-axis limits in the necessary plots
        self.view.ax[0, 1].set_ylim(-60, 60)
        self.view.ax[0, 2].set_ylim(-8, 3)
        self.view.ax[1, 0].set_ylim(0, 1)
        self.view.ax[1, 1].set_ylim(0, 1)

        # Applies some other plot configurations
        for i in range(3):
            for j in range(3):
                self.view.ax[i, j].xaxis.set_major_locator(MaxNLocator(integer=True))
                self.view.ax[i, j].relim()
                self.view.ax[i, j].autoscale_view()
        # Redraws the figure
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
        try:
            self.view.plots[1, 0][1].add_data(self.information["Trial"], float(count) / len(self.last_right))
        except:
            self.view.plots[1, 0][1].add_data(self.information["Trial"], 0)
        
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

    def bonsai(self):
        """
        Opens and runs the Bonsai task.
        """
        os.system(r"..\\..\\bonsai\\Bonsai.exe ..\\sound_lateralization_task.bonsai --start")

def get_animal_number():
    """
    Asks the user for the animal number.
    """
    while True:
        animal_number = input("Animal number: ")
        try:
            return int(animal_number)
        except:
            print("Not a valid input. Please enter an integer.")

def get_setup_number():
    """
    Asks the user for the setup number.
    """
    while True:
        setup = input("Setup number: ")
        try:
            return int(setup)
        except:
            print("Not a valid input. Please enter an integer.")

def is_new_session():
    """
    Asks the user whether this is a new session or not.
    """
    while True:
        new_session = input("New session? (blank or 1 = yes, 0 = no) ")
        if new_session == "" or new_session == "1":
            return True
        elif new_session == "0":
            return False
        else:
            print("Not a valid input.")

def get_session_type(df, is_new_animal: bool):
    """
    Asks the user for the session type.

    Parameters
    ----------
    df
        the Pandas dataframe from the last output file.
    """
    while True:
        session_type = input("Type of session: ")
        if session_type == "":
            if is_new_animal:
                return 1
            return int(df["SessionType"])
        else:
            try:
                return int(session_type)
            except:
                print("Not a valid input. Please enter an integer.")

def get_initial_level(df, is_new_animal: bool):
    """
    Asks the user for the initial training level.

    Parameters
    ----------
    df
        the Pandas dataframe from the last output file.
    """
    while True:
        training_level = input("Training level to start from (leave blank = start from previous): ")
        if training_level == "":
            if is_new_animal:
                return 1
            return int(df["TrainingLevel"])
        else:
            try:
                return int(training_level)
            except:
                print("Not a valid input. Please enter an integer.")

def get_last_level(training_path: str):
    """
    Asks the user for the last training level.

    Parameters
    ----------
    training_path : str
        path to the training.csv file.
    """
    while True:
        last_training_level = input("Training level to stop progressing (leave blank = final level): ")
        if last_training_level == "":
            df = pd.read_csv(training_path).iloc[-1]
            return int(df["Level"])
        else:
            try:
                return int(last_training_level)
            except:
                print("Not a valid input. Please enter an integer.")

def get_session_duration():
    """
    Asks the user for duration of the session.
    """
    while True:
        duration = input("Time of the session (in hh:mm:ss format): ")
        try:
            datetime.strptime(duration, "%H:%M:%S")
            return duration
        except:
            print("Not a valid input. Please enter the duration in the hh:mm:ss format.")

def get_latest_file(path: str, animal_number: int):
    folder = path + "/Rat" + str(animal_number).zfill(3)
    try:
        dirs = [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]
    except:
        return None, True

    for i in range(len(dirs) - 1, -1, -1):
        try:
            return pd.read_csv(folder + '/' + dirs[-1] + "/out.csv").iloc[-1], False
        except:
            continue
    return None, True


def correct_path(path: str):
    if path[0] == '.':
        return '.' + path
    return path