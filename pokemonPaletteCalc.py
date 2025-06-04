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

"""
The main screen should ask for the pokemon and then what operation should be carried out
If update pals:
    new screen that shows the old sprite, and then the new sprite
    first load the old pal numbers
    then perform the operation on each color
    should update the sprite after each color
    if there is an issue:
        highlight the color in red on the new sprite
        popup on right hand side the error message
        ask for input on right
"""


class MainScreen:
    # the main loading screen
    def __init__(self):
        #monlist = 'pokemonindex.pkl'
        monlist = 'Monsfile.pkl'
        # setup the basic screen details
        self.mons = pickle.load(open(monlist, 'rb'))
        #self.names = list(self.mons.values())
        self.names= self.mons
        self.window = tk.Tk()
        self.window.config(width=600, height=600)
        self.window.title("Palette Adjuster")
        y = 100
        # setup the dropdown entry
        txt1 = "Which Pokemon?"
        label = tk.Label(self.window, text=txt1)
        label.place(x=50, y=y - 25)
        self.whichmonbutton = ttk.Combobox(
            values=self.names
        )
        self.whichmonbutton.place(x=50, y=y)
        # on key release it will update the dropdown
        self.whichmonbutton.bind('<KeyRelease>', self.on_select)
        # check box1 for both pals
        label_text = f"Update Both Palettes"  # Label text for the checkbox
        bothpals = tk.IntVar()
        self.bothpalettes = tk.Checkbutton(self.window, text=label_text, variable=bothpals)
        self.bothpalettes.place(x=50, y=y + 25)
        # check box 2 for pngs
        label_text = f"Update .pngs"  # Label text for the checkbox
        pngs = tk.IntVar()
        self.updatepng = tk.Checkbutton(self.window, text=label_text, variable=pngs)
        self.updatepng.place(x=50, y=y + 50)
        # check box 3 for norm pal
        label_text = f"Update normal palette"  # Label text for the checkbox
        normpal = tk.IntVar()
        self.normpalettes = tk.Checkbutton(self.window, text=label_text, variable=normpal)
        self.normpalettes.place(x=50, y=y + 75)
        # check box 4 for shiny pal
        label_text = f"Update shiny palette"  # Label text for the checkbox
        shinypal = tk.IntVar()
        self.shinypalettes = tk.Checkbutton(self.window, text=label_text, variable=shinypal)
        self.shinypalettes.place(x=50, y=y + 100)
        # check box 5 for backups
        label_text = f"Restore backup"  # Label text for the checkbox
        backup = tk.IntVar()
        self.backupbutton = tk.Checkbutton(self.window, text=label_text, variable=backup)
        self.backupbutton.place(x=50, y=y + 125)
        # check box 6 for paldata
        label_text = f"add paldata"  # Label text for the checkbox
        paldata = tk.IntVar()
        self.paldatabutton = tk.Checkbutton(self.window, text=label_text, variable=paldata)
        self.paldatabutton.place(x=50, y=y + 150)
        # check box 7 for editing pal
        label_text = f"add paladata (shiny)"  # Label text for the checkbox
        normedit = tk.IntVar()
        self.normeditbutton = tk.Checkbutton(self.window, text=label_text, variable=normedit)
        self.normeditbutton.place(x=50, y=y + 175)
        # check box 8 for editing icon
        label_text = f"edit icon"  # Label text for the checkbox
        iconedit = tk.IntVar()
        self.iconeditbutton = tk.Checkbutton(self.window, text=label_text, variable=iconedit)
        self.iconeditbutton.place(x=50, y=y + 200)
        # set all variables into a list
        self.options = [bothpals, pngs, normpal, shinypal, backup, paldata, normedit,iconedit]
        # place a submit button
        self.submit_button = tk.Button(self.window, text="Submit", command=self.submit)
        self.submit_button.place(x=250, y=y)

    def submit(self):
        # gathers the options from the checkboxes, and the mon name
        self.selected_options = [var.get() for var in self.options]
        print("Selected options:", self.selected_options)
        self.name = self.whichmonbutton.get()
        print(self.whichmonbutton.get())
        # diverts options to another function
        self.handleoptions()

    def closeout(self):
        self.window.destroy()
        self.__init__()

    def on_select(self, event):
        # Get the text entered in the combobox
        current_text = self.whichmonbutton.get()

        # Clear the previous suggestions
        if (len(current_text) > 2):
            self.whichmonbutton['values'] = []

            # Create a list of suggestions based on the current input
            suggestions = [item for item in self.names if item.lower().startswith(current_text.lower())]

            # Update the combobox values with the suggestions
            self.whichmonbutton['values'] = suggestions
            self.whichmonbutton.event_generate("<Down>")

    def handleoptions(self):
        # options should process as png first, paldata, normal, shiny,
        opts = self.selected_options
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


class demowindow():
    def __init__(self, image, srcpal, mondata,mode=None):
        root = tk.Toplevel()  # create root window
        root.title("Basic GUI Layout")  # title of the GUI window
        root.maxsize(width=1800, height=800)  # specify the max size the window can expand to
        root.config(bg="skyblue")  # specify background color
        self.colors = [[[157, 106, 184], [105, 187, 147], [217, 224, 238], [135, 194, 124]],
                       [[177, 228, 226], [245, 126, 224], [207, 161, 144], [173, 137, 155]],
                       [[123, 251, 164], [64, 64, 64], [214, 138, 172], [194, 152, 208]],
                       [[243, 109, 114], [83, 113, 189], [248, 216, 48], [184, 108, 120]],
                       [[179, 254, 247], [218, 210, 91], [240, 240, 240], [94, 150, 144]],
                       [[151, 238, 158], [163, 207, 148], [100, 127, 161], [131, 127, 103]],
                       [[240, 240, 240], [93, 251, 255], [98, 239, 139], [248, 94, 160]],
                       [[81, 199, 122], [204, 86, 105], [140, 106, 172], [154, 151, 111]],
                       ]
        if mode is None:
            self.width = 256
        else:
            self.width = 128
        for i in range(8):
            # setup color 5 for each color option
            self.colors[i].append([self.colors[i][2][2], self.colors[i][1][0], self.colors[i][0][1]])
        self.paldata = mondata
        self.root = root
        self.srcpal = srcpal
        self.image = image
        self.labels = []
        for i in range(4):
            self.createpokepics(i)
        randomize = tk.Button(self.root, text="Randomize", command=self.randomizecolors, padx=10, pady=10)
        randomize.grid(column=4, row=0)

    def createpokepics(self, col):
        for row in range(2):
            # self.randomizecolors()
            self.updateimages(col, row)
            self.labels.append(tk.Label(self.root, image=self.image3))
            self.labels[col * 2 + row].grid(row=row, column=col, padx=5, pady=5)
            self.labels[col * 2 + row].image = self.image3

    def updateimages(self, col, row, colors=None, mode=0):
        if colors is None:
            colors = self.colors
        ind = (col * 2) + row  # which pic are we on
        tmp = []
        for val in self.srcpal:
            l = []
            for val2 in val:
                l.append(val2)
            tmp.append(l)
        # this should update the image on the right, should be called after every color update
        pal = []
        # ADD CODE FOR HANDLING OTHER CODES(LIKE BLENDS)
        for q in range(len(tmp)):
            b = False
            i = int(self.paldata[q][0])
            if len(self.paldata[q]) > 1:
                # gets us our blend code
                b = int(self.paldata[q][1])
            if i <= 5 and i > 0:
                # this tells us that depending what zone we need, we get that color
                color = colors[ind][i - 1]
                if b:
                    tmp2 = []
                    # print(f"{b} and this is for slot{q} in zone {i}")
                    if b == 9:
                        for comp in color:
                            # print(f'preadjust = {comp}')
                            comp = (comp + 255) / 2
                            # print(f'post adjust: {comp}')
                            tmp2.append(comp)
                    elif b == 8:
                        for comp in color:
                            # print(f'preadjust = {comp}')
                            comp = (comp + comp + 255) / 3
                            # print(f'post adjust: {comp}')
                            tmp2.append(comp)
                    elif b == 7:
                        color2 = colors[ind][3]
                        for i in range(3):
                            comp = color[i]
                            comp2 = color2[i]
                            # print(f'preadjust = {color[i]}')
                            comp = (comp + comp2) / 2
                            #  print(f'post adjust: {comp}')
                            tmp2.append(comp)
                    elif b == 6:
                        color2 = colors[ind][2]
                        for i in range(3):
                            comp = color[i]
                            comp2 = color2[i]
                            # print(f'preadjust = {comp}')
                            comp = (comp + comp2) / 2
                            # print(f'post adjust: {comp}')
                            tmp2.append(comp)
                    elif b == 5:
                        for comp in color:
                            # print(f'preadjust = {comp}')
                            comp = (comp + 0) / 3
                            # print(f'post adjust: {comp}')
                            tmp2.append(comp)
                    elif b == 4:
                        color2 = colors[ind][4]
                        for i in range(3):
                            comp = color[i]
                            comp2 = color2[i]
                            print(f'preadjust = {comp}')
                            comp = (comp + comp2) / 2
                            # print(f'post adjust: {comp}')
                            tmp2.append(comp)
                    elif b == 3:
                        for comp in color:
                            # print(f'preadjust = {comp}')
                            comp = (comp + 0) / 2
                            # print(f'post adjust: {comp}')
                            tmp2.append(comp)
                    else:
                        tmp2 = color
                    color = tmp2
            else:
                continue
            for val in range(len(tmp[q])):
                tmp[q][val] = int((self.srcpal[q][val] * color[val]) / 255)
        im = self.image
        # print(f'pal = {self.srcpal}')
        destpal = [item for sublist in tmp for item in sublist]
        im.putpalette(destpal)
        self.image1 = im.resize((self.width, 256), Image.Resampling.LANCZOS)
        self.image3 = ImageTk.PhotoImage(self.image1, master=self.root)
        if mode == 1:
            # print(f"ind = {ind}")
            self.labels[ind].configure(image=self.image3)
            self.labels[ind].image = self.image3

    def randomizecolors(self):
        self.randcolors = []
        for v in range(8):
            tmp = []
            print('color',v)
            for i in range(4):
                tmp2 = []
                r = random.randrange(80, 256)
                g = random.randrange(80, 256)
                b = random.randrange(80, 256)
                self.hsvcalc([r,g,b])
                tmp2 = [r, g, b]
                tmp.append(tmp2)
            self.randcolors.append(tmp)
        for i in range(8):
            # setup color 5 for each color option
            self.randcolors[i].append([self.randcolors[i][2][2], self.randcolors[i][1][0], self.randcolors[i][0][1]])
        for i in range(4):
            for q in range(2):
                self.updateimages(i, q, self.randcolors, 1)

    def hsvcalc(self,color):
        r = color[0]
        g = color[1]
        b = color[2]
        cmax = max(r,g,b)
        cmin = min(r,g,b)
        delta = cmax-cmin
        # get hue value
        if delta == 0:
            h = 0
        elif cmax == r:
            h = 60*(((g-b)/delta)%6)
        elif cmax == g:
            h = 60*(((b-r)/delta)+2)
        elif cmax == b:
            h = 60*(((r-g)/delta)+4)
        # get saturation
        if cmax==0:
            s = 0
        else:
            s = delta/cmax
        # get v
        h= int(h)
        s =int(s*255)
        v = int((cmax+cmin)/2)
        name,name2 = self.findclosestneighbor([h,s,v])
        #name, name2 = self.findclosestneighbor([r, g, b])
        #name = self.colornamer(h)
        print(f"{int(h)},{s},{int(v)} is {name} of {name2}. RGB: {r},{g},{b}")

    def colornamer(self,hue):
        if hue<=18:
            name='Red'
        elif hue<=45:
            name='Orange'
        elif hue<=74:
            name='Yellow'
        elif hue<=85:
            name='Yellow Green'
        elif hue<=110:
            name='Lime Green'
        elif hue<=150:
            name='Green'
        elif hue<=165:
            name='Teal'
        elif hue<=180:
            name='Turqouise'
        elif hue<=200:
            name='Sky Blue'
        elif hue<=250:
            name='Blue'
        elif hue<=270:
            name='Indigo'
        elif hue<=288:
            name='Purple'
        elif hue<=305:
            name='Magenta'
        elif hue<=330:
            name='Pink'
        elif hue<=360:
            name='Red'
        return name

    def findclosestneighbor(self,color):
        distances =[]
        hues = pickle.load(open('fullhues.pkl','rb'))
        for val in hues:
            hsv2=val[0]
            dists =[]
            for i in range(3):
                if i == 0:
                    v = (hsv2[i]/360-color[i]/360)*255
                    dists.append(v**2)
                else:
                    dists.append((hsv2[i]-color[i])**2)
            dist = abs(math.sqrt(dists[0]+dists[1]+dists[2]))
            distances.append(dist)
        closest = min(distances)
        print(closest)
        ind = distances.index(closest)
        if not isinstance(ind,int):
            if len(ind)>1:
                ind=ind[0]
        name = hues[ind][1]
        name2=hues[ind][2]
        return name,name2


