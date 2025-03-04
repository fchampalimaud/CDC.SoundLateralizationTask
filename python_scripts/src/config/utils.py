import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
from pyharp.device import Device
from serial.serialutil import SerialException
from tkinter.messagebox import showwarning
from tkinter import filedialog as fd


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
