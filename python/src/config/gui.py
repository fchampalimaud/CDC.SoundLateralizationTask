import ctypes
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from tkinter.messagebox import showinfo

from config.config import ConfigGUI
from config.load_sounds import LoadSounds
from config.utils import UploadSound

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

        self.load_gui.button.config(command=self.upload_sounds)

    def open_config_window(self):
        self.config_gui.deiconify()

    def open_load_window(self):
        self.load_gui.deiconify()

    def upload_sounds(self):
        self.load_gui.button.config(state=tk.DISABLED)
        thread = UploadSound(
            Path(self.load_gui.sound.calib_left.get()),
            Path(self.load_gui.sound.eq_left.get()),
            Path(self.load_gui.sound.calib_right.get()),
            Path(self.load_gui.sound.eq_right.get()),
            self.config_gui.ports.setup.get(),
            Path(self.config_gui.paths.setup.get()),
            num_sounds=5,
            durations=[
                duration.get()
                for duration in self.load_gui.sound_characteristics.durations
            ],
            ramp_times=[
                ramp_time.get()
                for ramp_time in self.load_gui.sound_characteristics.ramp_times
            ],
        )
        thread.start()

        self.monitor(thread)

    def monitor(self, thread):
        if thread.is_alive():
            # Check the thread every 100 ms
            self.after(100, lambda: self.monitor(thread))
        else:
            # Activates the Run button again
            self.load_gui.button.config(state=tk.NORMAL)

            showinfo(
                title="Information",
                message="The sounds were successfully uploaded to the SoundCard.",
            )
