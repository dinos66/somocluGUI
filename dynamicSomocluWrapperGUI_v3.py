#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:
# Purpose:       This .py file is a GUI wrapper for the Somoclu library
#                It requests a series of matrices containing node associations and produces an ESOM
#
# Required libs: pandas, numpy,matplotlib,somoclu
# Author:        Konstantinos Konstantinidis
# email:         konkonst@iti.gr
# Created:       09/12/2016
# Copyright:     (c) ITI (CERTH) 2016
# Licence:       <apache licence 2.0>
#-------------------------------------------------------------------------------
import pandas as pd
import somoclu, time, ntpath, os,sys, glob
import numpy as np
import sklearn.cluster as clusterAlgs
from scipy.spatial import distance
import matplotlib.pyplot as plt
from matplotlib.pylab import interactive
from tkinter import *
from tkinter import filedialog
from csv import Sniffer
#-------------------------------------------------------------------------------

def askForDatasetPath():
    global dataset_path
    root = Tk()
    root.withdraw()
    dataset_path = filedialog.askdirectory(parent=root,initialdir="/",title='Please select the dataset folder containing the matrices')

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

def makeWindow () :
    global selectmaptype, selectgridtype, selectinitial, epochs, radius0, scale0, radiusN, scaleN
    win = Tk()
    l = Label(win, text="SOMOCLU dynamic ESOM creator",font=("Helvetica", 16))
    l.pack()

    frame1 = Frame(win)       # Row of buttons
    frame1.pack()
    b1 = Button(frame1,text="Select matrix folder", command=askForDatasetPath).pack(side=LEFT,padx=10)
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

    Label(frame6, text="radiusN").grid(row=2, column=1)
    radiusN = IntVar()
    e4 = Entry(frame6, textvariable=radiusN, width = 10)
    e4.grid(row=3, column=1,padx=5)
    radiusN.set(1)
    e4.bind()
    
    Label(frame6, text="scaleN").grid(row=2, column=2)
    scaleN = DoubleVar()
    e5 = Entry(frame6, textvariable=scaleN, width = 10)
    e5.grid(row=3, column=2,padx=5)
    scaleN.set(0.01)
    e5.bind()
    
    frameESOM = Frame(win)       # Row of buttons
    frameESOM.pack()
    bESOM = Button(frameESOM,text="Make ESOM", fg="blue",font=("Helvetica", 16),command=win.quit)
    bESOM.pack(side=LEFT,padx=10)

    # frameEnd = Frame(win)       # Row of buttons
    # frameEnd.pack()
    bExit = Button(frameESOM,text="QUIT", fg="red",font=("Helvetica", 16),command=myexit)
    bExit.pack(side=RIGHT,padx=10)
    return win