class demowindowicon():
    def __init__(self, image, srcpal, mondata,mode=None):
        root = tk.Toplevel()  # create root window
        root.title("Basic GUI Layout")  # title of the GUI window
        root.maxsize(width=1800, height=800)  # specify the max size the window can expand to
        root.config(bg="skyblue")  # specify background color
        self.colors = [[[157, 106, 184], [105, 187, 147], [217, 224, 238], [135, 194, 124]],
                       [[177, 228, 226], [245, 126, 224], [207, 161, 144], [173, 137, 155]],
                       [[123, 251, 164], [64, 64, 64], [214, 138, 172], [194, 152, 208]],
                       [[243, 109, 114], [83, 113, 189], [248, 216, 48], [184, 108, 120]],
                       [[179, 254, 247], [218, 210, 91], [240, 240, 240], [94, 150, 144]],
                       [[151, 238, 158], [163, 207, 148], [100, 127, 161], [131, 127, 103]],
                       [[240, 240, 240], [93, 251, 255], [98, 239, 139], [248, 94, 160]],
                       [[81, 199, 122], [204, 86, 105], [140, 106, 172], [154, 151, 111]],
                       ]
        if mode is None:
            self.width = 256
        else:
            self.width = 128
        for i in range(8):
            # setup color 5 for each color option
            self.colors[i].append([self.colors[i][2][2], self.colors[i][1][0], self.colors[i][0][1]])
        self.paldata = mondata
        self.root = root
        self.srcpal = srcpal
        self.image = image
        self.labels = []
        for i in range(4):
            self.createpokepics(i)
        randomize = tk.Button(self.root, text="Randomize", command=self.randomizecolors, padx=10, pady=10)
        randomize.grid(column=4, row=0)

    def createpokepics(self, col):
        for row in range(2):
            # self.randomizecolors()
            self.updateimages(col, row)
            self.labels.append(tk.Label(self.root, image=self.image3))
            self.labels[col * 2 + row].grid(row=row, column=col, padx=5, pady=5)
            self.labels[col * 2 + row].image = self.image3

    def updateimages(self, col, row, colors=None, mode=0):
        if colors is None:
            colors = self.colors
        ind = (col * 2) + row  # which pic are we on
        tmp = []
        for val in self.srcpal:
            l = []
            for val2 in val:
                l.append(val2)
            tmp.append(l)
        # this should update the image on the right, should be called after every color update
        pal = []
        # ADD CODE FOR HANDLING OTHER CODES(LIKE BLENDS)
        for q in range(len(tmp)):
            if q == 0:
                continue
            b = False
            i = int(self.paldata[q][0])
            print(i)
            if len(self.paldata[q]) > 1:
                # gets us our blend code
                b = int(self.paldata[q][1])
            if i <= 5 and i > 0:
                # this tells us that depending what zone we need, we get that color
                color = colors[ind][i - 1]
                if b:
                    tmp2 = []
                    # print(f"{b} and this is for slot{q} in zone {i}")
                    if b == 1:
                        for comp in color:
                            # print(f'preadjust = {comp}')
                            comp= int(comp*.7)
                            # print(f'post adjust: {comp}')
                            tmp2.append(comp)
                    elif b == 2:
                        for comp in color:
                            # print(f'preadjust = {comp}')
                            comp= int(comp*.4)
                            # print(f'post adjust: {comp}')
                            tmp2.append(comp)
                    else:
                        tmp2.append(color)
                    color = tmp2
            else:
                if i == 9:
                    color = [248,248,248]
                elif i == 8:
                    if b == 1:
                        color = [
                            48,48,48
                        ]
                    else:
                        color = [16,16,16]
                else:
                    color =self.srcpal[q]
            tmp[q]=color
        im = self.image
        # print(f'pal = {self.srcpal}')
        destpal = [item for sublist in tmp for item in sublist]
        print(destpal)
        im.putpalette(destpal)
        self.image1 = im.resize((self.width, 256), Image.Resampling.LANCZOS)
        self.image3 = ImageTk.PhotoImage(self.image1, master=self.root)
        if mode == 1:
            # print(f"ind = {ind}")
            self.labels[ind].configure(image=self.image3)
            self.labels[ind].image = self.image3

    def randomizecolors(self):
        self.randcolors = []
        for v in range(8):
            tmp = []
            print('color',v)
            for i in range(4):
                tmp2 = []
                r = random.randrange(80, 256)
                g = random.randrange(80, 256)
                b = random.randrange(80, 256)
                self.hsvcalc([r,g,b])
                tmp2 = [r, g, b]
                tmp.append(tmp2)
            self.randcolors.append(tmp)
        for i in range(8):
            # setup color 5 for each color option
            self.randcolors[i].append([self.randcolors[i][2][2], self.randcolors[i][1][0], self.randcolors[i][0][1]])
        for i in range(4):
            for q in range(2):
                self.updateimages(i, q, self.randcolors, 1)

    def hsvcalc(self,color):
        r = color[0]
        g = color[1]
        b = color[2]
        cmax = max(r,g,b)
        cmin = min(r,g,b)
        delta = cmax-cmin
        # get hue value
        if delta == 0:
            h = 0
        elif cmax == r:
            h = 60*(((g-b)/delta)%6)
        elif cmax == g:
            h = 60*(((b-r)/delta)+2)
        elif cmax == b:
            h = 60*(((r-g)/delta)+4)
        # get saturation
        if cmax==0:
            s = 0
        else:
            s = delta/cmax
        # get v
        h= int(h)
        s =int(s*255)
        v = int((cmax+cmin)/2)
        name,name2 = self.findclosestneighbor([h,s,v])
        #name, name2 = self.findclosestneighbor([r, g, b])
        #name = self.colornamer(h)
        print(f"{int(h)},{s},{int(v)} is {name} of {name2}. RGB: {r},{g},{b}")

    def colornamer(self,hue):
        if hue<=18:
            name='Red'
        elif hue<=45:
            name='Orange'
        elif hue<=74:
            name='Yellow'
        elif hue<=85:
            name='Yellow Green'
        elif hue<=110:
            name='Lime Green'
        elif hue<=150:
            name='Green'
        elif hue<=165:
            name='Teal'
        elif hue<=180:
            name='Turqouise'
        elif hue<=200:
            name='Sky Blue'
        elif hue<=250:
            name='Blue'
        elif hue<=270:
            name='Indigo'
        elif hue<=288:
            name='Purple'
        elif hue<=305:
            name='Magenta'
        elif hue<=330:
            name='Pink'
        elif hue<=360:
            name='Red'
        return name

    def findclosestneighbor(self,color):
        distances =[]
        hues = pickle.load(open('fullhues.pkl','rb'))
        for val in hues:
            hsv2=val[0]
            dists =[]
            for i in range(3):
                if i == 0:
                    v = (hsv2[i]/360-color[i]/360)*255
                    dists.append(v**2)
                else:
                    dists.append((hsv2[i]-color[i])**2)
            dist = abs(math.sqrt(dists[0]+dists[1]+dists[2]))
            distances.append(dist)
        closest = min(distances)
        print(closest)
        ind = distances.index(closest)
        if not isinstance(ind,int):
            if len(ind)>1:
                ind=ind[0]
        name = hues[ind][1]
        name2=hues[ind][2]
        return name,name2

