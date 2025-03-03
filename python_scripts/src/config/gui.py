import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import ctypes

myappid = "fchampalimaud.parser.alpha"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
ctypes.windll.shcore.SetProcessDpiAwareness(1)


class PortsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)


class PathsFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Sets the window title and icon
        self.title("PreConfig")
        self.iconbitmap("assets/favicon.ico")

        # # Sets the window size
        # window_width = 350
        # window_height = 200

        # Gets the screen width and height
        # screen_width = self.winfo_screenwidth()
        # screen_height = self.winfo_screenheight()

        # Sets the window position
        # x = (screen_width / 2) - (window_width / 2)
        # y = (screen_height / 2) - (window_height / 2)
        # self.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

        # Configures the rows and column of the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.ports = PortsFrame(self)
        self.ports.grid(row=0, column=0)

        self.paths = PathsFrame(self)
        self.paths.grid(row=0, column=1)
