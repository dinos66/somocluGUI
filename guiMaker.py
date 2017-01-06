#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:
# Purpose:       This .py file is a GUI maker for the Somoclu library
#
# Required libs: tkinter
# Author:        Konstantinos Konstantinidis
# email:         konkonst@iti.gr
# Created:       09/12/2016
# Copyright:     (c) ITI (CERTH) 2016
# Licence:       <apache licence 2.0>
#-------------------------------------------------------------------------------
from tkinter import *
from tkinter import filedialog
from csv import Sniffer
#-------------------------------------------------------------------------------

# global selectmaptype, selectgridtype, selectinitial, epochs, radius0, scale0, radiusN, scaleN
class guiMaker:
    def askForDatasetFilePath(self):
        root = Tk()
        root.withdraw()
        self.dataset_path = filedialog.askopenfilename(parent=root,initialdir="/",title='Please select the dataset file containing the matrix')
        return self.dataset_path

    def askForDatasetFolderPath(self):
        root = Tk()
        root.withdraw()
        self.dataset_path = filedialog.askdirectory(parent=root,initialdir="/",title='Please select the dataset folder containing the matrices')
        return self.dataset_path

    def askForTargetPath(self):
        root = Tk()
        root.withdraw()
        self.target_path = filedialog.askdirectory(parent=root,initialdir="/",title='Please select the result writing directory')
        return self.target_path
                
    def onselect(self,event):
        # Note here that Tkinter passes an event object to onselect()
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print ('You selected option %d: "%s"' % (index, value))

    def center(self,toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def myexit(self):
        self.win.destroy()
        sys.exit()

    def findDelimiter(filename):
        if filename[-3:] == 'tsv':
            delimeter = '\t'
        elif filename[-3:] == 'csv':
            delimeter = ','
        else:
            sniffer = Sniffer()
            with open(filename) as f:
                next(f)
                delimeter = sniffer.sniff(f.readline().strip()).delimiter
        return delimeter

    def makeWindow (self,temporalType) :
        # global selectmaptype, selectgridtype, selectinitial, epochs, radius0, scale0, radiusN, scaleN
        win = Tk()
        self.win = win
        l = Label(win, text="SOMOCLU dynamic ESOM creator",font=("Helvetica", 16))
        l.pack()

        frame1 = Frame(win)       # Row of buttons
        frame1.pack()
        if temporalType == 'static':
            fileCommand = self.askForDatasetFilePath
            b1Label = "Select matrix file"
        else:
            fileCommand = self.askForDatasetFolderPath
            b1Label = "Select matrix folder"
        b1 = Button(frame1,text=b1Label, command=fileCommand).pack(side=LEFT,padx=10)
        b2 = Button(frame1,text="Select result folder", command=self.askForTargetPath).pack(side=RIGHT,padx=10)

        frame3 = Frame(win)       # select of names
        frame3.pack(pady=5)#side=LEFT,padx=10)
        l3 = Label(frame3, text="Specify map topology")
        l3.pack()
        selectmaptype = Listbox(frame3, height=2,exportselection=0, width = 12)
        selectmaptype.insert(END,"planar")
        selectmaptype.insert(END,"toroid")
        selectmaptype.selection_set(first=1)
        selectmaptype.bind('<<ListboxSelect>>', self.onselect)
        selectmaptype.pack()#fill=BOTH, expand=1)
        self.selectmaptype = selectmaptype

        frame4 = Frame(win)       # select of names
        frame4.pack(pady=5)#side=LEFT,padx=10)
        l4 = Label(frame4, text="Specify node grid form")
        l4.pack()
        selectgridtype = Listbox(frame4, height=2,exportselection=0, width = 12)
        selectgridtype.insert(END,"rectangular")
        selectgridtype.insert(END,"hexagonal")
        selectgridtype.selection_set(first=0)
        selectgridtype.bind('<<ListboxSelect>>', self.onselect)
        selectgridtype.pack()#fill=BOTH, expand=1)
        self.selectgridtype = selectgridtype

        frame5 = Frame(win)       # select of names
        frame5.pack(pady=5)#side=RIGHT,padx=10)
        l5 = Label(frame5, text="Specify initialization method")
        l5.pack()
        selectinitial = Listbox(frame5, height=2,exportselection=0, width = 12)
        selectinitial.insert(END,"random")
        selectinitial.insert(END,"pca")
        selectinitial.selection_set(first=1)
        selectinitial.bind('<<ListboxSelect>>', self.onselect)
        selectinitial.pack()#fill=BOTH)#, expand=1)
        self.selectinitial = selectinitial

        frame6 = Frame(win)
        frame6.pack(pady=5)
        
        Label(frame6, text="epochs").grid(row=0, column=0)
        epochs = IntVar()
        e1 = Entry(frame6, textvariable=epochs, width = 10)
        epochs.set(10)
        e1.grid(row=1, column=0,padx=5)
        e1.bind()
        self.epochs = epochs

        Label(frame6, text="radius0").grid(row=0, column=1)
        radius0 = IntVar()
        e2 = Entry(frame6, textvariable=radius0, width = 10)
        e2.grid(row=1, column=1,padx=5)
        radius0.set(0)
        e2.bind()
        self.radius0 = radius0
        
        Label(frame6, text="scale0").grid(row=0, column=2)
        scale0 = DoubleVar()
        e3 = Entry(frame6, textvariable=scale0, width = 10)
        e3.grid(row=1, column=2,padx=5)
        scale0.set(0.1)
        e3.bind()
        self.scale0 = scale0

        Label(frame6, text="radiusN").grid(row=2, column=1)
        radiusN = IntVar()
        e4 = Entry(frame6, textvariable=radiusN, width = 10)
        e4.grid(row=3, column=1,padx=5)
        radiusN.set(1)
        e4.bind()
        self.radiusN = radiusN
        
        Label(frame6, text="scaleN").grid(row=2, column=2)
        scaleN = DoubleVar()
        e5 = Entry(frame6, textvariable=scaleN, width = 10)
        e5.grid(row=3, column=2,padx=5)
        scaleN.set(0.01)
        e5.bind()
        self.scaleN = scaleN

        frame7 = Frame(win)       # select of names
        frame7.pack(pady=5)#side=RIGHT,padx=10)
        l7 = Label(frame7, text="Term clustering detection")
        l7.pack()
        selectclustering = Listbox(frame7, height=2,exportselection=0, width = 12)
        selectclustering.insert(END,"On")
        selectclustering.insert(END,"Off")
        selectclustering.selection_set(first=0)
        selectclustering.bind('<<ListboxSelect>>', self.onselect)
        selectclustering.pack()#fill=BOTH)#, expand=1)
        self.selectclustering = selectclustering
        
        frameESOM = Frame(win)       # Row of buttons
        frameESOM.pack()
        bESOM = Button(frameESOM,text="Make ESOM", fg="blue",font=("Helvetica", 16),command=win.quit)
        bESOM.pack(side=LEFT,padx=10)

        # frameEnd = Frame(win)       # Row of buttons
        # frameEnd.pack()
        bExit = Button(frameESOM,text="QUIT", fg="red",font=("Helvetica", 16),command=self.myexit)
        bExit.pack(side=RIGHT,padx=10)
        return win