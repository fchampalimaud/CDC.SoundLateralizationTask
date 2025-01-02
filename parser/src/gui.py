import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import ctypes
from src.generate_csv import generate_csv, append_json
from datetime import datetime

myappid = "fchampalimaud.parser.alpha"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class ParserGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Sets the window title and icon
        self.title("JSON to CSV parser")
        self.iconbitmap("assets/favicon.ico")

        # Sets the window size
        window_width = 350
        window_height = 200

        # Gets the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Sets the window position
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        self.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

        # Configures the rows and column of the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Creates the checkbox
        self.checkbox_var = tk.IntVar(self, 1)
        self.checkbox = ttk.Checkbutton(self, text="Single file", variable=self.checkbox_var, onvalue="1", offvalue="0")
        self.checkbox.grid(row=0, column=0)

        # Creates the button
        button = ttk.Button(self, text="Run", command=self.run)
        button.grid(row=1, column=0, sticky="nsew")
        
    def run(self):
        """
        Runs the parser code for chosen file(s) according to the checkbox state.
        """
        # Gets today's date and time
        now = datetime.now()
        # Format the date and time
        formatted_date = now.strftime("%y%m%d_%H%M%S")
        # Sets output file(s) path
        output_path = "output/" + formatted_date
        
        # Single file case
        if self.checkbox_var.get == 1:
            filename = fd.askopenfilename()
        # Directory case
        else:
            directory = fd.askdirectory()
            filename = output_path + ".json"
            append_json(directory, filename)

        # Generates the final CSV file
        generate_csv(input_file=filename, output_file=output_path + ".csv")
