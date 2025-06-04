"""So the basic algorithm should be: 1. get the current palette 2. get the paldata (MUST BE HAND GENERATED PRIOR TO
EXECUTING SCRIPT) 3. group the palette into each individual color 4. get the lightest color in that color group (
probably by averaging - this could cause a conflict if a color is set to be blended with another color? - this is the
primary mask and will be set to 255 255 255 at end of routine 5. find out which of the 3 colors in that are the
largest, mid, small (or tie? this could solve an issue with not knowing which color to decrement) 6. apply the mask
onto each of the other colors in the group -make sure that the integrity of the color ordering is maintained. the mid
color should not be the largest color later -if a color fails this test, ask user for input on how to handle the
error -wait to resolve this until all other colors have been resolved -display all properly resolved colors in log
for user to make an informed decision -test to make sure that a color val is not 0 -if it is, ask user for input on
handling in same manner 7. set the mask equal to 255 255 255 8. organize the data into a pal file 9. write to the
proper folder """
import os
import tkinter as tk
class Calculator:
    def __init__(self,mon,srcwindow=None,mode=None):
        #pass 'new to mode in order to get the correct behavior for entering new paldata
        super().__init__()
        if mode:
            self.mode=mode
        else:
            self.mode=0
        self.srcwindow = srcwindow
        self.mon = mon
        self.path1 = "C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{}/normal.pal".format(self.mon)
        self.path2 = "C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{}/shiny.pal".format(self.mon)
        self.backuppath1 = "C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{}/normalBACKUP".format(self.mon)
        self.backuppath2 = "C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/graphics/pokemon/{}/shinyBACKUP".format(self.mon)
        self.normpalfile = open(self.path1, "rb")
        self.pokedata = open("C:/Users/zashe/OneDrive/Desktop/decomps/pokeemerald/src/data/pokemon/species_info.h",'rb')
        self.colormasks = [0]
        self.header = b''
        self.passes = ['3','4','5','6', '7', '8', '9'] #codes that dont get masked
        self.getpal()
        self.getColorList()
        self.getpal(1)

    def overwriteNormalPal(self):
        self.arrangeColors(self.srcPalette)
        self.getcolororder()
        self.applyMasks()
        #self.savePal(overwriteshiny=False)
        self.clearself()

    def overWriteShinyPal(self):
        self.arrangeColors(self.srcPalette)
        self.getcolororder()
        self.applyMasks(mode=1)
        #self.savePal()
        self.clearself()

    def clearself(self):
        self.colormasks = [0]
        self.normpalfile = open(self.path1, "rb")
        self.getpal()
        self.getColorList()
        self.getpal(1)

    def getpal(self,mode=0):
        #this function will simply gather the palette data and create an array[16][3] of the data
        #mode 0 is for the normal pal, anything else is for the shiny pal
        i = 0
        if mode == 0:
            pal = self.normpalfile
            self.srcPalette = []  # this should be a 16 entry array by the end, each entry should have 3 vals
        else:
            self.shinypalfile = open(self.path2, "rb")
            pal = self.shinypalfile
            self.destPalette = []
        tmp = ''
        sourcepal = b''
        shinyPalette = []
        while True:
            line = pal.readline()
            if not line:
                break
            sourcepal += line
        sourcepal = sourcepal[20:].decode()
        color = []
        for char in sourcepal:
            if char == '\n':
                i += 1
                if mode == 0:
                    self.srcPalette.append(color)
                else:
                    self.destPalette.append(color)
                color = []
                tmp = ''
            elif char == ' ' or char == "\r":
                if tmp:
                    color.append(int(tmp))
                    tmp = ''
            else:
                # print(tmp)
                tmp += char

    def getColorList(self):
        #this will read the pokemoninfo.h file into binary, then pass that into a searcher.
        q = 0
        i = 0
        tmp = ''
        sourcefile = b''
        while True:
            line = self.pokedata.readline()
            if not line:
                break
            sourcefile += line
        sourcefile = sourcefile.decode()
        self.retColorIndex((sourcefile))
        self.retColorIndexIcon((sourcefile))

    def retColorIndexIcon(self,decodefile):
        #this should just get an array of the paldata
        #we have to declare a lot of variables to help with the search
        #tmp checks for mon name, tmp2 for paldata, and tmp3 holds the actual values in paldata
        #the founds are for if we have found the mon and then paldata in the file
        monname = self.mon.upper()
        index = []
        tmp = ''
        tmp2 = ''
        tmp3 = ''
        counter = 0 # this will handle if I haven't put in pal data yet
        counter2 = 0
        p = 'iconpal'
        found = False
        found2 = False
        i = 0
        for char in decodefile:
            if not found:
                #this progressively scans for the monname
                if char == monname[i]:
                    i += 1
                    tmp += char
                    #if we have found the monname, we now search for paldata
                    if tmp == monname:
                        found = True
                        tmp = ''
                        i = 0
                else:
                    i = 0
                    tmp = ''
            elif not found2:
                counter += 1
                if char == p[i]:
                    i += 1
                    tmp2 += char
                    #if we have found 'iconpal' now we can start looking for the actual data contained inside
                    if tmp2 == p:
                        found2 = True
                else:
                    i = 0
                    tmp2 = ''
                if counter == 1000:
                    print("Exception found, generating blank val for icon data")
                    self.iconindex = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                    self.srcwindow.newicondata = True
                    return
            else:
                #pretty much only allows the actual data to be passed in
                if char in ('0','1','2','3','4','5','6','7','8','9'):
                    counter2 += 1
                    tmp3 += char
                else:
                    #if we reached a nondata character, lets check our tmp val and see if it contains data
                    #if we can int the characters, we add it into our index
                    try:
                        int(tmp3)
                        index.append(tmp3)
                        tmp3 = ''
                    except:
                        tmp3 = ''
                        pass
            if counter2 == 50:
                raise Exception(f"Could not locate appropriate paldata. FILE KEPT READIING BEYONG {counter2} CHARACTERS AFTER PALDATA")
            if len(index) == 16:
                #we only want a hard 16 entries
                self.iconindex = index
                break

    def retColorIndex(self,decodefile):
        #this should just get an array of the paldata
        #we have to declare a lot of variables to help with the search
        #tmp checks for mon name, tmp2 for paldata, and tmp3 holds the actual values in paldata
        #the founds are for if we have found the mon and then paldata in the file
        monname = self.mon.upper()
        index = []
        tmp = ''
        tmp2 = ''
        tmp3 = ''
        counter = 0 # this will handle if I haven't put in pal data yet
        counter2 = 0
        p = 'paldata'
        found = False
        found2 = False
        i = 0
        for char in decodefile:
            if not found:
                #this progressively scans for the monname
                if char == monname[i]:
                    i += 1
                    tmp += char
                    #if we have found the monname, we now search for paldata
                    if tmp == monname:
                        found = True
                        tmp = ''
                        i = 0
                else:
                    i = 0
                    tmp = ''
            elif not found2:
                counter += 1
                if char == p[i]:
                    i += 1
                    tmp2 += char
                    #if we have found 'paldata' now we can start looking for the actual data contained inside
                    if tmp2 == p:
                        found2 = True
                else:
                    i = 0
                    tmp2 = ''
                if counter == 1100 and self.mode !='new':
                    raise Exception(f"Could not locate appropriate paldata. FILE KEPT READIING BEYONG {counter} CHARACTERS AFTER NAME")
                if counter == 1100 and self.mode =='new':
                    print("Exception found, generating blank val")
                    self.index = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                    self.srcwindow.newpaldata = True
                    return
            else:
                #pretty much only allows the actual data to be passed in
                if char in ('0','1','2','3','4','5','6','7','8','9'):
                    counter2 += 1
                    tmp3 += char
                else:
                    #if we reached a nondata character, lets check our tmp val and see if it contains data
                    #if we can int the characters, we add it into our index
                    try:
                        int(tmp3)
                        index.append(tmp3)
                        tmp3 = ''
                    except:
                        tmp3 = ''
                        pass
            if counter2 == 50:
                raise Exception(f"Could not locate appropriate paldata. FILE KEPT READIING BEYONG {counter2} CHARACTERS AFTER PALDATA")
            if len(index) == 16:
                #we only want a hard 16 entries
                self.index = index
                break

    def arrangeColors(self,palette):
        passes = self.passes
        color1 = []
        color1pass = []
        color2 = []
        color2pass =[]
        color3 = []
        color3pass =[]
        color4 = []
        color4pass =[]
        color5 = []
        color5pass=[]
        color6 = []
        color6pass=[]
        colormasks=[0]
        palette = palette.copy()
        # this should take each palette and organize the colors into what zone they are for
        for i in range(len(palette)):
            # get the code for that zone
            #should add colors into their respective color zones
            if self.index[i][0] == '1':
                #only get non blended areas
                if len(self.index[i])>1:
                    if self.index[i][1] in passes:
                        color1pass.append(palette[i].copy())
                    else:
                        color1.append(palette[i].copy())
                else:
                    color1.append(palette[i].copy())
            if self.index[i][0] == '2':
                #only get non blended areas
                if len(self.index[i])>1:
                    if self.index[i][1] in passes:
                        color2pass.append(palette[i].copy())
                    else:
                        color2.append(palette[i].copy())
                else:
                    color2.append(palette[i].copy())
            if self.index[i][0] == '3':
                #only get non blended areas
                if len(self.index[i])>1:
                    if self.index[i][1] in passes:
                        color3pass.append(palette[i].copy())
                    else:
                        color3.append(palette[i].copy())
                else:
                    color3.append(palette[i].copy())
            if self.index[i][0] == '4':
                #only get non blended areas
                if len(self.index[i])>1:
                    if self.index[i][1] in passes:
                        color4pass.append(palette[i].copy())
                    else:
                        color4.append(palette[i].copy())
                else:
                    color4.append(palette[i].copy())
            if self.index[i][0] == '5':
                #only get non blended areas
                if len(self.index[i])>1:
                    if self.index[i][1] in passes:
                        color5pass.append(palette[i].copy())
                    else:
                        color5.append(palette[i].copy())
                else:
                    color5.append(palette[i].copy())
            if self.index[i][0] == '6':
                #only get non blended areas
                if len(self.index[i])>1:
                    if self.index[i][1] in passes:
                        color6pass.append(palette[i].copy())
                    else:
                        color6.append(palette[i].copy())
                if self.index[i] != '69':
                    color6.append(palette[i].copy())
        colors = [color1, color2, color3, color4, color5,color6]
        for color in colors:
            #if there is data in the color we will look through it
            if color:
                tmp = []
                for val in color:
                #average each rgb val to determine the largest
                    avg = int(sum(val) / len(val))
                    tmp.append(avg)
                #find the largest
                peak = max(tmp)
                #get the index where that max is
                ind = tmp.index(peak)
                #append to colormasks the highest base color for that zone(no zone 0)
                colormasks.append(color[ind])
            else:
                colormasks.append(0)
        self.mask = colormasks.copy()
        #print(colormasks)

    def applyMasks(self,src=None, dest=None, mondata=None, colormasks=None,mode=0):
        print(f"src {self.srcPalette}")
        if src is None:
            src = self.srcPalette.copy()
        if dest is None:
            dest = self.srcPalette.copy()
        if mondata is None:
            mondata = self.index.copy()
        if colormasks is None:
            colormasks = self.mask.copy()
        # should loop 16 times
        i = self.srcwindow.palcounter
        blend = False
        #the masking value is going to be the mask at the index of the first character in paldata
        #so if a color uses code 34 (color3 with something else), we get the masking value at index 3 of masks
        mask = colormasks[int(mondata[i][0])]
        #print(f"mask for zone {mondata[i][0]} is {mask}")
        # check and see if the code is a blender code
        if len(mondata[i]) > 1:
            if mondata[i][1] in self.passes:
                blend = True
        if mask and not blend:
        #if a mask exists, lets mess with it
            for j in mask:
                if j == 0:
                    #handles issues of masks being 0, which they should not be going forward
                    mask[mask.index(j)] = 1
            #gets the value as a percentage of the mask, sets it against 255.
            #mode 0 for setting up the normal.pal
            #mode 1 if normal.pal is set and we need to mask to shiny.pal
            newr = int(dest[i][0] / mask[0] * 255)
            newg = int(dest[i][1] / mask[1] * 255)
            newb = int(dest[i][2] / mask[2] * 255)
            if mode == 1:
                avg = int((newr + newg + newb) / 3)
                dest[i][0] = avg
                dest[i][1] = avg
                dest[i][2] = avg
                tk.Label(self.srcwindow.tool_bar, text=f"{dest[i]}").grid(row=i + 1, column=2, padx=3, pady=2)
                #should then recursively run 16 times
                self.srcwindow.palcounter +=1
                #print('palcounter=',self.srcwindow.palcounter)
                if self.srcwindow.palcounter<len(self.srcPalette):
                    self.applyMasks(src,dest,mondata,colormasks,mode)
            else:
                order = self.getcolororder([newr,newg,newb])
                #after this, bug
                print(mondata)
                print(i)
                print(self.order)
                if (self.checkcolorintegrity(order,self.order[int(mondata[i][0])]) and (newr<256 and newg<256 and newb<256)):#or(int(dest[i][0])==newr and int(dest[i][1])==newg and int(dest[i][2]==newb)):
                    #print(f"passed {order} and {self.order[int(mondata[i][0])]}")
                    dest[i][0] = newr
                    dest[i][1] = newg
                    dest[i][2] = newb
                    tk.Label(self.srcwindow.tool_bar, text=f"{dest[i]}").grid(row=i + 1, column=2, padx=3, pady=2)
                    #if the color passes the check, we move on to the next one
                    self.srcwindow.palcounter += 1
                    print('palcounter=',self.srcwindow.palcounter)
                    if self.srcwindow.palcounter < len(self.srcPalette):
                        self.applyMasks(src, dest, mondata, colormasks, mode)

                else:
                    self.newr = newr
                    self.newg = newg
                    self.newb = newb
                    #handles if the colors dont do what they supposed to or if it is greater than 255
                    txt1 = (f"{newr} {newg} {newb} does not match ordering of {int(dest[i][0])},{int(dest[i][1])},{int(dest[i][2])} -> {mask}.")
                    txt2 = (f"{order} order and {self.order[int(mondata[i][0])]}")
                    self.srcwindow.errmsg1['text']=txt1
                    self.srcwindow.errmsg2['text'] = txt2
                    #set the color to red that we are editing in the image so we can see the color
                    q = dest[i].copy()
                    dest[i] = [255,0,0]
                    self.srcwindow.updateimage(dest)
                    dest[i]=q
                    rk = ('')
                    self.srcwindow.entryR.delete(0, tk.END)
                    self.srcwindow.entryG.delete(0, tk.END)
                    self.srcwindow.entryB.delete(0, tk.END)
                    txt3 = f"What to do for R component ({newr})? y to keep, or enter a value"
                    self.srcwindow.entryR.insert(0,newr)
                    txt4 = f"What to do for G component ({newg})? y to keep, or enter a value"
                    self.srcwindow.entryG.insert(0,newg)
                    txt5 = f"What to do for B component ({newb})? y to keep, or enter a value"
                    self.srcwindow.entryB.insert(0,newb)
                    self.srcwindow.errmsgR['text'] = txt3
                    self.srcwindow.errmsgG['text'] = txt4
                    self.srcwindow.errmsgB['text'] = txt5
                    #print(f'{self.srcPalette}  Line 350')
                    return
           # print(mask)
        #if our code is 69, tha tmeans the color is unused and should be set marked as such
        elif mondata[i]=='69':
            dest[i][0]=69
            dest[i][1]=69
            dest[i][2]=69
            self.srcwindow.palcounter += 1
            print('palcounter=', self.srcwindow.palcounter)
            if self.srcwindow.palcounter < len(self.srcPalette):
                self.applyMasks(src, dest, mondata, colormasks, mode)
        elif blend:
            dest[i][0]=255
            dest[i][1]=255
            dest[i][2]=255
            self.srcwindow.palcounter += 1
            print('palcounter=', self.srcwindow.palcounter)
            if self.srcwindow.palcounter < len(self.srcPalette):
                self.applyMasks(src, dest, mondata, colormasks, mode)
        else:
            self.srcwindow.palcounter += 1
            print('palcounter=', self.srcwindow.palcounter)
        print(dest)
        tk.Label(self.srcwindow.tool_bar, text=f"{dest[i]}").grid(row=i + 1, column=2, padx=3, pady=2)
        #print(dest)
        self.srcwindow.updateimage(dest)
        if self.srcwindow.palcounter < len(self.srcPalette):
            self.applyMasks(src, dest, mondata, colormasks, self.srcwindow.mode)
        else:
            #print('SAVED')
            self.srcwindow.submit.configure(text="Display Sprites")
            self.srcwindow.save = tk.Button(self.srcwindow.error_bar, text='Save Pal', command=lambda: self.savePal(overwriteshiny=(self.srcwindow.mode)))
            self.srcwindow.save.grid(row=90, column=1)
            self.srcwindow.icondisplay = tk.Button(self.srcwindow.error_bar, text='Show icons', command=self.srcwindow.rundemo)
            self.srcwindow.icondisplay.grid(row=91, column=1)

    def fixcolor(self,r,g,b):
        #print(f'line 400{self.srcPalette}')
        if r == 'y':
            if (self.newr>255 or self.newr<0):
                tk.messagebox.showerror("Entry Fail","r is out of range in memory, need update.",parent=self.srcwindow.root)
                return
            self.srcPalette[self.srcwindow.palcounter][0] = self.newr
        else:
            self.srcPalette[self.srcwindow.palcounter][0] = int(r)
        if g == 'y':
            if (self.newg>255 or self.newg<0):
                tk.messagebox.showerror("Entry Fail","g is out of range in memory, need update.",parent=self.srcwindow.root)
                return
            self.srcPalette[self.srcwindow.palcounter][1] = self.newg
        else:
            self.srcPalette[self.srcwindow.palcounter][1] = int(g)
        if b =='y':
            if (self.newb>255 or self.newb<0):
                tk.messagebox.showerror("Entry Fail","b is out of range in memory, need update.",parent=self.srcwindow.root)
                return
            self.srcPalette[self.srcwindow.palcounter][2] = self.newb
        else:
            self.srcPalette[self.srcwindow.palcounter][2] = int(b)
        #print('Why ',self.srcPalette[self.srcwindow.palcounter])
        tk.Label(self.srcwindow.tool_bar, text=f"{self.srcPalette[self.srcwindow.palcounter]}").grid(row=self.srcwindow.palcounter + 1, column=2, padx=3, pady=2)

        self.srcwindow.updateimage(self.srcPalette)
        self.srcwindow.palcounter += 1
        #print('palcounter384=', self.srcPalette[self.srcwindow.palcounter])
        self.srcwindow.clear()
        if self.srcwindow.palcounter < len(self.srcPalette):
            self.applyMasks(mode=self.srcwindow.mode)
        else:
            #print('SAVED')
            self.srcwindow.submit.configure(text="Display Sprites")
            self.srcwindow.save = tk.Button(self.srcwindow.error_bar, text='Save Pal', command=lambda: self.savePal(overwriteshiny=(self.srcwindow.mode)))
            self.srcwindow.save.grid(row=90, column=1)


    def getcolororder(self,colors=None):
        #if colors is blanked, defaults to the mask,
        #otherwise a color can be passed and returned
        #0 =smalles
        #1 = middles
        #2= largest
        #3 = mintie
        #4 = maxtie
        #ties can ignore the rules
        if colors is None:
            colors = self.mask
            order = []
        else:
            colors = [colors]
            order = []
        for val in colors:
            tmp = [0,0,0]
            if val:
                peak = max(val)
                mins = min(val)
                #if its the peak, set it to 2, if something else is also the peak set it to 4
                if val[0] == peak:
                    if val[1] != peak and val[2]!= peak:
                        tmp[0]=2
                    else:
                        tmp[0]=4
                #if it is the min, set it to 0, if something else is tied, set it 3
                elif val[0] == mins:
                    if val[1] != mins and val[2]!= mins:
                        tmp[0]=0
                    else:
                        tmp[0]=3
                #otherwise it is the middle, so 1
                else:
                    tmp[0]=1
                #do the same for the g comp
                if val[1] == peak:
                    if val[0] != peak and val[2]!= peak:
                        tmp[1]=2
                    else:
                        tmp[1]=4
                #if it is the min, set it to 0, if something else is tied, set it 3
                elif val[1] == mins:
                    if val[0] != mins and val[2]!= mins:
                        tmp[1]=0
                    else:
                        tmp[1]=3
                #otherwise it is the middle, so 1
                else:
                    tmp[1]=1
                #and then also the b componenet
                if val[2] == peak:
                    if val[0] != peak and val[1]!= peak:
                        tmp[2]=2
                    else:
                        tmp[2]=4
                #if it is the min, set it to 0, if something else is tied, set it 3
                elif val[2] == mins:
                    if val[0] != mins and val[1]!= mins:
                        tmp[2]=0
                    else:
                        tmp[2]=3
                #otherwise it is the middle, so 1
                else:
                    tmp[2]=1
            order.append(tmp)
        if colors == self.mask:
            self.order = order
        else:
            #print(order[0])
            return order[0]

    def checkcolorintegrity(self,color1,color2):
        #this will make sure each generated color follows the same ordering as the mask val
        matches = True
        #in theory, if the parent color is tied across the board, it should not matter what our values are at
        if color2 == [4,4,4]:
            return matches
        if color2 == [0,0,0]:
            return matches
        for i in range(len(color1)):
            #if the order matches, go to the next component
            if color1[i] == color2[i]:
                pass
            else:
                #if one of the colors is 4, make sure the other is not 0
                #this would look funky if the color tied for max dropped suddenly to the min
                if color1[i] == 4 or color2[i] == 4:
                    if color1[i] != 0 and color2[i] != 0:
                        pass
                    else:
                        matches = False
                        break;
                #this does the same, but makes sure the min doesn't suddenly becom max
                elif color1[i] == 3 or color2[i] == 3:
                    if color1[i] != 2 and color2[i] != 2:
                        pass
                    else:
                        matches = False
                        break;
                else:
                    matches = False
                    break
        return matches

    def savePal(self,pal=None,overwriteshiny=True):
        #this will default to writing over shiny.pal unless a code 2 is passed
        if pal is None:
            pal = self.srcPalette
        txt = 'JASC-PAL\r\n0100\r\n16\r\n'
        for color in pal:
            txt += "{} {} {}\r\n".format(color[0], color[1], color[2])
        txt2 = self.header + bytes(txt, 'utf-8')
        if overwriteshiny:
            self.backuppalette(self.backuppath2,self.path2)
            shinypalfile = open(self.path2, "wb")
            shinypalfile.write(txt2)
            shinypalfile.close()
            print(f"SHINY PAL SAVE SUCCESS :{txt2}")
        else:
            self.backuppalette(self.backuppath1, self.path1)
            normpalfile = open(self.path1, "wb")
            normpalfile.write(txt2)
            normpalfile.close()
            print(f"NORMAL PAL SAVE SUCCESS :{txt2}")
        self.srcwindow.savepal()

    def backuppalette(self,path1,path2):
        #we will create an array of all backup files so we can rotate the oldest out
        files =[]
        for i in range(10):
            path1mod = path1+str(i)+'.pal'
            if os.path.isfile(path1mod):
                files.append(path1mod)
                pass
            else:
                break
        if len(files) >=10:
            times = []
            #we want to always preserve the original ig
            files.pop(0)
            for path2mod in files:
                ti_m = os.path.getmtime(path2mod)
                times.append(path2mod)
            oldest = min(times)
            ind = times.index(oldest)
            path1mod = files[ind]
        pal = open(path1mod,"wb")
        pal2 = open(path2,'rb')
        pal.write(pal2.read())
        pal.close()
        pal2.close()
        print(f"Backup was successful of f{path1mod}.")

    def restorebackup(self,both=True):
        #this should restore a given backupfile if it exists
        #TO DO: Add a way to only restore one file
        while not found:
            backupfile = input("Which backup should be restored (0-9)?")
            if os.path.isfile(self.backuppath1 + backupfile + '.pal'):
                found = True
            if backupfile.lower() == 'q':
                return False
        #open each back up file as a read mode, and overwrite the original files
        filetorestorenormal = open(self.backuppath1 + backupfile + '.pal','rb')
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
        pass

