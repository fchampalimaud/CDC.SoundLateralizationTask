import os
import time
import tkinter as tk
from datetime import datetime
from threading import Thread
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showwarning

import numpy as np
import pandas as pd
import serial.tools.list_ports
from pyharp.device import Device
from serial.serialutil import SerialException
from speaker_calibration.sound import create_sound_file, white_noise


class LabeledSpinbox:
    def __init__(
        self,
        container,
        text: str,
        row: int,
        column: int,
        width: float = 10,
        rowspan: int = 1,
        columnspan: int = 1,
        sticky=None,
    ):
        self.frame = tk.Frame(container)
        for i in range(2):
            self.frame.grid_rowconfigure(i, weight=1)
        for i in range(1):
            self.frame.grid_columnconfigure(i, weight=1)

        self.label = tk.Label(self.frame, text=text)
        self.label.grid(row=0, column=0, sticky="s")

        self.var = tk.IntVar(self.frame, 0)

        self.spinbox = ttk.Spinbox(
            self.frame,
            textvariable=self.var,
            justify="center",
            width=width,
            from_=0,
            to=1000,  # FIXME
        )
        self.spinbox.grid(row=1, column=0, sticky="n")

        self.frame.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            padx=5,
            pady=5,
            sticky=sticky,
        )

    def get(self):
        return self.var.get()

    def set(self, value: int):
        self.var.set(value)


class PortCombobox:
    def __init__(
        self,
        container,
        text: str,
        board_id: int,
        row: int,
        column: int,
        width: float = 10,
        rowspan: int = 1,
        columnspan: int = 1,
        sticky=None,
    ):
        self.id = board_id
        self.frame = tk.Frame(container)
        for i in range(2):
            self.frame.grid_rowconfigure(i, weight=1)
        for i in range(1):
            self.frame.grid_columnconfigure(i, weight=1)

        self.label = tk.Label(self.frame, text=text)
        self.label.grid(row=0, column=0, sticky="s")

        self.var = tk.StringVar(self.frame, "COMx")

        self.combobox = ttk.Combobox(
            self.frame,
            textvariable=self.var,
            justify="center",
            state="readonly",
            width=width,
        )
        self.combobox.grid(row=1, column=0, sticky="n")
        self.combobox["values"] = self.get_ports()
        self.combobox.bind("<<ComboboxSelected>>", self.connect)

        self.frame.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            padx=5,
            pady=5,
            sticky=sticky,
        )

        if self.id == 1216:
            self.board_name = "Harp Behavior"
        elif self.id == 1280:
            self.board_name = "Harp SoundCard"
        elif self.id == 1296:
            self.board_name = "Harp SyringePump"
        elif self.id == 1282:
            self.board_name = "Harp CurrentDriver"

    def get(self):
        port = self.var.get()
        if port == "COMx":
            return "COM0"
        return port

    def set(self, value: str):
        self.var.set(value)

    def set_values(self, value_list: list):
        self.combobox["values"] = value_list

    def get_ports(self):
        ports = serial.tools.list_ports.comports()

        port_strings = []
        for port in ports:
            port_strings.append(port.device)

        port_strings.append("Refresh")

        return port_strings

    def connect(self, event):
        if hasattr(self, "board"):
            self.board.disconnect()

        if self.var.get() == "Refresh":
            self.combobox["values"] = self.get_ports()
            self.var.set("COMx")
            return

        try:
            self.board = Device(self.var.get())
            if self.board.WHO_AM_I != self.id:
                showwarning("Warning", f"This is not a {self.board_name}.")
                self.var.set("COMx")
                self.board.disconnect()
        except SerialException:
            showwarning("Warning", "This is not a Harp Device.")
            self.var.set("COMx")


class PathWidget:
    def __init__(
        self,
        container,
        text: str,
        row: int,
        column: int,
        rowspan: int = 1,
        columnspan: int = 1,
        sticky=None,
        folder: bool = False,
    ):
        self.folder = folder
        self.frame = tk.Frame(container)
        for i in range(2):
            self.frame.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.frame.grid_columnconfigure(i, weight=1)

        self.label = tk.Label(self.frame, text=text)
        self.label.grid(row=0, column=0, columnspan=2, sticky="s")

        self.var = tk.StringVar(self.frame, "")

        self.entry = ttk.Entry(self.frame, textvariable=self.var, width=80)
        self.entry.grid(row=1, column=0, sticky="ne")
        if self.folder:
            self.button = ttk.Button(
                self.frame, text="Select Folder", command=self.get_file
            )
        else:
            self.button = ttk.Button(
                self.frame, text="Select File", command=self.get_file
            )
        self.button.grid(row=1, column=1, sticky="nw")

        self.frame.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            padx=5,
            pady=5,
            sticky=sticky,
        )

    def get(self):
        return self.var.get()

    def set(self, value: str):
        self.var.set(value)

    def get_file(self):
        if self.folder:
            self.set(fd.askdirectory())
        else:
            self.set(fd.askopenfilename())


