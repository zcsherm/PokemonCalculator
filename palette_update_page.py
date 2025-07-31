import math
import os.path
import pickle
import sys
from tkinter import messagebox, ttk
import tkinter as tk

class PaletteUpdatePage(tk.Toplevel):
    def __init__(self, master, mon, palette_type= "normal):
        super().__init__()
        self._master = master
        self._mon = mon
        self.title("Update Palette Data")
        self.focus_set()
        self.calc = Calculator(mon, self)              # Need to reformat 

        # Create frames
        frame1 = tk.LabelFrame(self, borderwidth=1)    # For the images
        frame1.grid(row=0,column=0)

        frame2 = tk.LabelFrame(self, borderwidth=1)    # For the tools
        frame2.grid(row=0, column=1)

        frame3 = tk.LabelFrame(self, borderwidth=1)    # For action buttons?
        frame3.grid(row=0, column=2)
