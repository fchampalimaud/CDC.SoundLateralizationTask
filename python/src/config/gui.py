import ctypes
import tkinter as tk
from tkinter import ttk

from config.config import ConfigGUI
from config.load_sounds import LoadSounds

myappid = "fchampalimaud.preconfig.alpha"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
ctypes.windll.shcore.SetProcessDpiAwareness(1)


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Sets the window title and icon
        self.title("Setup")
        self.iconbitmap("assets/favicon.ico")
        self.geometry("250x100")

        # Configures the rows and column of the grid
        for i in range(2):
            self.grid_rowconfigure(i, weight=1)
        for i in range(1):
            self.grid_columnconfigure(i, weight=1)

        self.config_gui = ConfigGUI()
        self.config_gui.withdraw()
        self.load_gui = LoadSounds()
        self.load_gui.withdraw()

        self.config_button = ttk.Button(
            self, text="Setup configuration", command=self.open_config_window
        )
        self.config_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.load_button = ttk.Button(
            self, text="Load sounds to Harp SoundCard", command=self.open_load_window
        )
        self.load_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    def open_config_window(self):
        self.config_gui.deiconify()

    def open_load_window(self):
        self.load_gui.deiconify()
