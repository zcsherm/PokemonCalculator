import math
import os.path
import pickle
import sys
import tkinter
from tkinter import messagebox, ttk
import tkinter as tk
from PIL import Image, ImageTk
from calculatorfortkinter import *
import random
import time
import spritecropper

class MainScreen:
    """
    The main launch screen. Gives the user different options for editing palettes.
    """
    def __init__(self):
        # monlist = 'pokemonindex.pkl' # Use if your pokemon index is different from gen III.
        monlist = 'Monsfile.pkl' # Gets us a list of all names

        # setup the basic screen details
        self._mons = pickle.load(open(monlist, 'rb'))
        self._names= self._mons
        # Setup our basic tkinter window
        self._window = tk.Tk()
        self._window.config(width=600, height=600)
        self._window.title("Palette Adjuster")
        y = 100 # The Y height of the button
        # setup the dropdown entry
        txt1 = "Which Pokemon?"
        label = tk.Label(self._window, text=txt1)
        label.place(x=50, y=y - 25)
        self._which_mon_button = ttk.Combobox(
            values=self._names
        )
        self._which_mon_button.place(x=50, y=y)
        # on key release it will update the dropdown
        self._which_mon_button.bind('<KeyRelease>', self.on_select)

        # Setup the first launch option: Update both palettes
        label_text = "Update Both Palettes"  # Label text for the checkbox
        bothpals = tk.IntVar()
        self._both_palettes = tk.Checkbutton(self._window, text=label_text, variable=bothpals)
        self._both_palettes.place(x=50, y=y + 25)

        # Setup the second option: Update pngs
        label_text = f"Update .pngs"  # Label text for the checkbox
        pngs = tk.IntVar()
        self._update_png = tk.Checkbutton(self._window, text=label_text, variable=pngs)
        self._update_png.place(x=50, y=y + 50)

        # Setup the third option: Update normal palette only
        label_text = f"Update normal palette"  # Label text for the checkbox
        normpal = tk.IntVar()
        self._norm_palettes = tk.Checkbutton(self._window, text=label_text, variable=normpal)
        self._norm_palettes.place(x=50, y=y + 75)

        # setup the 4th option: Update Shiny pals only
        label_text = f"Update shiny palette"  # Label text for the checkbox
        shinypal = tk.IntVar()
        self._shiny_palettes = tk.Checkbutton(self._window, text=label_text, variable=shinypal)
        self._shiny_palettes.place(x=50, y=y + 100)

        # setup the 6th option: Restore backup data
        label_text = f"Restore backup"  # Label text for the checkbox
        backup = tk.IntVar()
        self._backup_button = tk.Checkbutton(self._window, text=label_text, variable=backup)
        self._backup_button.place(x=50, y=y + 125)

        # Setup the 6th option: Add paldata (This is the main function we use)
        label_text = f"add paldata"  # Label text for the checkbox
        paldata = tk.IntVar()
        self._pal_data_button = tk.Checkbutton(self._window, text=label_text, variable=paldata)
        self._pal_data_button.place(x=50, y=y + 150)

        # Setup the 7th option: Add paldata for a shiny only
        label_text = f"add paladata (shiny)"  # Label text for the checkbox
        normedit = tk.IntVar()
        self._norm_edit_button = tk.Checkbutton(self._window, text=label_text, variable=normedit)
        self._norm_edit_button.place(x=50, y=y + 175)

        # Setup the 8th option: Icon editing (integrated in add paldata)
        label_text = f"edit icon"  # Label text for the checkbox
        iconedit = tk.IntVar()
        self._icon_edit_button = tk.Checkbutton(self._window, text=label_text, variable=iconedit)
        self._icon_edit_button.place(x=50, y=y + 200)

        # set all variables into a list
        self._launch_options = [bothpals, pngs, normpal, shinypal, backup, paldata, normedit, iconedit]
        # place a submit button
        self._submit_button = tk.Button(self._window, text="Submit", command=self.submit)
        self._submit_button.place(x=250, y=y)

    def submit(self):
        """
        Gets the choices that the user has selected on the main screen and the pokemon that was chosen.
        """
        # gathers the options from the checkboxes, and the mon name
        self.selected_options = [var.get() for var in self._launch_options]
        self._selected_options= self.selected_options
        print("Selected options:", self.selected_options)
        self.name = self._which_mon_button.get()
        self._mon_name =self.name
        print(self._which_mon_button.get())
        # diverts options to another function
        self.handleoptions()

    def closeout(self):
        """
        Destroys the current window
        """
        self._window.destroy()
        self.__init__()

    def on_select(self, event):
        """
        Populates the text box with autofill suggestions based on the users input
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

    def handleoptions(self):
        """
        Launches the chosen options that the user has selected for a given pokemon.
        :return:
        """
        # options should process as png first, paldata, normal, shiny,
        opts = self._selected_options
        # if the user has selected both pals and a single pal option, post an error
        if opts[0] and (opts[2] or opts[3]):
            print("INCOMPATIBLE SELECTIONS: Selected both palettes and a single pal option.")
            return
        # make sure we only selected backups and nothing else
        elif opts[4] and not (opts[0] or opts[1] or opts[2] or opts[3] or opts[5]):
            print('Only backups')
            newscreen = BackupScreen(self.name)
            return
        elif opts[4]:
            print("INCOMPATIBLE SELECTIONS: Selected backup and other options")
            return
        else:
            if opts[0]:
                print("bothpalettes")
                newscreen = PaletteUpdateScreen(self)
                newscreen.runpalfunc()
            if opts[1]:
                print("pngs")
                spritecropper.crop(self.name.lower())
            if opts[2]:
                print("normpalettes")
            if opts[3]:
                print("shinypalettes")
                newscreen = PaletteUpdateScreen(self, mode=1)
                newscreen.runpalfunc()
            if opts[5]:
                PalDataScreenWithIcon(self)
                print("paldata")
            if opts[6]:
                PalDataScreen(self, mode='shiny')
                print("paledit")
            if opts[7]:
                IconScreen(self)
                print("Icons")

    def launchshiny(self):
        self.palcounter = 0
        newscreen = PaletteUpdateScreen(self, mode=1)
        newscreen.runpalfunc()

class PaletteUpdateScreen:
    # This screen handles updating the palette data itself
    # by default this will read a pal file contents and then overwrite those same contents
    def __init__(self, source, mode=0):

        root = tk.Toplevel()  # create root window
        root.title("Basic GUI Layout")  # title of the GUI window
        root.geometry('900x800')  # specify the max size the window can expand to
        root.config(bg="skyblue")  # specify background color
        self.root = root
        self.source = source
        self.palcounter = 0
        self.mode = mode
        # Create left and right frames
        left_frame = tk.Frame(root, width=200, height=400, bg='grey')
        left_frame.grid(row=0, column=0, padx=10, pady=5)

        right_frame = tk.Frame(root, width=200, height=400, bg='grey')
        right_frame.place(x=300, y=5)
        error_box = tk.Frame(root, width=200, height=400, bg='grey')
        error_box.place(x=300, y=340)

        # Create frames and labels in left_frame
        tk.Label(left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(right_frame, text="Altered Image").grid(row=0, column=0, padx=5, pady=5)

        # load image to be "edited"
        mon = source.name.lower()
        self.calc = Calculator(mon, self)
        if mode == 0:
            # if we dont pass a mode, this is going to be the normal pal
            self.pal = self.calc.srcPalette
        if mode == 1:
            # if we dont pass a mode, this is going to be shiny
            self.pal = self.calc.destPalette
        image1 = Image.open(f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{mon}/front.png")
        image1back = Image.open(f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{mon}/back.png")
        image1icon = Image.open(f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{mon}/icon.png")
        if mode == 0:
            # if we dont pass a mode, this is going to be the normal pal
            self.pal = self.calc.srcPalette
        elif mode == 1:
            # if we dont pass a mode, this is going to be shiny
            self.pal = self.calc.destPalette
            destpal = [item for sublist in self.pal for item in sublist]
            image1.putpalette(destpal)
            image1back.putpalette(destpal)
        self.image1 = image1.resize((256, 256), Image.Resampling.LANCZOS)
        self.image1icon = image1icon.resize((128, 256), Image.Resampling.LANCZOS)
        self.image1back = image1back.resize((256, 256), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image1, master=root)
        self.imageback = ImageTk.PhotoImage(self.image1back, master=root)
        self.original_image = self.image  # resize image using subsample
        self.original_image_back = self.imageback
        self.label1 = tk.Label(left_frame, image=self.original_image)
        self.label1.grid(row=1, column=0, padx=5, pady=5)
        self.label1.image = self.original_image
        # Display image in right_frame)
        self.label2 = tk.Label(right_frame, image=self.image)
        self.label2.grid(row=1, column=0, padx=5, pady=5)
        self.label2b = tk.Label(right_frame, image=self.imageback)
        self.label2b.grid(row=1, column=1, padx=5, pady=5)
        self.label2b.image = self.imageback
        # Create tool bar frame
        self.tool_bar = tk.Frame(left_frame, width=400, height=600)
        self.tool_bar.grid(row=2, column=0, padx=5, pady=5)
        # create the error bar
        self.error_bar = tk.Frame(error_box, width=270, height=426)
        self.error_bar.grid(row=2, column=0, padx=5, pady=5)
        # Errmsg 1 and 2 are for the additional info on the error
        self.errmsg1 = tk.Label(self.error_bar, text='')
        self.errmsg1.grid(row=0, column=0, padx=3, pady=2)
        self.errmsg2 = tk.Label(self.error_bar)
        self.errmsg2.grid(row=1, column=0, padx=3, pady=2)
        # setup a message for each color and then an entry for each
        self.errmsgR = tk.Label(self.error_bar)
        self.errmsgR.grid(row=2, column=0, padx=3, pady=2)
        self.entryR = tk.Spinbox(self.error_bar, from_=0, to=255)
        self.entryR.grid(row=2, column=1, padx=3, pady=2)
        self.errmsgG = tk.Label(self.error_bar)
        self.errmsgG.grid(row=3, column=0, padx=3, pady=2)
        self.entryG = tk.Spinbox(self.error_bar, from_=0, to=255)
        self.entryG.grid(row=3, column=1, padx=3, pady=2)
        self.errmsgB = tk.Label(self.error_bar)
        self.errmsgB.grid(row=4, column=0, padx=3, pady=2)
        self.entryB = tk.Spinbox(self.error_bar, from_=0, to=255)
        self.entryB.grid(row=4, column=1, padx=3, pady=2)
        self.submit = tk.Button(text="Next Color", master=self.error_bar, command=self.checkinputs)
        self.submit.grid(row=5, column=1)
        self.errmsg1["text"] = "test"
        self.label2.image = self.image
        # Example labels that serve as placeholders for other widgets
        tk.Label(self.tool_bar, text="Original Palette", relief=tk.RAISED).grid(row=0, column=1, padx=5, pady=3,
                                                                                ipadx=10)  # ipadx is padding inside the Label widget
        tk.Label(self.tool_bar, text="New Palette", relief=tk.RAISED).grid(row=0, column=2, padx=5, pady=3, ipadx=10)

        # Example labels that could be displayed under the "Tool" menu
        for i in range(16):
            tk.Label(self.tool_bar, text=f"Color {i}").grid(row=i + 1, column=0, padx=3, pady=2)
        for i in range(16):
            tmp = self.pal[i]
            txt = f"{tmp[0]}, {tmp[1]}, {tmp[2]}"
            tk.Label(self.tool_bar, text=f"{txt}").grid(row=i + 1, column=1, padx=3, pady=2)

    def runpalfunc(self):
        self.calc.arrangeColors(self.calc.srcPalette)
        self.calc.getcolororder()
        self.calc.applyMasks(mode=self.mode)
        pass

    def rundemo(self):
        demowindowicon(self.image1icon, self.calc.srcPalette, self.calc.iconindex,mode=1)


    def checkinputs(self):
        if self.palcounter > 15:
            demowindow(self.image1, self.calc.srcPalette, self.calc.index)
            demowindow(self.image1back, self.calc.srcPalette, self.calc.index)
            return
        r = self.entryR.get()
        g = self.entryG.get()
        b = self.entryB.get()
        if not (r or g or b):
            r = 'y'
            g = 'y'
            b = 'y'
        if not (r and g and b):
            print("FAILURE")
            tk.messagebox.showerror('Entry Error', 'Error: Cannot have blank fields!', parent=self.root)
            return
        try:
            if int(r) > 255 or int(r) < 0:
                print('fail')
                tk.messagebox.showerror('Entry Error', f'Error: r {r} was not 0-255!', parent=self.root)
                return
        except:
            if r.lower() != 'y':
                tk.messagebox.showerror('Entry Error', f'Error: r {r} was not valid!', parent=self.root)
                return
        try:
            if int(g) > 255 or int(g) < 0:
                print('fail')
                tk.messagebox.showerror('Entry Error', f'Error: g {g} was not 0-255!', parent=self.root)
                return
        except:
            if g.lower() != 'y':
                tk.messagebox.showerror('Entry Error', f'Error: g {r} was not valid!', parent=self.root)
                return
        try:
            if int(b) > 255 or int(b) < 0:
                print('fail')
                tk.messagebox.showerror('Entry Error', f'Error: b {b} was not 0-255!', parent=self.root)
                return
        except:
            if b.lower() != 'y':
                tk.messagebox.showerror('Entry Error', f'Error: b {b} was not valid!', parent=self.root)
                return
        self.calc.fixcolor(r, g, b)

    def updateimage(self, destpal):
        """
        asd
        :param destpal: 
        :return: 
        """
        # this should update the image on the right, should be called after every color update
        destpal2 = [item for sublist in destpal for item in sublist]
        print(destpal)
        print(destpal2)
        im = self.image1
        im2 = self.image1back
        im.putpalette(destpal2)
        im2.putpalette(destpal2)
        self.image1 = im.resize((256, 256), Image.Resampling.LANCZOS)
        self.image1back = im2.resize((256, 256), Image.Resampling.LANCZOS)
        self.image3 = ImageTk.PhotoImage(self.image1, master=self.root)
        self.image3back = ImageTk.PhotoImage(self.image1back, master=self.root)
        self.label2.configure(image=self.image3)
        self.label2.image = self.image3
        self.label2b.configure(image=self.image3back)
        self.label2b.image = self.image3back

    def clear(self):
        self.errmsg2['text'] = ''
        self.errmsg1['text'] = ''
        self.entryR.delete(0, tk.END)
        self.entryG.delete(0, tk.END)
        self.entryB.delete(0, tk.END)
        self.errmsgR['text'] = ''
        self.errmsgG['text'] = ''
        self.errmsgB['text'] = ''

    def savepal(self):
        print('test')
        if self.mode == 0 and self.source.selected_options[0]:
            self.root.destroy()
            self.source.palcounter = 0
            self.source.launchshiny()