k=True
while k:
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
    #----
    radius0 = radius0.get()
    print('Selected %d radius0' %radius0)
    scale0 = scale0.get()
    print('Selected %.2f scale0' %scale0)
    #----
    radiusN = radiusN.get()
    print('Selected %d radiusN' %radiusN)
    scaleN = scaleN.get()
    print('Selected %.2f scaleN' %scaleN)
    print('**********************************')

    win.destroy()

    folderExtension = '_'.join([maptype,gridtype,initialization,str(epochs)+'epc_',str(radius0)+'rad0_',str(radiusN)+'radN_',str(scale0)+'scl0_',str(scaleN)+'sclN'])
    if not os.path.exists(target_path+'/dynamic__'+folderExtension):
        os.makedirs(target_path+'/dynamic__'+folderExtension)    

    files = glob.glob(dataset_path+'/*.txt')
    files.sort(key=lambda x: os.path.getmtime(x))    

    head, tail = ntpath.split(files[0])         
    filename = tail or ntpath.basename(head)
    theDelimeter = findDelimiter(files[0])
    df = pd.read_table(files[0], sep=theDelimeter, header=0,index_col=0)
    nodes = df.index.tolist()

    lenUnPer = len(nodes)
    if lenUnPer*5< 50*30:
        n_columns, n_rows = 50,30
        lablshift = .5 
    else:
        rat = int(np.ceil(np.sqrt(lenUnPer*5/1500)))
        n_columns, n_rows = 50*rat, 30*rat
        lablshift = .5*rat 
    SOMdimensionsString = 'x'.join([str(x) for x in [n_columns,n_rows]])
    print('Number of nodes is: %d' %lenUnPer)
    print('SOM dimension is: %s' %SOMdimensionsString)

    som = somoclu.Somoclu(n_columns, n_rows, maptype=maptype, gridtype=gridtype, initialization=initialization)

    timestamp = str(int(time.time()))

    for file in files:

        head, tail = ntpath.split(file)         
        filename = tail or ntpath.basename(head)
        periodIdx = filename[filename.index('_')+1:-4]

        df = pd.read_table(file, sep=str(theDelimeter), header=0,index_col=0)
        dfmax = df.max()
        dfmax[dfmax == 0] = 1
        df = df / dfmax
        nodes = df.index.tolist()
        som.update_data(df.values)
        if int(periodIdx) != 0:
            radius0 = n_rows//5
            scale0 = 0.03
            epochs = 3

        som.train(epochs=epochs, radius0=radius0, radiusN=radiusN, scale0=scale0, scaleN=scaleN)

        '''----------------------clustering params-----------'''
        clusterAlgLabel = 'AffinityPropagation' # KMeans8 , SpectralClustering,AffinityPropagation, Birch 

        if clusterAlgLabel == 'Birch':
            algorithm = clusterAlgs.Birch()
        elif clusterAlgLabel == 'AffinityPropagation':   
            original_shape = som.codebook.shape
            som.codebook.shape = (som._n_columns*som._n_rows, som.n_dim)
            init = -np.max(distance.pdist(som.codebook, 'euclidean'))      
            som.codebook.shape = original_shape        
            algorithm = clusterAlgs.AffinityPropagation(preference = init,damping = 0.9)
        elif clusterAlgLabel == 'KMeans8':
            algorithm = None

        print('Clustering algorithm employed: %s' %clusterAlgLabel)
        som.cluster(algorithm=algorithm)
        '''----------------------clustering params-----------'''
        colors = []
        for idm,bm in enumerate(som.bmus):
            colors.append(som.clusters[bm[1], bm[0]])
        areas = [70]*len(som.bmus)

        xDimension, yDimension = [], []
        for x in som.bmus:
            xDimension.append(x[0])
            yDimension.append(x[1])

        fig, ax = plt.subplots()
        colMap = 'Spectral_r'
        plt.imshow(som.umatrix,cmap = colMap, aspect = 'auto')
        ax.scatter(xDimension,yDimension,s=areas,c=colors, cmap='RdYlBu')#
        doneLabs = set([''])
        for label, x, y in zip(nodes, xDimension, yDimension):
            lblshiftRatio = 1
            labFinshift = ''
            while labFinshift in doneLabs:
                potentialPositions = [(x, y+lblshiftRatio*lablshift), (x, y-lblshiftRatio*lablshift),(x+lblshiftRatio*lablshift*2, y), (x-lblshiftRatio*lablshift*2, y),(x+lblshiftRatio*lablshift*2, y+lblshiftRatio*lablshift), 
                (x-lblshiftRatio*lablshift*2, y+lblshiftRatio*lablshift), (x+lblshiftRatio*lablshift*2, y-lblshiftRatio*lablshift),(x-lblshiftRatio*lablshift*2, y-lblshiftRatio*lablshift)]
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
        fig.savefig(target_path+'/dynamic__'+folderExtension+'/esom_'+str(periodIdx)+'_'+timestamp+'.png',bbox_inches='tight')
        plt.close()
        interactive(False)

        #-----------------------------------------------------------------------------------------------
        '''Check for merges, splits and bmu movements in the files'''#-------------------------------------------
        #-----------------------------------------------------------------------------------------------
        if int(periodIdx)>0:
            if not os.path.exists(target_path+'/dynamic__'+folderExtension+'/drifts/'):
                os.makedirs(target_path+'/dynamic__'+folderExtension+'/drifts/')
            tmpStrClusters = [','.join([str(y) for y in x]) for x in som.bmus]
            strClustDict[periodIdx] = {}
            for idx, sC in enumerate(tmpStrClusters):
                if sC in strClustDict[periodIdx]:
                    strClustDict[periodIdx][sC].append(nodes[idx])
                else:
                    strClustDict[periodIdx][sC] = [nodes[idx]]
            tmpSameBMUsNodes = list(strClustDict[periodIdx].values())
            invStrClustDict[periodIdx] = {','.join(v):k for k,v in strClustDict[periodIdx].items()}
            bmuNodes[periodIdx] = tmpSameBMUsNodes
            tmpsplits,tmpmerges = 0, 0
            with open(target_path+'/dynamic__'+folderExtension+'/drifts/changes_'+str(periodIdx)+'_'+timestamp+'.txt','w') as f:
                for tsbn in tmpSameBMUsNodes:
                    if tsbn not in bmuNodes[str(int(periodIdx)-1)]:
                        oldbmucoords = []
                        for ts in tsbn:
                            for ots in bmuNodes[str(int(periodIdx)-1)]:
                                if ts in ots:
                                    oldbmucoords.append(invStrClustDict[str(int(periodIdx)-1)][','.join(ots)])
                        if len(set(oldbmucoords)) < 2:
                            f.write('Terms %s at %s were split from %s \n' %(','.join(tsbn),invStrClustDict[periodIdx][','.join(tsbn)],'|'.join(oldbmucoords)))
                            if len(tsbn) <= len(strClustDict[str(int(periodIdx)-1)][oldbmucoords[0]])/2:
                                tmpsplits+=len(tsbn)
                                termDislocation['splits'].extend(tsbn)
                                termDislocation['both'].extend(tsbn)
                        else:
                            f.write('Terms %s at %s were merged from %s \n' %(','.join(tsbn),invStrClustDict[periodIdx][','.join(tsbn)],'|'.join(oldbmucoords)))
                            for tmpclusts in [strClustDict[str(int(periodIdx)-1)][x] for x in set(oldbmucoords)]:
                                tmpclustIntersect = set(tmpclusts).intersection(set(tsbn))
                                if len(tmpclustIntersect) <= len(tsbn)/2:
                                    tmpmerges+=len(tmpclustIntersect)
                                    termDislocation['merges'].extend(tmpclustIntersect)
                                    termDislocation['both'].extend(tmpclustIntersect)
                        # termDislocation['both'].extend(tsbn)
            dislocationDict['merges'].append(100*tmpmerges/len(nodes))
            dislocationDict['splits'].append(100*tmpsplits/len(nodes))
            dislocationDict['both'].append(100*(tmpmerges+tmpsplits)/len(nodes))
        else:
            tmpStrClusters = [','.join([str(y) for y in x]) for x in som.bmus]
            strClustDict = {periodIdx:{}}
            for idx, sC in enumerate(tmpStrClusters):
                if sC in strClustDict[periodIdx]:
                    strClustDict[periodIdx][sC].append(nodes[idx])
                else:
                    strClustDict[periodIdx][sC] = [nodes[idx]]
            bmuNodes = {periodIdx:list(strClustDict[periodIdx].values())}
            invStrClustDict = {periodIdx:{','.join(v):k for k,v in strClustDict[periodIdx].items()}}
            dislocationDict = {'merges':[],'splits':[],'both':[]}
            termDislocation = {'merges':[],'splits':[],'both':[]}
            #-------------------------------------------------------------------------------------------------------------------------------------
