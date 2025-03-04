import tkinter as tk
from tkinter import ttk
import ctypes
from config.utils import PortCombobox, PathWidget
from sgen.config import Config
import yaml

myappid = "fchampalimaud.preconfig.alpha"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
ctypes.windll.shcore.SetProcessDpiAwareness(1)


class PortsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for i in range(1):
            self.grid_columnconfigure(i, weight=1)

        self.behavior = PortCombobox(
            self, text="Harp Behavior", board_id=1216, row=0, column=0
        )
        self.soundcard = PortCombobox(
            self, text="Harp SoundCard", board_id=1280, row=1, column=0
        )
        self.left_pump = PortCombobox(
            self, text="Left Harp SyringePump", board_id=1296, row=2, column=0
        )
        self.right_pump = PortCombobox(
            self, text="Right Harp SyringePump", board_id=1296, row=3, column=0
        )
        self.current_driver = PortCombobox(
            self, text="Harp CurrentDriver", board_id=1282, row=4, column=0
        )


class PathsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        for i in range(4):
            self.grid_rowconfigure(i, weight=1)
        for i in range(1):
            self.grid_columnconfigure(i, weight=1)

        self.animal = PathWidget(self, text="Animal Config", row=0, column=0)
        self.setup = PathWidget(self, text="Setup Config", row=1, column=0)
        self.training = PathWidget(self, text="Training Config", row=2, column=0)
        self.output = PathWidget(
            self, text="Output Directory", row=3, column=0, folder=True
        )


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Sets the window title and icon
        self.title("Task pre-configuration")
        self.iconbitmap("assets/favicon.ico")

        # Configures the rows and column of the grid
        for i in range(2):
            self.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        self.ports = PortsFrame(self)
        self.ports.grid(row=0, column=0)

        self.paths = PathsFrame(self)
        self.paths.grid(row=0, column=1)

        self.button = ttk.Button(
            self, text="Update Configuration", command=self.generate_config
        )
        self.button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def generate_config(self):
        config = Config(
            behavior_port=self.ports.behavior.get(),
            soundcard_port=self.ports.soundcard.get(),
            left_pump_port=self.ports.left_pump.get(),
            right_pump_port=self.ports.right_pump.get(),
            currentdriver_port=self.ports.current_driver.get(),
            animal_path=self.paths.animal.get(),
            setup_path=self.paths.setup.get(),
            training_path=self.paths.training.get(),
            output_path=self.paths.output.get(),
        )

        config_dict = config.model_dump()

        yaml_string = (
            "# yaml-language-server: $schema=schemas/config-schema.json\n"
            + yaml.dump(config_dict, default_flow_style=False)
        )

        with open("../src/config/config.yml", "w") as file:
            file.write(yaml_string)
