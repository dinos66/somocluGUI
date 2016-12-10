#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:
# Purpose:       This .py file is a GUI wrapper for the Somoclu library
#                It requests a matrix containing node associations and produces an ESOM
#
# Required libs: pandas, numpy,matplotlib,somoclu
# Author:        Konstantinos Konstantinidis
# email:         konkonst@iti.gr
# Created:       09/12/2016
# Copyright:     (c) ITI (CERTH) 2016
# Licence:       <apache licence 2.0>
#-------------------------------------------------------------------------------
import pandas as pd
import somoclu, time, ntpath, os,sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import interactive
from tkinter import *
#-------------------------------------------------------------------------------

def askForDatasetPath():
    global dataset_path
    root = Tk()
    root.withdraw()
    dataset_path = filedialog.askopenfilename(parent=root,initialdir="/",title='Please select the dataset file containing the matrix')

def askForTargetPath():
    global target_path
    root = Tk()
    root.withdraw()
    target_path = filedialog.askdirectory(parent=root,initialdir="/",title='Please select the result writing directory')
    
def onselect(event):
    # Note here that Tkinter passes an event object to onselect()
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print ('You selected item %d: "%s"' % (index, value))

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

def myexit():
    win.destroy()
    sys.exit()

def makeWindow () :
    global selectmaptype, selectgridtype, selectinitial, epochs, radius0, scale0 
    win = Tk()
    l = Label(win, text="SOMOCLU static ESOM creator",font=("Helvetica", 16))
    l.pack()

    frame1 = Frame(win)       # Row of buttons
    frame1.pack()
    b1 = Button(frame1,text="Select matrix file", command=askForDatasetPath).pack(side=LEFT,padx=10)
    b2 = Button(frame1,text="Select result folder", command=askForTargetPath).pack(side=RIGHT,padx=10)

    frame3 = Frame(win)       # select of names
    frame3.pack(pady=5)#side=LEFT,padx=10)
    l3 = Label(frame3, text="Specify map topology")
    l3.pack()
    selectmaptype = Listbox(frame3, height=2,exportselection=0, width = 12)
    selectmaptype.insert(END,"planar")
    selectmaptype.insert(END,"toroid")
    selectmaptype.selection_set(first=1)
    selectmaptype.bind('<<ListboxSelect>>', onselect)
    selectmaptype.pack()#fill=BOTH, expand=1)

    frame4 = Frame(win)       # select of names
    frame4.pack(pady=5)#side=LEFT,padx=10)
    l4 = Label(frame4, text="Specify node grid form")
    l4.pack()
    selectgridtype = Listbox(frame4, height=2,exportselection=0, width = 12)
    selectgridtype.insert(END,"rectangular")
    selectgridtype.insert(END,"hexagonal")
    selectgridtype.selection_set(first=0)
    selectgridtype.bind('<<ListboxSelect>>', onselect)
    selectgridtype.pack()#fill=BOTH, expand=1)

    frame5 = Frame(win)       # select of names
    frame5.pack(pady=5)#side=RIGHT,padx=10)
    l5 = Label(frame5, text="Specify initialization method")
    l5.pack()
    selectinitial = Listbox(frame5, height=2,exportselection=0, width = 12)
    selectinitial.insert(END,"random")
    selectinitial.insert(END,"pca")
    selectinitial.selection_set(first=1)
    selectinitial.bind('<<ListboxSelect>>', onselect)
    selectinitial.pack()#fill=BOTH)#, expand=1)

    frame6 = Frame(win)
    frame6.pack(pady=5)
    
    Label(frame6, text="epochs").grid(row=0, column=0)
    epochs = IntVar()
    e1 = Entry(frame6, textvariable=epochs, width = 10)
    epochs.set(10)
    e1.grid(row=1, column=0,padx=5)
    e1.bind()

    Label(frame6, text="radius0").grid(row=0, column=1)
    radius0 = IntVar()
    e2 = Entry(frame6, textvariable=radius0, width = 10)
    e2.grid(row=1, column=1,padx=5)
    radius0.set(0)
    e2.bind()
    
    Label(frame6, text="scale0").grid(row=0, column=2)
    scale0 = DoubleVar()
    e3 = Entry(frame6, textvariable=scale0, width = 10)
    e3.grid(row=1, column=2,padx=5)
    scale0.set(0.1)
    e3.bind()
    
    frameESOM = Frame(win)       # Row of buttons
    frameESOM.pack()
    bESOM = Button(frameESOM,text="Make ESOM", fg="blue",font=("Helvetica", 16),command=win.quit)
    bESOM.pack(side=LEFT,padx=10)

    # frameEnd = Frame(win)       # Row of buttons
    # frameEnd.pack()
    bExit = Button(frameESOM,text="QUIT", fg="red",font=("Helvetica", 16),command=myexit)
    bExit.pack(side=RIGHT,padx=10)
    return win

