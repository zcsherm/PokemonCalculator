import math
import os.path
import pickle
import sys
from tkinter import messagebox, ttk
import tkinter as tk

MON_FILE = 'Monsfile.pkl'
CHECKBOX_LABELS = ["Update Both Palettes",
                   "Update .pngs",
                   "Update normal palette",
                   "Update shiny palette",
                   "Restore backup",
                   "Add paldata",
                   "add paladata (shiny)",
                   "edit icon"
                  ]

class MainPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__()
        self._master = master
        self.title("Home")
        self.focus_set()
        self._launch_options =[tk.IntVar() for i in range(len((CHECKBOX_LABELS)]

        self.mons=pickle.load(open(MON_FILE,'rb'))

        # Setup the frames
        frame1 = tk.LabelFrame(self, borderwidth=0)  # For the Combobox and label
        frame1.grid(row=0, column=0, columnspan=3)
        frame2 = tk.LabelFrame(self, borderwidth=0) # For the checkbox elements
        frame2.grid(row=1, column=0, columnspan=1)
        frame3 = tk.LabelFrame(self, borderwidth=0) # For submit button
        frame3.grid(row=2, column=0, columnspan=3)
        frame4 = tk.LabelFrame(self, borderwidth=0) # For help button
        frame4.grid(row=3,column=3,columnspan=1)

        # Setup the elements
        label = tk.Label(frame1, text="Which Pokemon?")
        label.grid(row=0,column=0)
        self._which_mon_box = ttk.Combobox(frame1, values=self._mons)
        self._which_mon_box.grid(row=0, column=1)
        self._which_mon_button.bind('<KeyRelease>', self.on_select)

        # Checkboxes
        for i in range(len(CHECKBOX_LABELS)):
            label_text = CHECKBOX_LABELS[i]  # Label text for the checkbox
            check_button = tk.Checkbutton(frame2, text=label_text, variable=self._launch_options[i])
            check_button.grid(row=i,column=0,side='left',justify='left')
        
        # Submit
        submit_button = tk.Button(frame3,text="Submit",command=self.submit)
        submit_button.pack()

  
    def on_select(self, event=None):
        """
        Updates the combobox values when typing
        """
        current_text = self._which_mon_button.get()

        # Clear the previous suggestions
        if (len(current_text) > 2):
            self._which_mon_button['values'] = []

            # Create a list of suggestions based on the current input
            suggestions = [item for item in self._names if item.lower().startswith(current_text.lower())]
    
            # Update the combobox values with the suggestions
            self._which_mon_button['values'] = suggestions
            self._which_mon_button.event_generate("<Down>")
            
    def submit(self, event=None):
        """
        Fetches the requested pages
        """
        # gathers the options from the checkboxes, and the mon name
        options = [var.get() for var in self._launch_options]
        pokemon = self._which_mon_button.get()
        
        # diverts options to another function
        self._master.handle_options(self, options)