class BackupScreen:
    # this screen should generate a list of all backup files and ask which should be loaded
    def __init__(self, mon):
        root = tk.Toplevel()  # create root window
        root.title("Backup A Palette")  # title of the GUI window
        # root.geometry('400x600')  # specify the max size the window can expand to
        root.config(bg="skyblue")  # specify background color
        self.root = root
        self.mon = mon
        self.path1 = "C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{}/normal.pal".format(
            self.mon)
        self.path2 = "C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{}/shiny.pal".format(
            self.mon)
        self.backuppath1 = "C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{}/normalBACKUP".format(
            self.mon)
        self.backuppath2 = "C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{}/shinyBACKUP".format(
            self.mon)
        self.getfiles(self.backuppath1)
        if len(self.names) == 0:
            tk.messagebox.showerror(f'Backup Error', f'Error: No backup entries found for {mon}!')
            self.root.destroy()
            return
        self.root.geometry('600x600')
        self.buttons = []
        global radiovar1
        global radiovar2
        radiovar1 = tk.IntVar()
        radiovar1.set(value=0)
        radiovar2 = tk.IntVar()
        radiovar2.set(value=0)
        # Create left and right frames

        self.left_frame = tk.Frame(root, width=200, height=400)
        self.left_frame.grid(row=1, column=0, padx=10, pady=5)

        self.right_frame = tk.Frame(root, width=200, height=400)
        self.right_frame.grid(row=1, column=1, padx=10, pady=5)
        # label each frame
        lb1 = tk.Label(self.left_frame, text="Normal Pal")
        lb1.grid(row=0, column=0, columnspan=2)
        lb2 = tk.Label(self.right_frame, text="Shiny Pal")
        lb2.grid(row=0, column=0, columnspan=2)

        self.displayfiles(self.left_frame)
        self.getfiles(self.backuppath2)
        self.displayfiles(self.right_frame)
        self.sub1 = tk.Button(self.left_frame, text="Backup Normal Pal", command=self.submitnorm)
        self.sub1.grid(row=99, columnspan=2, column=0)
        self.sub2 = tk.Button(self.right_frame, text="Backup Shiny Pal", command=self.submitshiny)
        self.sub2.grid(row=99, columnspan=2, column=0)

    def getfiles(self, path):
        # this should restore a given backupfile if it exists
        # TO DO: Add a way to only restore one file
        names = []
        for i in range(10):
            if os.path.isfile(path + str(i) + '.pal'):
                # [72:] should display only the relevant path
                backupname = path + str(i) + '.pal'
                names.append(backupname)
        if path == self.backuppath1:
            self.names = names
        else:
            self.shinynames = names

        # open each back up file as a read mode, and overwrite the original files
        """filetorestorenormal = open(self.backuppath1 + backupfile + '.pal','rb')
        filetorestoreshiny = open(self.backuppath1 + backupfile + '.pal','rb')
        filetooverwritenormal = open(self.path1,'wb')
        filetooverwriteshiny = open(self.path2,'wb')
        #backup the normal files before overwriting
        self.backuppalette(self.backuppath1, self.path1)
        self.backuppalette(self.backuppath2, self.path2)
        filetooverwritenormal.write(filetorestorenormal.read())
        print(f"SUCCESS restored backup {backupfile} to normal.pal")
        filetooverwriteshiny.write(filetorestoreshiny.read())
        print(f"SUCCESS restored backup {backupfile} to shiny.pal")
        pass"""

    def displayfiles(self, side):
        i = 0
        buttons = []
        if side == self.left_frame:
            files = self.names
            v = radiovar1
        else:
            files = self.shinynames
            v = radiovar2
        for val in files:
            # tk.Label(side,text=val[69:]).grid(row=i*2,column=1)
            tk.Label(side, text="Modified on " + time.ctime(os.path.getmtime(val))).grid(row=i * 3 + 2, column=1)
            button = tk.Radiobutton(side, text=val[69:], variable=v, value=i)
            buttons.append(button)  # can add a command to dynamically
            button.grid(row=i * 3 + 1, column=1)
            i += 1
        if files == self.names:
            self.normbuttons = buttons
        else:
            self.shinybuttons = buttons

    def submitnorm(self):
        # First save the old one as a back up,
        # then restore the backup over the main one
        self.backuppalette(self.backuppath1, self.path1)
        tk.messagebox.showerror(f'Backup Error', f'Backup {radiovar1.get()} selected', parent=self.root)
        filetorestorenormal = open(self.names[radiovar1.get()], 'rb')
        # filetorestoreshiny = open(self.backuppath1 + backupfile + '.pal','rb')
        filetooverwritenormal = open(self.path1, 'wb')
        # filetooverwriteshiny = open(self.path2,'wb')
        # self.backuppalette(self.backuppath2, self.path2)
        filetooverwritenormal.write(filetorestorenormal.read())
        print(f"SUCCESS restored backup {self.names[radiovar1.get()]} to normal.pal")
        # filetooverwriteshiny.write(filetorestoreshiny.read())
        # print(f"SUCCESS restored backup {backupfile} to shiny.pal")

    def submitshiny(self):
        tk.messagebox.showerror(f'Backup Error', f'Backup {radiovar2.get()} selected', parent=self.root)

    def backuppalette(self, path1, path2):
        # we will create an array of all backup files so we can rotate the oldest out
        files = []
        for i in range(10):
            path1mod = path1 + str(i) + '.pal'
            if os.path.isfile(path1mod):
                files.append(path1mod)
                pass
            else:
                break
        if len(files) >= 10:
            times = []
            # we want to always preserve the original ig
            files.pop(0)
            for path2mod in files:
                ti_m = os.path.getmtime(path2mod)
                times.append(ti_m)
            oldest = min(times)
            ind = times.index(oldest)
            path1mod = files[ind]
        pal = open(path1mod, "wb")
        pal2 = open(path2, 'rb')
        pal.write(pal2.read())
        print(f"Backup was successful of {path1mod}.")


