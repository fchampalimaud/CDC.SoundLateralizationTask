import ctypes
import tkinter as tk
from tkinter import ttk

from config.utils import PathWidget

myappid = "fchampalimaud.preconfig.alpha"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
ctypes.windll.shcore.SetProcessDpiAwareness(1)


class SoundCharacteristics(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        self.durations = []
        self.duration_widgets = []
        self.ramp_times = []
        self.ramp_time_widgets = []

        label = ttk.Label(self, text="Duration (s)")
        label.grid(row=0, column=1, padx=5, pady=5)

        label = ttk.Label(self, text="Ramp Time (s)")
        label.grid(row=0, column=2, padx=5, pady=5)

        for i in range(5):
            label = ttk.Label(self, text="Sound " + str(i))
            label.grid(row=i + 1, column=0, padx=5, pady=5)

            self.durations.append(tk.DoubleVar(value=10))
            self.duration_widgets.append(
                ttk.Spinbox(
                    self,
                    from_=0,
                    to=10,
                    increment=0.01,
                    textvariable=self.durations[i],
                    state="disabled",
                )
            )
            self.duration_widgets[i].grid(row=i + 1, column=1, padx=5, pady=5)

            # label = ttk.Label(self, text="Sound " + str(i) + " ramp time (s)")
            # label.grid(row=i, column=2, padx=5, pady=5)

            self.ramp_times.append(tk.DoubleVar(value=0.005))
            self.ramp_time_widgets.append(
                ttk.Spinbox(
                    self,
                    from_=0,
                    to=1,
                    increment=0.001,
                    textvariable=self.ramp_times[i],
                )
            )
            self.ramp_time_widgets[i].grid(row=i + 1, column=2, padx=5, pady=5)


class SoundLoadingFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)
        for i in range(1):
            self.grid_columnconfigure(i, weight=1)

        self.calib_left = PathWidget(
            self,
            text="Left Speaker Calibration Parameters",
            row=0,
            column=0,
            filetypes=[("NPY files", "*.npy"), ("All files", "*.*")],
        )
        self.eq_left = PathWidget(
            self,
            text="Left Speaker EQ Filter",
            row=1,
            column=0,
            filetypes=[("NPY files", "*.npy"), ("All files", "*.*")],
        )
        self.calib_right = PathWidget(
            self,
            text="Right Speaker Calibration Parameters",
            row=2,
            column=0,
            filetypes=[("NPY files", "*.npy"), ("All files", "*.*")],
        )
        self.eq_right = PathWidget(
            self,
            text="Right Speaker EQ Filter",
            row=3,
            column=0,
            filetypes=[("NPY files", "*.npy"), ("All files", "*.*")],
        )


class LoadSounds(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.withdraw)

        # Sets the window title and icon
        self.title("Load sounds")
        self.iconbitmap("assets/favicon.ico")

        # Configures the rows and column of the grid
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        self.sound = SoundLoadingFrame(self)
        self.sound.grid(
            row=0,
            column=0,
            columnspan=1,
        )

        self.sound_characteristics = SoundCharacteristics(self)
        self.sound_characteristics.grid(
            row=0,
            column=1,
            columnspan=1,
        )

        self.button = ttk.Button(self, text="Upload Sounds")
        self.button.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