def upload_sound(
    duration: float,
    left_calib_path: str,
    left_eq_filter_path: str,
    right_calib_path: str,
    right_eq_filter_path: str,
    abl: float = None,
    ild: float = 0,
    fs: int = 192000,
    filename: str = "sound.bin",
    soundcard_index: int = None,
):
    if soundcard_index < 2 and soundcard_index > 31:
        raise (ValueError("soundcard_index must be between 2 and 31"))

    eq_left = np.load(left_eq_filter_path)
    eq_right = np.load(right_eq_filter_path)
    fit_left = np.loadtxt(left_calib_path, delimiter=",")
    fit_right = np.loadtxt(right_calib_path, delimiter=",")

    if abl is None:
        attenuation_left = 1
        attenuation_right = 1
    else:
        db_left = abl - ild / 2
        attenuation_left = 10 ** ((db_left - fit_left[1]) / fit_left[0])
        db_right = abl + ild / 2
        attenuation_right = 10 ** ((db_right - fit_right[1]) / fit_right[0])

    signal_left = white_noise(
        duration,
        fs,
        amplitude=attenuation_left,
        freq_min=5000,
        freq_max=20000,
        inverse_filter=eq_left,
    )
    signal_right = white_noise(
        duration,
        fs,
        amplitude=attenuation_right,
        freq_min=5000,
        freq_max=20000,
        inverse_filter=eq_right,
    )

    create_sound_file(signal_left, signal_right, filename)
    if soundcard_index is not None:
        while True:
            output = os.popen(
                "cmd /c .\\assets\\toSoundCard.exe "
                + filename
                + " "
                + str(soundcard_index)
                + " 0 "
                + str(fs)
            ).read()

            if "Bandwidth: " in output:
                break
            print(output)
            time.sleep(3)


class UploadSound(Thread):
    def __init__(
        self,
        left_calib_path: str,
        left_eq_filter_path: str,
        right_calib_path: str,
        right_eq_filter_path: str,
        setup: int,
        setup_path: str,
    ):
        super().__init__()
        self.eq_left = np.load(left_eq_filter_path)
        self.eq_right = np.load(right_eq_filter_path)
        self.fit_left = np.loadtxt(left_calib_path, delimiter=",")
        self.fit_right = np.loadtxt(right_calib_path, delimiter=",")
        self.setup = setup
        self.setup_path = setup_path

    def run(self):
        date = datetime.now().strftime("%y%m%d_%H%M%S")
        for i in range(self.num_sounds.get()):
            upload_sound(
                10,
                self.calib_left.get(),
                self.eq_left.get(),
                self.calib_right.get(),
                self.eq_right.get(),
                abl=None,
                ild=0,
                fs=192000,
                filename="../" + date + "/noise" + str(i) + ".bin",
                soundcard_index=(2 * i + 2),
            )

        upload_sound(
            0.001,
            self.calib_left.get(),
            self.eq_left.get(),
            self.calib_right.get(),
            self.eq_right.get(),
            abl=None,
            ild=0,
            fs=192000,
            filename="../" + date + "/silence.bin",
            soundcard_index=31,
        )

        try:
            calib_left = np.loadtxt(self.calib_left.get(), delimiter=",")
            calib_right = np.loadtxt(self.calib_right.get(), delimiter=",")
            setups = pd.read_csv(self.setup_path)
            setups.loc[self.setup, "speakers.left_slope"] = calib_left[0]
            setups.loc[self.setup, "speakers.left_intercept"] = calib_left[1]
            setups.loc[self.setup, "speakers.right_slope"] = calib_right[0]
            setups.loc[self.setup, "speakers.right_intercept"] = calib_right[1]
            setups.to_csv(self.setup_path, index=False)

        except:
            print("It wasn't possible to update the setup.csv file.")