class PalDataScreen:
    def __init__(self, source, mode=None):
        sys.setrecursionlimit(1000)
        root = tk.Toplevel()  # create root window
        root.title("Backup A Palette")  # title of the GUI window
        root.geometry('1000x900')  # specify the max size the window can expand to
        root.config(bg="skyblue")  # specify background color
        self.root = root
        self.mode = mode
        self.mon = source.name
        self.newpaldata = False  # this will get tripped to true if there was no paldata previously, allows proper saving
        self.calc = Calculator(self.mon, self, mode='new')
        self.source = source
        self.label1 = tk.Canvas(self.root, width=256, height=512)
        self.label1.bind("<Button-1>", self.draw)
        self.label1b = tk.Canvas(self.root, width=256, height=256)
        # self.label1b.bind("<B1-Motion>", self.draw)
        self.label1b.bind("<Button-1>", self.drawback)
        self.deletetempfiles()
        if mode == 'normal':
            self.path1 = "C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{}/normal.pal".format(
                self.mon)
        else:
            self.path1 = "C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{}/shiny.pal".format(
                self.mon)
        image1 = Image.open(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front.png")
        self.purefront = image1.copy()
        image1b = Image.open(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/back.png")
        # with open((f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front.png"), "rb") as image:
        #    f = image.read()
        #    for val in f:
        #        print(val)
        self.pureback = image1b.copy()
        self.image_pixel_array_front = self.createpixelarray(image1)
        self.pix_val_flat_front = [x for sets in self.image_pixel_array_front for x in sets]
        self.image_pixel_array_back = self.createpixelarray(image1b)
        self.pix_val_flat_back = [x for sets in self.image_pixel_array_back for x in sets]
        for line in self.image_pixel_array_front:
            print(line)
        self.image1 = image1.resize((256, 512), Image.Resampling.LANCZOS)
        self.image1b = image1b.resize((256, 256), Image.Resampling.LANCZOS)
        if mode == 'normal' or mode is None:
            self.pal = self.calc.srcPalette
        else:
            self.pal = self.calc.destPalette
        self.image = ImageTk.PhotoImage(self.image1, master=root)
        self.imageb = ImageTk.PhotoImage(self.image1b, master=root)
        # self.label1 = tk.Label(root, image=self.image)
        # self.label1.grid(row=0, column=0, padx=5, pady=5)
        # self.label1.image = self.image
        # This was the old method ^ trying out using a canvas v
        self.label1.grid(row=0, column=0, padx=5, pady=5)
        self.label1.create_image(0, 0, anchor=tk.NW, image=self.image)
        # self.label1b = tk.Label(root, image=self.imageb)
        # self.label1b.grid(row=1, column=0, padx=5, pady=5)
        # self.label1b.image = self.imageb
        self.label1b.grid(row=1, column=0, padx=5, pady=5)
        pal = list(self.image1.getpalette())
        print(pal)
        self.label1b.create_image(0, 0, anchor=tk.NW, image=self.imageb)
        self.tool_bar = tk.Frame(master=self.root, width=500, height=600)
        self.tool_bar.grid(row=0, column=2)
        self.image_edit_frame = tk.Frame(master=self.root, width=40, height=600)
        self.image_edit_frame.grid(row=0, column=1)
        self.fill_tool_check = tk.IntVar()
        self.imageeditframesetup()
        self.colors = [[248, 0, 0], [0, 0, 248], [0, 248, 0]]
        self.entries = []  # holds the spinboxes for the color zones
        self.entries2 = []  # holds the spinboxes for the colors
        self.zones = []
        self.image_pal = []
        self.undo_stack = []
        self.undo_limit = 20 #define a max depth for our undo functions
        self.root.bind('<Control-z>', self.undo)
        for val in self.pal:
            self.image_pal.append(val.copy())
        tk.Label(self.tool_bar, text="Colors", anchor='center').grid(row=0, column=0, columnspan=2)
        tk.Label(self.tool_bar, text="src", anchor='center').grid(row=0, column=2, columnspan=1)
        tk.Label(self.tool_bar, text="R", anchor='center').grid(row=0, column=3, columnspan=1)
        tk.Label(self.tool_bar, text="B", anchor='center').grid(row=0, column=4, columnspan=1)
        tk.Label(self.tool_bar, text="G", anchor='center').grid(row=0, column=5, columnspan=1)
        tk.Label(self.tool_bar, text="new", anchor='center').grid(row=0, column=6, columnspan=1)
        tk.Label(self.tool_bar, text="zone", anchor='center').grid(row=0, column=7, columnspan=1)
        tk.Label(self.tool_bar, text="newr", anchor='center').grid(row=0, column=8, columnspan=1)
        tk.Label(self.tool_bar, text="newg", anchor='center').grid(row=0, column=9, columnspan=1)
        tk.Label(self.tool_bar, text="newb", anchor='center').grid(row=0, column=10, columnspan=1)
        tk.Label(self.tool_bar, text="notes", anchor='center').grid(row=0, column=11, columnspan=1)
        global buttonvars
        buttonvars = []
        for i in range(16):
            buttonvars.append(tk.IntVar())
        for i in range(16):
            tk.Label(self.tool_bar, text=f"Color {i}:").grid(row=i + 1, column=0, padx=3, pady=2)
        for i in range(16):
            tmp = self.pal[i]
            txt = f"{tmp[0]}, {tmp[1]}, {tmp[2]}"
            tk.Label(self.tool_bar, text=f"{txt}").grid(row=i + 1, column=1, padx=3, pady=2)
            for j in range(5):
                button = tk.Radiobutton(self.tool_bar, variable=buttonvars[i], value=j, anchor='center',
                                        command=self.updateimage)
                button.grid(row=i + 1, column=2 + j)
            v = tk.Spinbox(self.tool_bar, from_=0, to=99, width=3)
            v.grid(row=i + 1, column=7)
            tk.Entry(self.tool_bar).grid(row=i + 1, column=11)
            self.entries.append(v)
            v.delete(0, tk.END)
            v.insert(0, self.calc.index[i])
            tmp2 = []
            for q in range(3):
                v = tk.Spinbox(self.tool_bar, from_=0, to=255, width=3)
                v.grid(row=i + 1, column=8 + q)
                tmp2.append((v))
                v.delete(0, tk.END)
                v.insert(0, self.pal[i][q])
            self.entries2.append(tmp2)
        tk.Button(self.tool_bar, text='Save .paldata', command=self.submit).grid(row=18, column=1)
        tk.Button(self.tool_bar, text='Save .pal', command=self.submitpal).grid(row=20, column=1)

    def updateimage(self):
        for i in range(16):
            if buttonvars[i].get() == 0:
                self.image_pal[i] = self.pal[i].copy()
            elif buttonvars[i].get() != 4:
                self.image_pal[i] = self.colors[buttonvars[i].get() - 1].copy()
            else:
                tmp = []
                for q in range(3):
                    tmp.append(int(self.entries2[i][q].get()))
                self.image_pal[i] = tmp.copy()
        # we have a temporary file that has the edits made to the canvas on paldata that gets updated every step of the way.
        if os.path.isfile(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/backtemp.png"):
            imb = Image.open(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/backtemp.png")
        else:
            imb = self.image1b
        if os.path.isfile(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front_temp.png"):
            im = Image.open(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front_temp.png")
        else:
            im = self.image1
        # print(f'pal = {self.srcpal}')
        destpal = [item for sublist in self.image_pal for item in sublist]
        im.putpalette(destpal)
        self.image1 = im.resize((256, 512), Image.Resampling.LANCZOS)
        self.image3 = ImageTk.PhotoImage(self.image1, master=self.root)
        self.label1.delete('all')
        self.label1.create_image(0, 0, anchor=tk.NW, image=self.image3)
        # self.label1.image=self.image3
        imb.putpalette(destpal)
        self.label1b.delete('all')
        self.image1b = imb.resize((256, 256), Image.Resampling.LANCZOS)
        self.image3b = ImageTk.PhotoImage(self.image1b, master=self.root)
        # self.label1b.configure(image=self.image3b)
        self.label1b.create_image(0, 0, anchor=tk.NW, image=self.image3b)
        # self.label1b.image=self.image3b
        pass

    def submit(self):
        self.newindex = []
        for entry in self.entries:
            self.newindex.append(entry.get())
        self.savepaldata()

    def submitpal(self):
        self.newpal = []
        for entry in self.entries2:
            tmp = []
            for component in entry:
                tmp.append(int(component.get()))
            self.newpal.append(tmp)
        if self.mode == 'shiny':
            self.savePal(overwriteshiny=True)
        else:
            self.savePal(overwriteshiny=False)

    def savefront(self):
        self.purefront.save(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front.png")
        still = self.purefront.copy().crop((0, 0, 64, 64))
        still.save(f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/front.png")
        tk.messagebox.showinfo("Save Successful!", f"Successfully saved front.png and anim_front.png for {self.mon}",
                               parent=self.root)

    def saveback(self):
        self.pureback.save(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/back.png")
        tk.messagebox.showinfo("Save Successful!", f"Successfully saved back.png for {self.mon}",
                               parent=self.root)

    def savepaldata(self):
        # update so it overwrites if existing paldata
        contents = open("C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/src/data/pokemon/species_info.h", 'rb')
        c = contents.readlines()
        print(bytes(self.newindex[0], 'utf-8'))
        tmp = b''
        for i in range(16):
            tmp += bytes(self.newindex[i], 'utf-8')
            if i != 15:
                tmp += b','
        val = b'        .paldata = {' + tmp + b'},\n'
        i = -1
        for line in c:
            i += 1
            if bytes(self.mon.upper(), 'utf-8') in line:
                break
        if self.newpaldata:
            c.insert(i + 28, val)
        else:
            c[i + 28] = val
        newfile = b''
        for line in c:
            newfile += line
        overwrite = open("C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/src/data/pokemon/species_info.h", 'wb')
        overwrite.write(newfile)
        overwrite.close()
        tk.messagebox.showinfo('Save Successful',
                               f'Save was successful to pokemon_info.h, {self.newindex} written to {self.mon}',
                               parent=self.root)
        print("Save Successful")

    def savePal(self, pal=None, overwriteshiny=True):
        if pal is None:
            pal = self.newpal
        txt = 'JASC-PAL\r\n0100\r\n16\r\n'
        for color in pal:
            txt += "{} {} {}\r\n".format(color[0], color[1], color[2])
        txt2 = bytes(txt, 'utf-8')
        if overwriteshiny:
            self.backuppalette(self.calc.backuppath2, self.calc.path2)
            shinypalfile = open(self.calc.path2, "wb")
            shinypalfile.write(txt2)
            shinypalfile.close()
            print(f"SHINY PAL SAVE SUCCESS :{txt2}")
        else:
            self.backuppalette(self.calc.backuppath1, self.calc.path1)
            normpalfile = open(self.calc.path1, "wb")
            normpalfile.write(txt2)
            normpalfile.close()
            print(f"NORMAL PAL SAVE SUCCESS :{txt2}")

    def backuppalette(self, path1, path2):
        # we will create an array of all backup files so we can rotate the oldest out
        files = []
        for i in range(10):
            path1mod = path1 + str(i) + '.pal'
            if os.path.isfile(path1mod):
                files.append(path1mod)
                pass
            else:
                break
        if len(files) >= 10:
            times = []
            # we want to always preserve the original ig
            files.pop(0)
            for path2mod in files:
                ti_m = os.path.getmtime(path2mod)
                times.append(path2mod)
            oldest = min(times)
            ind = times.index(oldest)
            path1mod = files[ind]
        pal = open(path1mod, "wb")
        pal2 = open(path2, 'rb')
        pal.write(pal2.read())
        pal.close()
        pal2.close()
        print(f"Backup was successful of f{path1mod}.")

    def draw(self, event,mode=0):
        x, y = event.x, event.y
        backupcode = self.pix_val_flat_front.copy()
        self.undo_stack.insert(0,[backupcode,'front'])
        x = x // 4
        y = y // 4
        print(self.fill_tool_check.get())
        if self.fill_tool_check.get() or mode == 1:
            self.flood_fill(y, x, self.image_pixel_array_front, palselected.get(), self.image_pixel_array_front[y][x],self.pix_val_flat_front)
            self.pix_val_flat_front = [x for sets in self.image_pixel_array_front for x in sets]
        else:

            # self.label1.create_rectangle(x*4, y*4, x*4 + 3, y*4 + 3, fill="black")
            self.image_pixel_array_front[y][x] = palselected.get()
            self.pix_val_flat_front[(y * 64) + x] = palselected.get()
            coords = y*64+x
            #backupcode = [[coords],originalcolor,self.pix_val_flat_front]
        self.purefront.putdata(self.pix_val_flat_front)
        self.purefront.save(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front_temp.png")
        self.updateimage()

    def drawback(self, event,mode=0):
        if palselected == 99:
            return
        x, y = event.x, event.y
        backupcode = self.pix_val_flat_back.copy()
        self.undo_stack.insert(0, [backupcode, 'back'])
        x = x // 4
        y = y // 4
        if self.fill_tool_check.get() or mode==1:
            self.flood_fill(y, x, self.image_pixel_array_back, palselected.get(), self.image_pixel_array_back[y][x],self.pix_val_flat_back)
            self.pix_val_flat_back = [x for sets in self.image_pixel_array_back for x in sets]
        else:
        # self.label1b.create_rectangle(x*4, y*4, x*4 + 3, y*4 + 3, fill="black")
            self.image_pixel_array_front[y][x] = palselected.get()
            self.pix_val_flat_back[(y * 64) + x] = palselected.get()

        self.pureback.putdata(self.pix_val_flat_back)
        self.pureback.save(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/backtemp.png")
        self.updateimage()

    def createpixelarray(self, image):
        pix_val = list(image.getdata())
        i = 0
        tmp = []
        arranged_pix_vals = []
        for x in pix_val:
            tmp.append(x)
            i += 1
            if i == 64:
                arranged_pix_vals.append(tmp)
                i = 0
                tmp = []
        return arranged_pix_vals

    def filltool(self, y, x, array, fillval, targetval):
        """x and y are the coords that were clicked, fill val should be the pal data we want to fill with, target is the val at x and y"""
        array[y][x] = fillval
        if y < len(array)-1:
            if (array[y + 1][x] == targetval):
                array[y + 1][x] = fillval
                self.filltool(y + 1, x, array, fillval, targetval)
        if y > 0:
            if (array[y - 1][x] == targetval):
                array[y - 1][x] = fillval
                self.filltool(y - 1, x, array, fillval, targetval)
        if x < len(array[y])-1:
            if (array[y][x + 1] == targetval):
                array[y][x + 1] = fillval
                self.filltool(y, x + 1, array, fillval, targetval)
        if x > 0:
            if (array[y][x - 1] == targetval):
                array[y][x - 1] = fillval
                self.filltool(y, x - 1, array, fillval, targetval)

    def flood_fill(self, start_y,start_x, array, new_color, old_color,flatarray):
        if not array:
            return
        # Get the dimensions of the image
        rows, cols = len(array), len(array[0])

        # Define the four possible neighbors (up, down, left, right)
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Create a stack to store the coordinates to be processed
        stack = [(start_y, start_x)]

        # Get the original color at the starting point
        original_color = array[start_y][start_x]
        if original_color == new_color:
            return

        # Perform iterative flood fill
        while stack:
            y, x = stack.pop()

            # Check if the current cell is within bounds and has the original color
            if 0 <= y < rows and 0 <= x < cols and array[y][x] == original_color:
                # Change the color of the current cell
                array[y][x] = new_color
                # Push neighboring cells onto the stack
                for dy, dx in neighbors:
                    stack.append((y + dy, x + dx))


    def imageeditframesetup(self):
        global palselected
        palselected = tk.IntVar()
        tk.Label(self.image_edit_frame, text="Paint").grid(row=0,column=0)
        for i in range(16):
            button = tk.Radiobutton(self.image_edit_frame, variable=palselected, value=i, anchor='center',
                                    command=self.updateimage)
            button.grid(row=i+1, column=0)
        label = tk.Label(self.image_edit_frame, text='Flood')
        label2 = tk.Checkbutton(self.image_edit_frame,variable=self.fill_tool_check)
        label.grid(row=17, column=0)
        label2.grid(row=18,column=0)
        tk.Button(self.tool_bar, text='Save front .png', command=self.savefront).grid(row=18, column=11)
        tk.Button(self.tool_bar, text='Save back .png', command=self.saveback).grid(row=20, column=11)

    def deletetempfiles(self):
        # temp files used during image editing should be deleted
        if os.path.isfile(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/backtemp.png"):
            os.remove(f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/backtemp.png")
        if os.path.isfile(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front_temp.png"):
            os.remove(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front_temp.png")

    def undo(self,event):
        if self.undo_stack[0][1]=='front':
            print('hi')
            image=self.purefront
            self.pix_val_flat_front=self.undo_stack[0][0]
            i = 0
            stacked=[]
            tmp=[]
            for val in self.pix_val_flat_front:
                tmp.append(val)
                i+=1
                if i == 64:
                    stacked.append(tmp)
                    i = 0
                    tmp=[]
            self.image_pixel_array_front=stacked
            file = f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front_temp.png"
        else:
            image = self.pureback
            self.pix_val_flat_back = self.undo_stack[0][0]
            i = 0
            stacked=[]
            tmp=[]
            for val in self.pix_val_flat_back:
                tmp.append(val)
                i+=1
                if i == 64:
                    stacked.append(tmp)
                    i = 0
                    tmp=[]
            self.image_pixel_array_back=stacked
            file = f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/backtemp.png"
        print(self.undo_stack[0])
        image.putdata(self.undo_stack[0][0])
        image.save(file)
        self.updateimage()
        self.undo_stack = self.undo_stack[1:]

class PalDataScreenWithIcon:
    #need to add the ability to edit the stuff for the icon
    def __init__(self, source, mode=None):
        sys.setrecursionlimit(1000)
        root = tk.Toplevel()  # create root window
        root.title("Backup A Palette")  # title of the GUI window
        root.geometry('2000x2000')  # specify the max size the window can expand to
        root.config(bg="skyblue")  # specify background color
        self.root = root
        self.mode = mode
        self.mon = source.name
        self.newpaldata = False  # this will get tripped to true if there was no paldata previously, allows proper saving
        self.newicondata = False
        self.calc = Calculator(self.mon, self, mode='new')
        self.source = source
        self.label1 = tk.Canvas(self.root, width=256, height=512)
        self.label1.bind("<Button-1>", self.draw)
        self.label1b = tk.Canvas(self.root, width=256, height=256)
        self.labelicon = tk.Canvas(self.root, width=256, height=512)
        # self.label1b.bind("<B1-Motion>", self.draw)
        self.label1b.bind("<Button-1>", self.drawback)
        self.labelicon.bind("<Button-1>",self.drawicon)
        self.deletetempfiles()
        if mode is None:
            self.path1 = "C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{}/normal.pal".format(
                self.mon)
        else:
            self.path1 = "C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{}/shiny.pal".format(
                self.mon)
        image1 = Image.open(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front.png")
        self.purefront = image1.copy()
        image1b = Image.open(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/back.png")
        imageicon = Image.open(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icon.png")
        self.pureicon = imageicon.copy()
        self.pureback = image1b.copy()
        self.image_pixel_array_front = self.createpixelarray(image1)
        self.pix_val_flat_front = [x for sets in self.image_pixel_array_front for x in sets]
        self.image_pixel_array_back = self.createpixelarray(image1b)
        self.pix_val_flat_back = [x for sets in self.image_pixel_array_back for x in sets]
        self.image_pixel_array_icon = self.createpixelarray(imageicon,icon=True)
        self.pix_val_flat_icon = [x for sets in self.image_pixel_array_icon for x in sets]
        self.image1 = image1.resize((256, 512), Image.Resampling.LANCZOS)
        self.image1b = image1b.resize((256, 256), Image.Resampling.LANCZOS)
        self.image1icon = imageicon.resize((256, 512), Image.Resampling.LANCZOS)
        if mode == 'normal' or mode is None:
            self.pal = self.calc.srcPalette
        else:
            self.pal = self.calc.destPalette
        self.image = ImageTk.PhotoImage(self.image1, master=root)
        self.imageb = ImageTk.PhotoImage(self.image1b, master=root)
        self.imageicon = ImageTk.PhotoImage(self.image1icon, master=root)
        self.label1.grid(row=0, column=0, padx=5, pady=5)
        self.label1b.grid(row=1, column=0, padx=5, pady=5)
        self.labelicon.grid(row=0,column=90,padx=5,pady=5)
        self.label1.create_image(0, 0, anchor=tk.NW, image=self.image)
        self.label1b.create_image(0, 0, anchor=tk.NW, image=self.imageb)
        self.labelicon.create_image(0, 0, anchor=tk.NW, image=self.imageicon)
        pal2 = self.image1icon.getpalette()
        self.palicon = []
        tmp =[]
        for val in pal2:
            tmp.append(val)
            if len(tmp)>2:
                self.palicon.append(tmp)
                tmp = []
        print(self.palicon)
        self.tool_bar = tk.Frame(master=self.root, width=500, height=600)
        self.tool_bar.grid(row=0, column=2)
        self.icon_tool_bar = tk.Frame(master=self.root, width=500, height=600)
        self.icon_tool_bar.grid(row=0, column=92)
        self.image_edit_frame = tk.Frame(master=self.root, width=40, height=600)
        self.image_edit_frame.grid(row=0, column=1)
        self.icon_edit_frame = tk.Frame(master=self.root, width=40, height=600)
        self.icon_edit_frame.grid(row=0, column=91)
        self.fill_tool_check = tk.IntVar()
        self.fill_tool_check_icon = tk.IntVar()
        self.imageeditframesetup()
        self.colors = [[248, 0, 0], [0, 0, 248], [0, 248, 0]]
        self.entries = []  # holds the spinboxes for the color zones
        self.entries2 = []  # holds the spinboxes for the colors
        self.icon_entries = []
        self.zones = []
        self.icon_zones = []
        self.image_pal = []
        self.icon_image_pal = []
        self.undo_stack = []
        self.undo_limit = 20 #define a max depth for our undo functions
        self.root.bind('<Control-z>', self.undo)
        for val in self.pal:
            self.image_pal.append(val.copy())
        for val in self.palicon:
            self.icon_image_pal.append(val.copy())
        tk.Label(self.tool_bar, text="Colors", anchor='center').grid(row=0, column=0, columnspan=2)
        tk.Label(self.tool_bar, text="src", anchor='center').grid(row=0, column=2, columnspan=1)
        tk.Label(self.tool_bar, text="R", anchor='center').grid(row=0, column=3, columnspan=1)
        tk.Label(self.tool_bar, text="B", anchor='center').grid(row=0, column=4, columnspan=1)
        tk.Label(self.tool_bar, text="G", anchor='center').grid(row=0, column=5, columnspan=1)
        tk.Label(self.tool_bar, text="new", anchor='center').grid(row=0, column=6, columnspan=1)
        tk.Label(self.tool_bar, text="zone", anchor='center').grid(row=0, column=7, columnspan=1)
        tk.Label(self.tool_bar, text="newr", anchor='center').grid(row=0, column=8, columnspan=1)
        tk.Label(self.tool_bar, text="newg", anchor='center').grid(row=0, column=9, columnspan=1)
        tk.Label(self.tool_bar, text="newb", anchor='center').grid(row=0, column=10, columnspan=1)
        tk.Label(self.tool_bar, text="notes", anchor='center').grid(row=0, column=11, columnspan=1)
        # setup the labels for the icon
        tk.Label(self.icon_tool_bar, text="Colors", anchor='center').grid(row=0, column=0, columnspan=1)
        tk.Label(self.icon_tool_bar, text="src", anchor='center').grid(row=0, column=2, columnspan=1)
        tk.Label(self.icon_tool_bar, text="R", anchor='center').grid(row=0, column=3, columnspan=1)
        tk.Label(self.icon_tool_bar, text="B", anchor='center').grid(row=0, column=4, columnspan=1)
        tk.Label(self.icon_tool_bar, text="G", anchor='center').grid(row=0, column=5, columnspan=1)
        tk.Label(self.icon_tool_bar, text="zone", anchor='center').grid(row=0, column=7, columnspan=1)
        global buttonvars
        buttonvars = []
        global buttonvars2
        buttonvars2 = []
        for i in range(16):
            buttonvars.append(tk.IntVar())
            buttonvars2.append(tk.IntVar())
        for i in range(16):
            tk.Label(self.tool_bar, text=f"Color {i}:").grid(row=i + 1, column=0, padx=3, pady=2)
            tk.Label(self.icon_tool_bar, text=f"Color {i}:").grid(row=i + 1, column=0, padx=3, pady=2)
        for i in range(16):
            tmp = self.pal[i]
            txt = f"{tmp[0]}, {tmp[1]}, {tmp[2]}"
            tk.Label(self.tool_bar, text=f"{txt}").grid(row=i + 1, column=1, padx=3, pady=2)
            for j in range(5):
                button = tk.Radiobutton(self.tool_bar, variable=buttonvars[i], value=j, anchor='center',
                                        command=self.updateimage)
                button.grid(row=i + 1, column=2 + j)
                button2 = tk.Radiobutton(self.icon_tool_bar, variable=buttonvars2[i], value=j, anchor='center',
                                        command=self.updateimageicon)
                button2.grid(row=i + 1, column=2 + j)
            v = tk.Spinbox(self.tool_bar, from_=0, to=99, width=3)
            v.grid(row=i + 1, column=7)
            v2 = tk.Spinbox(self.icon_tool_bar, from_=0, to=99, width=3)
            v2.grid(row=i + 1, column=7)
            tk.Entry(self.tool_bar).grid(row=i + 1, column=11)
            self.entries.append(v)
            self.icon_entries.append(v2)
            v.delete(0, tk.END)
            v.insert(0, self.calc.index[i])
            v2.delete(0, tk.END)
            passes = [0]
            if i == 14 and self.calc.iconindex[i] in passes:
                v2.insert(0, 81)
            elif i == 15 and self.calc.iconindex[i] in passes:
                v2.insert(0, 8)
            else:
                v2.insert(0, self.calc.iconindex[i])
            tmp2 = []
            for q in range(3):
                v = tk.Spinbox(self.tool_bar, from_=0, to=255, width=3)
                v.grid(row=i + 1, column=8 + q)
                tmp2.append((v))
                v.delete(0, tk.END)
                v.insert(0, self.pal[i][q])
            self.entries2.append(tmp2)
        tk.Button(self.tool_bar, text='Save .paldata', command=self.submit).grid(row=18, column=1)
        tk.Button(self.icon_tool_bar, text='Save .iconpal', command=self.submiticon).grid(row=18, column=0)
        tk.Button(self.icon_tool_bar, text='display icon', command=self.rundemo).grid(row=18, column=7)
        tk.Button(self.tool_bar, text='Save .pal', command=self.submitpal).grid(row=20, column=1)
        tk.Button(self.tool_bar,text='Align',command=self.aligncolors).grid(row=18,column=0)
        tk.Button(self.tool_bar, text='Sort', command=self.sortcolors).grid(row=20, column=0)

    def updateimage(self):
        for i in range(16):
            if buttonvars[i].get() == 0:
                self.image_pal[i] = self.pal[i].copy()
            elif buttonvars[i].get() != 4:
                self.image_pal[i] = self.colors[buttonvars[i].get() - 1].copy()
            else:
                tmp = []
                for q in range(3):
                    tmp.append(int(self.entries2[i][q].get()))
                self.image_pal[i] = tmp.copy()
        # we have a temporary file that has the edits made to the canvas on paldata that gets updated every step of the way.
        if os.path.isfile(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/backtemp.png"):
            imb = Image.open(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/backtemp.png")
        else:
            imb = self.image1b
        if os.path.isfile(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front_temp.png"):
            im = Image.open(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front_temp.png")
        else:
            im = self.image1
        # print(f'pal = {self.srcpal}')
        destpal = [item for sublist in self.image_pal for item in sublist]
        im.putpalette(destpal)
        self.image1 = im.resize((256, 512), Image.Resampling.LANCZOS)
        self.image3 = ImageTk.PhotoImage(self.image1, master=self.root)
        self.label1.delete('all')
        self.label1.create_image(0, 0, anchor=tk.NW, image=self.image3)
        # self.label1.image=self.image3
        imb.putpalette(destpal)
        self.label1b.delete('all')
        self.image1b = imb.resize((256, 256), Image.Resampling.LANCZOS)
        self.image3b = ImageTk.PhotoImage(self.image1b, master=self.root)
        # self.label1b.configure(image=self.image3b)
        self.label1b.create_image(0, 0, anchor=tk.NW, image=self.image3b)
        # self.label1b.image=self.image3b

    def updateimageicon(self):
        for i in range(16):
            if buttonvars2[i].get() == 0:
                self.icon_image_pal[i] = self.palicon[i]
            else:
                self.icon_image_pal[i] = self.colors[buttonvars2[i].get() - 1].copy()
        # we have a temporary file that has the edits made to the canvas on paldata that gets updated every step of the way.
        if os.path.isfile(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icontemp.png"):
            imicon = Image.open(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icontemp.png")
        else:
            imicon = self.image1icon
        # print(f'pal = {self.srcpal}')
        destpal = [item for sublist in self.icon_image_pal for item in sublist]
        print(destpal)
        imicon.putpalette(destpal)
        self.image1icon = imicon.resize((256, 512), Image.Resampling.LANCZOS)
        self.image1icon2 = ImageTk.PhotoImage(self.image1icon, master=self.root)
        self.labelicon.delete('all')
        self.labelicon.create_image(0, 0, anchor=tk.NW, image=self.image1icon2)

    def aligncolors(self):
        for i in range(len(buttonvars)):
            buttonvars[i].set(0)
        self.updateimage()

    def sortcolors(self):
        for i in range(len(buttonvars)):
            val = int(self.entries[i].get()[0])
            if val > 3:
                val = 0
            buttonvars[i].set(val)
        self.updateimage()

    def rundemo(self):
        self.newindexicon = []
        for entry in self.icon_entries:
            self.newindexicon.append(entry.get())
        demowindowicon(self.image1icon, self.palicon, self.newindexicon,mode=1)

    def submit(self):
        self.newindex = []
        for entry in self.entries:
            self.newindex.append(entry.get())
        self.savepaldata()

    def submiticon(self):
        self.newindexicon = []
        for entry in self.icon_entries:
            self.newindexicon.append(entry.get())
        self.saveiconpaldata()

    def submitpal(self):
        self.newpal = []
        for entry in self.entries2:
            tmp = []
            for component in entry:
                tmp.append(int(component.get()))
            self.newpal.append(tmp)
        if self.mode == 'shiny':
            self.savePal(overwriteshiny=True)
        else:
            self.savePal(overwriteshiny=False)

    def savefront(self):
        self.purefront.save(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front.png")
        still = self.purefront.copy().crop((0, 0, 64, 64))
        still.save(f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/front.png")
        tk.messagebox.showinfo("Save Successful!", f"Successfully saved front.png and anim_front.png for {self.mon}",
                               parent=self.root)

    def saveback(self):
        self.pureback.save(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/back.png")
        tk.messagebox.showinfo("Save Successful!", f"Successfully saved back.png for {self.mon}",
                               parent=self.root)
    def saveicon(self):
        self.pureicon.save(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icon.png")
        tk.messagebox.showinfo("Save Successful!", f"Successfully saved icon.png for {self.mon}",
                               parent=self.root)

    def savepaldata(self):
        # update so it overwrites if existing paldata
        contents = open("C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/src/data/pokemon/species_info.h", 'rb')
        c = contents.readlines()
        print(bytes(self.newindex[0], 'utf-8'))
        tmp = b''
        for i in range(16):
            tmp += bytes(self.newindex[i], 'utf-8')
            if i != 15:
                tmp += b','
        val = b'        .paldata = {' + tmp + b'},\n'
        i = -1
        for line in c:
            i += 1
            if bytes(self.mon.upper(), 'utf-8') in line:
                break
        if self.newpaldata and self.newicondata:
            c.insert(i + 28, val)
        elif self.newpaldata and not self.newicondata:
            c.insert(i+29,val)
        elif not self.newpaldata and self.newicondata:
            c[i + 28] = val
        else:
            c[i+29]=val
        newfile = b''
        for line in c:
            newfile += line
        overwrite = open("C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/src/data/pokemon/species_info.h", 'wb')
        overwrite.write(newfile)
        overwrite.close()
        tk.messagebox.showinfo('Save Successful',
                               f'Save was successful to pokemon_info.h, {self.newindex} written to {self.mon}',
                               parent=self.root)
        print("Save Successful")
        self.newpaldata = False

    def saveiconpaldata(self):
        # update so it overwrites if existing paldata
        contents = open("C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/src/data/pokemon/species_info.h", 'rb')
        c = contents.readlines()
        tmp = b''
        for i in range(16):
            tmp += bytes(self.newindexicon[i], 'utf-8')
            if i != 15:
                tmp += b','
        val = b'        .iconpal = {' + tmp + b'},\n'
        i = -1
        for line in c:
            i += 1
            if bytes(self.mon.upper(), 'utf-8') in line:
                break
        if self.newicondata:
            c.insert(i + 28, val)
        else:
            c[i + 28] = val
        newfile = b''
        for line in c:
            newfile += line
        overwrite = open("C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/src/data/pokemon/species_info.h", 'wb')
        overwrite.write(newfile)
        overwrite.close()
        tk.messagebox.showinfo('Save Successful',
                               f'Save was successful to pokemon_info.h, {self.newindexicon} written to {self.mon}',
                               parent=self.root)
        print("Save Successful")
        self.newicondata=False

    def savePal(self, pal=None, overwriteshiny=True):
        if pal is None:
            pal = self.newpal
        txt = 'JASC-PAL\r\n0100\r\n16\r\n'
        for color in pal:
            txt += "{} {} {}\r\n".format(color[0], color[1], color[2])
        txt2 = bytes(txt, 'utf-8')
        if overwriteshiny:
            self.backuppalette(self.calc.backuppath2, self.calc.path2)
            shinypalfile = open(self.calc.path2, "wb")
            shinypalfile.write(txt2)
            shinypalfile.close()
            print(f"SHINY PAL SAVE SUCCESS :{txt2}")
        else:
            self.backuppalette(self.calc.backuppath1, self.calc.path1)
            normpalfile = open(self.calc.path1, "wb")
            normpalfile.write(txt2)
            normpalfile.close()
            print(f"NORMAL PAL SAVE SUCCESS :{txt2}")

    def backuppalette(self, path1, path2):
        # we will create an array of all backup files so we can rotate the oldest out
        files = []
        for i in range(10):
            path1mod = path1 + str(i) + '.pal'
            if os.path.isfile(path1mod):
                files.append(path1mod)
                pass
            else:
                break
        if len(files) >= 10:
            times = []
            # we want to always preserve the original ig
            files.pop(0)
            for path2mod in files:
                ti_m = os.path.getmtime(path2mod)
                times.append(path2mod)
            oldest = min(times)
            ind = times.index(oldest)
            path1mod = files[ind]
        pal = open(path1mod, "wb")
        pal2 = open(path2, 'rb')
        pal.write(pal2.read())
        pal.close()
        pal2.close()
        print(f"Backup was successful of f{path1mod}.")

    def draw(self, event,mode=0):
        x, y = event.x, event.y
        backupcode = self.pix_val_flat_front.copy()
        self.undo_stack.insert(0,[backupcode,'front'])
        x = x // 4
        y = y // 4
        print(self.fill_tool_check.get())
        if self.fill_tool_check.get() or mode == 1:
            self.flood_fill(y, x, self.image_pixel_array_front, palselected.get(), self.image_pixel_array_front[y][x],self.pix_val_flat_front)
            self.pix_val_flat_front = [x for sets in self.image_pixel_array_front for x in sets]
        else:

            # self.label1.create_rectangle(x*4, y*4, x*4 + 3, y*4 + 3, fill="black")
            self.image_pixel_array_front[y][x] = palselected.get()
            self.pix_val_flat_front[(y * 64) + x] = palselected.get()
            coords = y*64+x
            #backupcode = [[coords],originalcolor,self.pix_val_flat_front]
        self.purefront.putdata(self.pix_val_flat_front)
        self.purefront.save(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front_temp.png")
        self.updateimage()

    def drawback(self, event,mode=0):
        if palselected == 99:
            return
        x, y = event.x, event.y
        backupcode = self.pix_val_flat_back.copy()
        self.undo_stack.insert(0, [backupcode, 'back'])
        x = x // 4
        y = y // 4
        if self.fill_tool_check.get() or mode==1:
            self.flood_fill(y, x, self.image_pixel_array_back, palselected.get(), self.image_pixel_array_back[y][x],self.pix_val_flat_back)
            self.pix_val_flat_back = [x for sets in self.image_pixel_array_back for x in sets]
        else:
        # self.label1b.create_rectangle(x*4, y*4, x*4 + 3, y*4 + 3, fill="black")
            self.image_pixel_array_front[y][x] = palselected.get()
            self.pix_val_flat_back[(y * 64) + x] = palselected.get()

        self.pureback.putdata(self.pix_val_flat_back)
        self.pureback.save(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/backtemp.png")
        self.updateimage()

    def drawicon(self,event,mode=0):
        if palselectedicon == 99:
            return
        x, y = event.x, event.y
        backupcode = self.pix_val_flat_icon.copy()
        self.undo_stack.insert(0, [backupcode, 'icon'])
        x = x // 8
        y = y // 8
        if self.fill_tool_check_icon.get() or mode == 1:
            self.flood_fill(y, x, self.image_pixel_array_icon, palselectedicon.get(), self.image_pixel_array_icon[y][x],
                            self.pix_val_flat_icon)
            self.pix_val_flat_icon = [x for sets in self.image_pixel_array_icon for x in sets]
        else:
            # self.label1b.create_rectangle(x*4, y*4, x*4 + 3, y*4 + 3, fill="black")
            self.image_pixel_array_icon[y][x] = palselectedicon.get()
            self.pix_val_flat_icon[(y * 32) + x] = palselectedicon.get()

        self.pureicon.putdata(self.pix_val_flat_icon)
        self.pureicon.save(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icontemp.png")
        self.updateimageicon()

    def createpixelarray(self, image,icon=False):
        if icon:
            width = 32
        else:
            width = 64
        pix_val = list(image.getdata())
        i = 0
        tmp = []
        arranged_pix_vals = []
        for x in pix_val:
            tmp.append(x)
            i += 1
            if i == width:
                arranged_pix_vals.append(tmp)
                i = 0
                tmp = []
        return arranged_pix_vals

    def filltool(self, y, x, array, fillval, targetval):
        array[y][x] = fillval
        if y < len(array)-1:
            if (array[y + 1][x] == targetval):
                array[y + 1][x] = fillval
                self.filltool(y + 1, x, array, fillval, targetval)
        if y > 0:
            if (array[y - 1][x] == targetval):
                array[y - 1][x] = fillval
                self.filltool(y - 1, x, array, fillval, targetval)
        if x < len(array[y])-1:
            if (array[y][x + 1] == targetval):
                array[y][x + 1] = fillval
                self.filltool(y, x + 1, array, fillval, targetval)
        if x > 0:
            if (array[y][x - 1] == targetval):
                array[y][x - 1] = fillval
                self.filltool(y, x - 1, array, fillval, targetval)

    def flood_fill(self, start_y,start_x, array, new_color, old_color,flatarray):
        if not array:
            return
        # Get the dimensions of the image
        rows, cols = len(array), len(array[0])

        # Define the four possible neighbors (up, down, left, right)
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Create a stack to store the coordinates to be processed
        stack = [(start_y, start_x)]

        # Get the original color at the starting point
        original_color = array[start_y][start_x]
        if original_color == new_color:
            return

        # Perform iterative flood fill
        while stack:
            y, x = stack.pop()

            # Check if the current cell is within bounds and has the original color
            if 0 <= y < rows and 0 <= x < cols and array[y][x] == original_color:
                # Change the color of the current cell
                array[y][x] = new_color
                # Push neighboring cells onto the stack
                for dy, dx in neighbors:
                    stack.append((y + dy, x + dx))


    def imageeditframesetup(self):
        global palselected
        palselected = tk.IntVar()
        global palselectedicon
        palselectedicon = tk.IntVar()
        tk.Label(self.image_edit_frame, text="Paint").grid(row=0,column=0)
        tk.Label(self.icon_edit_frame, text="Paint").grid(row=0, column=0)
        for i in range(16):
            button = tk.Radiobutton(self.image_edit_frame, variable=palselected, value=i, anchor='center',
                                    command=self.updateimage)
            button.grid(row=i+1, column=0)
            button_icon = tk.Radiobutton(self.icon_edit_frame, variable=palselectedicon, value=i, anchor='center',
                                    command=self.updateimageicon)
            button_icon.grid(row=i+1, column=0)
        label = tk.Label(self.image_edit_frame, text='Flood')
        label2 = tk.Checkbutton(self.image_edit_frame,variable=self.fill_tool_check)
        labelicon = tk.Label(self.icon_edit_frame, text='Flood')
        label2icon = tk.Checkbutton(self.icon_edit_frame,variable=self.fill_tool_check_icon)
        label.grid(row=17, column=0)
        label2.grid(row=18,column=0)
        labelicon.grid(row=17, column=0)
        label2icon.grid(row=18,column=0)
        tk.Button(self.tool_bar, text='Save front .png', command=self.savefront).grid(row=18, column=11)
        tk.Button(self.tool_bar, text='Save back .png', command=self.saveback).grid(row=20, column=11)
        tk.Button(self.icon_tool_bar, text='Save icon .png', command=self.saveicon).grid(row=20, column=0)

    def deletetempfiles(self):
        # temp files used during image editing should be deleted
        if os.path.isfile(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/backtemp.png"):
            os.remove(f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/backtemp.png")
        if os.path.isfile(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front_temp.png"):
            os.remove(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front_temp.png")

    def undo(self,event):
        if self.undo_stack[0][1]=='front':
            print('hi')
            image=self.purefront
            self.pix_val_flat_front=self.undo_stack[0][0]
            i = 0
            stacked=[]
            tmp=[]
            for val in self.pix_val_flat_front:
                tmp.append(val)
                i+=1
                if i == 64:
                    stacked.append(tmp)
                    i = 0
                    tmp=[]
            self.image_pixel_array_front=stacked
            file = f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/anim_front_temp.png"
        elif self.undo_stack[0][1]=='icon':
            image = self.pureicon
            self.pix_val_flat_icon = self.undo_stack[0][0]
            i = 0
            stacked=[]
            tmp=[]
            for val in self.pix_val_flat_icon:
                tmp.append(val)
                i+=1
                if i == 32:
                    stacked.append(tmp)
                    i = 0
                    tmp=[]
            self.image_pixel_array_icon=stacked
            file = f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icontemp.png"
        else:
            image = self.pureback
            self.pix_val_flat_back = self.undo_stack[0][0]
            i = 0
            stacked=[]
            tmp=[]
            for val in self.pix_val_flat_back:
                tmp.append(val)
                i+=1
                if i == 64:
                    stacked.append(tmp)
                    i = 0
                    tmp=[]
            self.image_pixel_array_back=stacked
            file = f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/backtemp.png"
        print(self.undo_stack[0])
        image.putdata(self.undo_stack[0][0])
        image.save(file)
        self.updateimage()
        self.updateimageicon()
        self.undo_stack = self.undo_stack[1:]


class IconScreen:
    def __init__(self, source, mode=None):
        sys.setrecursionlimit(1000)
        root = tk.Toplevel()  # create root window
        root.title("Backup A Palette")  # title of the GUI window
        root.geometry('1000x900')  # specify the max size the window can expand to
        root.config(bg="skyblue")  # specify background color
        self.root = root
        self.mode = mode
        self.mon = source.name
        self.newicondata = False  # this will get tripped to true if there was no paldata previously, allows proper saving
        self.calc = Calculator(self.mon, self, mode='new')
        self.source = source
        self.label1 = tk.Canvas(self.root, width=256, height=512)
        self.label1.bind("<Button-1>", self.draw)
        #self.label1b = tk.Canvas(self.root, width=256, height=256)
        # self.label1b.bind("<B1-Motion>", self.draw)
        #self.label1b.bind("<Button-1>", self.drawback)
        self.deletetempfiles()
        if mode == 'normal':
            self.path1 = "C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{}/normal.pal".format(
                self.mon)
        else:
            self.path1 = "C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{}/shiny.pal".format(
                self.mon)
        image1 = Image.open(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icon.png")
        self.purefront = image1.copy()
        image1b = Image.open(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icon.png")

        self.pureback = image1b.copy()
        self.image_pixel_array_front = self.createpixelarray(image1)
        self.pix_val_flat_front = [x for sets in self.image_pixel_array_front for x in sets]
        self.image_pixel_array_back = self.createpixelarray(image1b)
        self.pix_val_flat_back = [x for sets in self.image_pixel_array_back for x in sets]
        for line in self.image_pixel_array_front:
            print(line)
        self.image1 = image1.resize((256, 512), Image.Resampling.LANCZOS)
        self.image1b = image1b.resize((256, 256), Image.Resampling.LANCZOS)
        if mode == 'normal' or mode is None:
            self.pal = self.calc.srcPalette
        else:
            self.pal = self.calc.destPalette
        self.image = ImageTk.PhotoImage(self.image1, master=root)
        self.imageb = ImageTk.PhotoImage(self.image1b, master=root)
        # self.label1 = tk.Label(root, image=self.image)
        # self.label1.grid(row=0, column=0, padx=5, pady=5)
        # self.label1.image = self.image
        # This was the old method ^ trying out using a canvas v
        self.label1.grid(row=0, column=0, padx=5, pady=5)
        self.label1.create_image(0, 0, anchor=tk.NW, image=self.image)
        # self.label1b = tk.Label(root, image=self.imageb)
        # self.label1b.grid(row=1, column=0, padx=5, pady=5)
        # self.label1b.image = self.imageb
        #self.label1b.grid(row=1, column=0, padx=5, pady=5)
        pal = list(self.image1.getpalette())
        pal2 = self.image1.getpalette()
        self.pal = []
        tmp =[]
        for val in pal2:
            tmp.append(val)
            if len(tmp)>2:
                self.pal.append(tmp)
                tmp = []
        print("Hey",self.pal)
        #self.label1b.create_image(0, 0, anchor=tk.NW, image=self.imageb)
        self.tool_bar = tk.Frame(master=self.root, width=500, height=600)
        self.tool_bar.grid(row=0, column=2)
        self.image_edit_frame = tk.Frame(master=self.root, width=40, height=600)
        self.image_edit_frame.grid(row=0, column=1)
        self.fill_tool_check = tk.IntVar()
        self.imageeditframesetup()
        self.colors = [[248, 0, 0], [0, 0, 248], [0, 248, 0]]
        self.entries = []  # holds the spinboxes for the color zones
        self.entries2 = []  # holds the spinboxes for the colors
        self.zones = []
        self.image_pal = []
        self.undo_stack = []
        self.undo_limit = 20 #define a max depth for our undo functions
        self.root.bind('<Control-z>', self.undo)
        for val in self.pal:
            self.image_pal.append(val.copy())
        tk.Label(self.tool_bar, text="Colors", anchor='center').grid(row=0, column=0, columnspan=2)
        tk.Label(self.tool_bar, text="src", anchor='center').grid(row=0, column=2, columnspan=1)
        tk.Label(self.tool_bar, text="R", anchor='center').grid(row=0, column=3, columnspan=1)
        tk.Label(self.tool_bar, text="B", anchor='center').grid(row=0, column=4, columnspan=1)
        tk.Label(self.tool_bar, text="G", anchor='center').grid(row=0, column=5, columnspan=1)
        tk.Label(self.tool_bar, text="new", anchor='center').grid(row=0, column=6, columnspan=1)
        tk.Label(self.tool_bar, text="zone", anchor='center').grid(row=0, column=7, columnspan=1)
        tk.Label(self.tool_bar, text="newr", anchor='center').grid(row=0, column=8, columnspan=1)
        tk.Label(self.tool_bar, text="newg", anchor='center').grid(row=0, column=9, columnspan=1)
        tk.Label(self.tool_bar, text="newb", anchor='center').grid(row=0, column=10, columnspan=1)
        tk.Label(self.tool_bar, text="notes", anchor='center').grid(row=0, column=11, columnspan=1)
        global buttonvars2
        buttonvars2 = []
        for i in range(16):
            buttonvars2.append(tk.IntVar())
        for i in range(16):
            tk.Label(self.tool_bar, text=f"Color {i}:").grid(row=i + 1, column=0, padx=3, pady=2)
        for i in range(16):
            tmp = self.pal[i]
            txt = f"{tmp[0]}, {tmp[1]}, {tmp[2]}"
            tk.Label(self.tool_bar, text=f"{txt}").grid(row=i + 1, column=1, padx=3, pady=2)
            for j in range(5):
                button = tk.Radiobutton(self.tool_bar, variable=buttonvars2[i], value=j, anchor='center',
                                        command=self.updateimage)
                button.grid(row=i + 1, column=2 + j)
            v = tk.Spinbox(self.tool_bar, from_=0, to=99, width=3)
            v.grid(row=i + 1, column=7)
            tk.Entry(self.tool_bar).grid(row=i + 1, column=11)
            self.entries.append(v)
            v.delete(0, tk.END)
            v.insert(0, 0)
            tmp2 = []
            for q in range(3):
                v = tk.Spinbox(self.tool_bar, from_=0, to=255, width=3)
                v.grid(row=i + 1, column=8 + q)
                tmp2.append((v))
                v.delete(0, tk.END)
                v.insert(0, self.pal[i][q])
            self.entries2.append(tmp2)
        tk.Button(self.tool_bar, text='Save .paldata', command=self.submit).grid(row=18, column=1)
        #tk.Button(self.tool_bar, text='Save .pal', command=self.submitpal).grid(row=20, column=1)

    def updateimage(self):
        for i in range(16):
            if buttonvars2[i].get() == 0:
                self.image_pal[i] = self.pal[i].copy()
            elif buttonvars2[i].get() != 4:
                self.image_pal[i] = self.colors[buttonvars2[i].get() - 1].copy()
            else:
                tmp = []
                for q in range(3):
                    tmp.append(int(self.entries2[i][q].get()))
                self.image_pal[i] = tmp.copy()
        # we have a temporary file that has the edits made to the canvas on paldata that gets updated every step of the way.
        if os.path.isfile(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icontemp.png"):
            imb = Image.open(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icontemp.png")
        else:
            imb = self.image1b
        if os.path.isfile(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icon_temp.png"):
            im = Image.open(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icon_temp.png")
        else:
            im = self.image1
        # print(f'pal = {self.srcpal}')
        destpal = [item for sublist in self.image_pal for item in sublist]
        im.putpalette(destpal)
        self.image1 = im.resize((256, 512), Image.Resampling.LANCZOS)
        self.image3 = ImageTk.PhotoImage(self.image1, master=self.root)
        self.label1.delete('all')
        self.label1.create_image(0, 0, anchor=tk.NW, image=self.image3)
        # self.label1.image=self.image3
        imb.putpalette(destpal)
        #self.label1b.delete('all')
        self.image1b = imb.resize((256, 256), Image.Resampling.LANCZOS)
        self.image3b = ImageTk.PhotoImage(self.image1b, master=self.root)
        # self.label1b.configure(image=self.image3b)
        #self.label1b.create_image(0, 0, anchor=tk.NW, image=self.image3b)
        # self.label1b.image=self.image3b
        pass

    def submit(self):
        self.newindex = []
        for entry in self.entries:
            self.newindex.append(entry.get())
        self.savepaldata()

    def submitpal(self):
        self.newpal = []
        for entry in self.entries2:
            tmp = []
            for component in entry:
                tmp.append(int(component.get()))
            self.newpal.append(tmp)
        if self.mode == 'shiny':
            self.savePal(overwriteshiny=True)
        else:
            self.savePal(overwriteshiny=False)

    def savefront(self):
        self.purefront.save(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icon.png")
        tk.messagebox.showinfo("Save Successful!", f"Successfully saved front.png and anim_front.png for {self.mon}",
                               parent=self.root)

    def saveback(self):
        self.pureback.save(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icon.png")
        tk.messagebox.showinfo("Save Successful!", f"Successfully saved back.png for {self.mon}",
                               parent=self.root)

    def savepaldata(self):
        # update so it overwrites if existing paldata
        contents = open("C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/src/data/pokemon/species_info.h", 'rb')
        c = contents.readlines()
        print(bytes(self.newindex[0], 'utf-8'))
        tmp = b''
        for i in range(16):
            tmp += bytes(self.newindex[i], 'utf-8')
            if i != 15:
                tmp += b','
        val = b'        .iconpal = {' + tmp + b'},\n'
        i = -1
        for line in c:
            i += 1
            if bytes(self.mon.upper(), 'utf-8') in line:
                break
        if not self.newicondata:
            c.insert(i + 28, val)
            print('overwrote')
        else:
            c[i + 28] = val
        newfile = b''
        for line in c:
            newfile += line
        overwrite = open("C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/src/data/pokemon/species_info.h", 'wb')
        overwrite.write(newfile)
        overwrite.close()
        tk.messagebox.showinfo('Save Successful',
                               f'Save was successful to pokemon_info.h, {self.newindex} written to {self.mon}',
                               parent=self.root)
        print("Save Successful")

    def savePal(self, pal=None, overwriteshiny=True):
        if pal is None:
            pal = self.newpal
        txt = 'JASC-PAL\r\n0100\r\n16\r\n'
        for color in pal:
            txt += "{} {} {}\r\n".format(color[0], color[1], color[2])
        txt2 = bytes(txt, 'utf-8')
        if overwriteshiny:
            self.backuppalette(self.calc.backuppath2, self.calc.path2)
            shinypalfile = open(self.calc.path2, "wb")
            shinypalfile.write(txt2)
            shinypalfile.close()
            print(f"SHINY PAL SAVE SUCCESS :{txt2}")
        else:
            self.backuppalette(self.calc.backuppath1, self.calc.path1)
            normpalfile = open(self.calc.path1, "wb")
            normpalfile.write(txt2)
            normpalfile.close()
            print(f"NORMAL PAL SAVE SUCCESS :{txt2}")

    def backuppalette(self, path1, path2):
        # we will create an array of all backup files so we can rotate the oldest out
        files = []
        for i in range(10):
            path1mod = path1 + str(i) + '.pal'
            if os.path.isfile(path1mod):
                files.append(path1mod)
                pass
            else:
                break
        if len(files) >= 10:
            times = []
            # we want to always preserve the original ig
            files.pop(0)
            for path2mod in files:
                ti_m = os.path.getmtime(path2mod)
                times.append(path2mod)
            oldest = min(times)
            ind = times.index(oldest)
            path1mod = files[ind]
        pal = open(path1mod, "wb")
        pal2 = open(path2, 'rb')
        pal.write(pal2.read())
        pal.close()
        pal2.close()
        print(f"Backup was successful of f{path1mod}.")

    def draw(self, event,mode=0):
        x, y = event.x, event.y
        backupcode = self.pix_val_flat_front.copy()
        self.undo_stack.insert(0,[backupcode,'front'])
        x = x // 8
        y = y // 8
        print(self.fill_tool_check.get())
        if self.fill_tool_check.get() or mode == 1:
            self.flood_fill(y, x, self.image_pixel_array_front, palselected2.get(), self.image_pixel_array_front[y][x],self.pix_val_flat_front)
            self.pix_val_flat_front = [x for sets in self.image_pixel_array_front for x in sets]
        else:

            # self.label1.create_rectangle(x*4, y*4, x*4 + 3, y*4 + 3, fill="black")
            self.image_pixel_array_front[y][x] = palselected2.get()
            self.pix_val_flat_front[(y * 32) + x] = palselected2.get()
            coords = y*32+x
            #backupcode = [[coords],originalcolor,self.pix_val_flat_front]
        self.purefront.putdata(self.pix_val_flat_front)
        self.purefront.save(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icon_temp.png")
        self.updateimage()

    def drawback(self, event,mode=0):
        if palselected2 == 99:
            return
        x, y = event.x, event.y
        backupcode = self.pix_val_flat_back.copy()
        self.undo_stack.insert(0, [backupcode, 'back'])
        x = x // 8
        y = y // 8
        if self.fill_tool_check.get() or mode==1:
            self.flood_fill(y, x, self.image_pixel_array_back, palselected2.get(), self.image_pixel_array_back[y][x],self.pix_val_flat_back)
            self.pix_val_flat_back = [x for sets in self.image_pixel_array_back for x in sets]
        else:
        # self.label1b.create_rectangle(x*4, y*4, x*4 + 3, y*4 + 3, fill="black")
            self.image_pixel_array_front[y][x] = palselected2.get()
            self.pix_val_flat_back[(y * 32) + x] = palselected2.get()

        self.pureback.putdata(self.pix_val_flat_back)
        self.pureback.save(
            f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icontemp.png")
        self.updateimage()

    def createpixelarray(self, image):
        pix_val = list(image.getdata())
        i = 0
        tmp = []
        arranged_pix_vals = []
        for x in pix_val:
            tmp.append(x)
            i += 1
            if i == 32:
                arranged_pix_vals.append(tmp)
                i = 0
                tmp = []
        return arranged_pix_vals

    def filltool(self, y, x, array, fillval, targetval):
        """x and y are the coords that were clicked, fill val should be the pal data we want to fill with, target is the val at x and y"""
        array[y][x] = fillval
        if y < len(array)-1:
            if (array[y + 1][x] == targetval):
                array[y + 1][x] = fillval
                self.filltool(y + 1, x, array, fillval, targetval)
        if y > 0:
            if (array[y - 1][x] == targetval):
                array[y - 1][x] = fillval
                self.filltool(y - 1, x, array, fillval, targetval)
        if x < len(array[y])-1:
            if (array[y][x + 1] == targetval):
                array[y][x + 1] = fillval
                self.filltool(y, x + 1, array, fillval, targetval)
        if x > 0:
            if (array[y][x - 1] == targetval):
                array[y][x - 1] = fillval
                self.filltool(y, x - 1, array, fillval, targetval)

    def flood_fill(self, start_y,start_x, array, new_color, old_color,flatarray):
        if not array:
            return
        # Get the dimensions of the image
        rows, cols = len(array), len(array[0])

        # Define the four possible neighbors (up, down, left, right)
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Create a stack to store the coordinates to be processed
        stack = [(start_y, start_x)]

        # Get the original color at the starting point
        original_color = array[start_y][start_x]
        if original_color == new_color:
            return

        # Perform iterative flood fill
        while stack:
            y, x = stack.pop()

            # Check if the current cell is within bounds and has the original color
            if 0 <= y < rows and 0 <= x < cols and array[y][x] == original_color:
                # Change the color of the current cell
                array[y][x] = new_color
                # Push neighboring cells onto the stack
                for dy, dx in neighbors:
                    stack.append((y + dy, x + dx))


    def imageeditframesetup(self):
        global palselected2
        palselected2 = tk.IntVar()
        tk.Label(self.image_edit_frame, text="Paint").grid(row=0,column=0)
        for i in range(16):
            button = tk.Radiobutton(self.image_edit_frame, variable=palselected2, value=i, anchor='center',
                                    command=self.updateimage)
            button.grid(row=i+1, column=0)
        label = tk.Label(self.image_edit_frame, text='Flood')
        label2 = tk.Checkbutton(self.image_edit_frame,variable=self.fill_tool_check)
        label.grid(row=17, column=0)
        label2.grid(row=18,column=0)
        tk.Button(self.tool_bar, text='Save front .png', command=self.savefront).grid(row=18, column=11)
        #tk.Button(self.tool_bar, text='Save back .png', command=self.saveback).grid(row=20, column=11)

    def deletetempfiles(self):
        # temp files used during image editing should be deleted
        if os.path.isfile(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icontemp.png"):
            os.remove(f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icontemp.png")
        if os.path.isfile(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icon_temp.png"):
            os.remove(
                f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icon_temp.png")

    def undo(self,event):
        if self.undo_stack[0][1]=='front':
            print('hi')
            image=self.purefront
            self.pix_val_flat_front=self.undo_stack[0][0]
            i = 0
            stacked=[]
            tmp=[]
            for val in self.pix_val_flat_front:
                tmp.append(val)
                i+=1
                if i == 32:
                    stacked.append(tmp)
                    i = 0
                    tmp=[]
            self.image_pixel_array_front=stacked
            file = f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icon_temp.png"
        else:
            image = self.pureback
            self.pix_val_flat_back = self.undo_stack[0][0]
            i = 0
            stacked=[]
            tmp=[]
            for val in self.pix_val_flat_back:
                tmp.append(val)
                i+=1
                if i == 32:
                    stacked.append(tmp)
                    i = 0
                    tmp=[]
            self.image_pixel_array_back=stacked
            file = f"C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{self.mon}/icontemp.png"
        print(self.undo_stack[0])
        image.putdata(self.undo_stack[0][0])
        image.save(file)
        self.updateimage()
        self.undo_stack = self.undo_stack[1:]


screens = []
while True:
    if not screens:
        screen = MainScreen()
        screens.append(screen)
        screen.window.mainloop()
