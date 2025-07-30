import main_page
import pickle as pkl
import tkinter as tk
from tkinter import messagebox

class Launcher:
    def __init__(self):
        self._root = tk.Tk()
        self.root.withdraw()
        self.launch_home()


    def launch_home(self, source=None):
        self._current = main_page.MainPage(master=self)
        if source:
            source.destroy()
        self._current.force_focus()
        
    def handle_options(self, source, options):
        """
        Handles requests for new pages from the Home Screen
        """
        pass