k=0
while k<1:
    win = makeWindow()
    center(win)
    win.mainloop()
    try:
        dataset_path     
    except:
        askForDatasetPath()
        pass
    print('Selected matrix file is: %s' %dataset_path)
    try:
        target_path     
    except:
        askForTargetPath()
        pass
    print('Selected result folder is: %s' %target_path)
    print('**********************************')
    maptype = ['planar','toroid'][int(selectmaptype.curselection()[0])]
    print('Selected map type is: %s' %maptype)
    gridtype = ['rectangular','hexagonal'][int(selectgridtype.curselection()[0])]
    print('Selected grid type is: %s' %gridtype)   
    initialization = ['random','pca'][int(selectinitial.curselection()[0])]
    print('Selected initialization is: %s' %initialization)
    epochs = epochs.get()
    print('Selected %d epochs' %epochs)
    radius0 = radius0.get()
    print('Selected %d radius0' %radius0)
    scale0 = scale0.get()
    print('Selected %.2f scale0' %scale0)
    print('**********************************')

    win.destroy()

    head, tail = ntpath.split(dataset_path)         
    filename = tail or ntpath.basename(head)
    if filename[-3:] == 'tsv':
        delimeter = '\t'
    elif filename[-3:] == 'csv':
        delimeter = ','
    else:
        win = Tk()
        l = Label(win, text="Please choose delimeter")
        l.pack()
        delimeter = StringVar()
        delimeter.set("L") # initialize
        Radiobutton(win, text="comma",font=("Helvetica", 12), variable=delimeter, value=',').pack(anchor=W)
        Radiobutton(win, text="tab",font=("Helvetica", 12), variable=delimeter, value='\t').pack(anchor=W) 
        bExit = Button(win,text="Validate\ndelimeter choice", fg="red",command=win.quit)
        bExit.pack(side=RIGHT,padx=10)
        center(win)
        win.mainloop()
        delimeter = delimeter.get()
        win.destroy()

    df = pd.read_table(dataset_path, sep=str(delimeter), header=0,index_col=0)
    nodes = df.index.tolist()
    lenUnPer = len(nodes)
    if lenUnPer*5< 50*30:
        n_columns, n_rows = 50,30
        lablshift = 1 
    else:
        rat = int(np.ceil(np.sqrt(lenUnPer*5/1500)))
        n_columns, n_rows = 50*rat, 30*rat
        lablshift = 2 
    SOMdimensionsString = 'x'.join([str(x) for x in [n_columns,n_rows]])
    print('Number of nodes is: %d' %lenUnPer)
    print('SOM dimension is: %s' %SOMdimensionsString)

    som = somoclu.Somoclu(n_columns, n_rows, maptype=maptype, gridtype=gridtype, initialization=initialization)

    dfmax = df.max()
    dfmax[dfmax == 0] = 1
    df = df / dfmax
    som.update_data(df.values)
    som.train(epochs=epochs, radius0=radius0, scale0=scale0)

    areas = [50]*len(som.bmus)

    xDimension, yDimension = [], []
    for x in som.bmus:
        xDimension.append(x[0])
        yDimension.append(x[1])

    folderExtension = '_'.join([maptype,gridtype,initialization,str(epochs)+'epc',str(radius0)+'rad',str(scale0)+'scl'])
    if not os.path.exists(target_path+'/'+folderExtension):
        os.makedirs(target_path+'/'+folderExtension)

    fig, ax = plt.subplots()
    colMap = 'Spectral_r'
    plt.title('ESOM of file %s. Size of map: %s' %(filename,SOMdimensionsString))
    plt.imshow(som.umatrix,cmap = colMap, aspect = 'auto')
    ax.scatter(xDimension,yDimension,s=areas)#
    doneLabs = set([''])
    for label, x, y in zip(nodes, xDimension, yDimension):
        lblshiftRatio = 1
        labFinshift = ''
        while labFinshift in doneLabs:
            potentialPositions = [(x, y+lblshiftRatio*lablshift), (x, y-lblshiftRatio*lablshift),(x+lblshiftRatio*lablshift, y), (x-lblshiftRatio*lablshift, y),(x+lblshiftRatio*lablshift, y+lblshiftRatio*lablshift), 
            (x-lblshiftRatio*lablshift, y+lblshiftRatio*lablshift), (x+lblshiftRatio*lablshift, y-lblshiftRatio*lablshift),(x-lblshiftRatio*lablshift, y-lblshiftRatio*lablshift)]
            for pP in potentialPositions:
                labFinshift = pP
                if labFinshift not in doneLabs:
                    break
            lblshiftRatio+=1
        doneLabs.add(labFinshift)
        try:
            finalLabel = labelDict[str(label)]
        except:
            finalLabel = label
        plt.annotate(finalLabel, xy = (x, y), xytext = labFinshift, textcoords = 'data', ha = 'center', va = 'center', fontsize = 10,bbox = dict(boxstyle = 'round,pad=0.1', fc = 'white', alpha = 0.4))#,arrowprops = dict(arrowstyle = '-', connectionstyle = 'arc3,rad=0'))

    plt.xlim(0,n_columns-1)
    plt.ylim(0,n_rows-1) 
    plt.gca().invert_yaxis()
    plt.xlabel('ESOM')
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    interactive(True)
    plt.show()   
    time.sleep(5)
    fig.savefig(target_path+'/'+folderExtension+'/'+filename[:-4]+'_'+str(int(time.time()))+'.png',bbox_inches='tight')
    plt.close()
    interactive(False)
