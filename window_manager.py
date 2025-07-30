import pickle as pkl
import tkinter as tk
from tkinter import messagebox

class Launcher:
    def __init__(self):
        self._root = tk.Tk()
        self.root.withdraw()
        #self._window = login_screen.LoginScreen(master=self)
        self._current = self._window
