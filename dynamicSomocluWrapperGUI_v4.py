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
import guiMaker
from guiMaker import *
#-------------------------------------------------------------------------------
temporalType = 'dynamic'
k=True
guimaker = guiMaker()
while k:
    win = guimaker.makeWindow(temporalType)
    guimaker.center(win)
    win.mainloop()
    try:
        dataset_path = guimaker.dataset_path
    except:        
        if temporalType == 'static':
            dataset_path = guimaker.askForDatasetFilePath()
        else:
            dataset_path = guimaker.askForDatasetFolderPath()
        pass
    print('Selected matrix folder is: %s' %dataset_path)
    try:
        target_path = guimaker.target_path    
    except:
        target_path = guimaker.askForTargetPath()
        pass
    print('Selected result folder is: %s' %target_path)
    print('**********************************')
    maptype = ['planar','toroid'][int(guimaker.selectmaptype.curselection()[0])]
    print('Selected map type is: %s' %maptype)
    gridtype = ['rectangular','hexagonal'][int(guimaker.selectgridtype.curselection()[0])]
    print('Selected grid type is: %s' %gridtype)   
    initialization = ['random','pca'][int(guimaker.selectinitial.curselection()[0])]
    print('Selected initialization is: %s' %initialization)
    epochs = guimaker.epochs.get()
    print('Selected %d epochs' %epochs)
    #----
    radius0 = guimaker.radius0.get()
    print('Selected %d radius0' %radius0)
    scale0 = guimaker.scale0.get()
    print('Selected %.2f scale0' %scale0)
    #----
    radiusN = guimaker.radiusN.get()
    print('Selected %d radiusN' %radiusN)
    scaleN = guimaker.scaleN.get()
    print('Selected %.2f scaleN' %scaleN)    
    clustering = ['On','Off'][int(guimaker.selectclustering.curselection()[0])]
    print('Affinity Propagation Clustering is %s' %clustering)
    print('**********************************')

    win.destroy()

    folderExtension = '_'.join([maptype,gridtype,initialization,str(epochs)+'epc_',str(radius0)+'rad0_',str(radiusN)+'radN_',str(scale0)+'scl0_',str(scaleN)+'sclN'])
    if not os.path.exists(target_path+'/dynamic__'+folderExtension):
        os.makedirs(target_path+'/dynamic__'+folderExtension)    

    files = glob.glob(dataset_path+'/*.*')
    files.sort(key=lambda x: os.path.getmtime(x))    

    theDelimeter = guiMaker.findDelimiter(files[0])
    
    df = pd.read_table(files[0], sep=theDelimeter, header=0,index_col=0)
    nodes = df.index.tolist()

    lenUnPer = len(nodes)
    if lenUnPer*5< 5*3:
        n_columns, n_rows = 5,3
        lablshift = 0.05 
    else:
        rat = int(np.ceil(np.sqrt(lenUnPer*5/15)))
        n_columns, n_rows = 5*rat, 3*rat
        lablshift = 0.05*rat 
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

        if clustering == 'On':
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
        else:
            colors = [0]*len(nodes)
        areas = [70]*len(som.bmus)

        xDimension, yDimension = [], []
        for x in som.bmus:
            xDimension.append(x[0])
            yDimension.append(x[1])

        fig, ax = plt.subplots()
        plt.switch_backend('TkAgg')
        colMap = 'Spectral_r'
        plt.imshow(som.umatrix,cmap = colMap, aspect = 'auto')
        plt.scatter(xDimension,yDimension,s=areas,c=colors, cmap='RdYlBu')#
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

        plt.xlim(-0.5,n_columns-1)
        plt.ylim(-0.5,n_rows-1)
        plt.gca().invert_yaxis()
        plt.xlabel('ESOM of file %s. Size of map: %s' %(filename,SOMdimensionsString))
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')
        interactive(True)
        plt.show()            
        plt.savefig(target_path+'/dynamic__'+folderExtension+'/esom_'+str(periodIdx)+'_'+timestamp+'.png',bbox_inches='tight')
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
            with codecs.open(target_path+'/dynamic__'+folderExtension+'/drifts/changes_'+str(periodIdx)+'_'+timestamp+'.txt','w','utf8') as f:
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
