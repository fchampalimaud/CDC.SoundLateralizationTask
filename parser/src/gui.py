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

        # Configuration of the main window
        # Sets the window title and icon
        self.title("JSON to CSV parser")
        self.iconbitmap("assets/favicon.ico")
        # Sets the window width and height
        window_width = 350
        window_height = 200
        # Gets the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Sets the window position
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        self.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
        # Configures the row and column of the main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.checkbox_var = tk.IntVar(self, 1)
        self.checkbox = ttk.Checkbutton(self, text="Single file", variable=self.checkbox_var, onvalue="1", offvalue="0")
        self.checkbox.grid(row=0, column=0)

        button = ttk.Button(self, text="Run", command=self.run)
        button.grid(row=1, column=0, sticky="nsew")
        

    def run(self):
        now = datetime.now()
        # Format the date and time
        formatted_date = now.strftime("%y%m%d_%H%M%S")
        output_path = "output/" + formatted_date
        
        if self.checkbox_var.get == 1:
            filename = fd.askopenfilename()
        else:
            directory = fd.askdirectory()
            filename = output_path + ".json"
            append_json(filename, directory)
        generate_csv(output_filename=output_path + ".csv", read_filename=filename)

if __name__ == "__main__":
    gui = ParserGUI()
    gui.mainloop()