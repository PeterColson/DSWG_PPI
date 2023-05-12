# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 09:39:35 2023

@author: lpate

This script makes a function that makes .csv files containing the indicator codes and country names 
for which data are to be pulled.
It builds .sel files that pull data for these indicator codes and country names for each of the databases
saved in the relevant folders (see below). The function is called in the "databaseUpdater" script.

HOW TO USE: you need to have all the GIM database files you want to pull from saved in 'Databases/GIM' and all the 
GEM database files you want to pull from saved in 'Databases/GEM'. Note that you need the *extension*
version of the GEM since this has the full country coverage that we want.

Updated by Peter Colson 21/04/2023 - adapting for the GIM to allow more flexibility in choosing variables, indicators 
and measures.
"""

#------Importing packages------#
import pandas as pd
import itertools as it
import os
from os import listdir
from os.path import isfile, join

#------Get list of country labels------#
def sel(sel_dict, var, agg):
    thisdir = os.getcwd() # used in loops below that get lists of files
    GIMPulls = [] # convert selection dictionary into a list of tuples (vbl, location)
    for i in sel_dict.values(): 
        if isinstance(i, list): # if multiple vbls per country, loop over list
            for j in i:
                for k in sel_dict.keys():
                    GIMPulls.append((j,k))
        else:
            for k in sel_dict.keys():
                GIMPulls.append((i,k))
    # create sel file
    GIMPulls = pd.DataFrame(GIMPulls, columns=['Indicator', 'Country']) #make a dataframe with columns for indicator and country .sel code
    GIMPulls.to_csv('Inputs/GIMPulls.csv', header=False, index=False)
    if var: # determine whether to pull the variables or residuals as determined in the functions arguments
        buildGIMSel = GIMPulls.assign(varOrResid='V')
    else:
        buildGIMSel = GIMPulls.assign(varOrResid='R')  
    buildGIMSel = buildGIMSel.assign(agg_code=agg, db="") # determine if we pull in levels, annual levels etc
    #Get list of GIM databases and associated scenarios to pull from
    dbGIM = [thisdir + '\Databases\GIM\\' + f for f in listdir('Databases/GIM') if isfile(join('Databases/GIM', f)) and '.db' in f] #list of paths for database files in the GIM folder
    scenGIM = [f for f in listdir('Databases/GIM') if isfile(join('Databases/GIM', f)) and '.db' in f] #list of names of database files in the GIM folder
    scenGIM = [sub.replace('.db', '') for sub in scenGIM] #get rid of .db to get name of scenario; used in loop below to name sel files
    for i in range(len(dbGIM)):
        GIMSel_i = buildGIMSel.assign(db=dbGIM[i]) #make separate sel text for each db, with a populated db variable
        GIMSel_i.to_csv('Databases/GIM/'+scenGIM[i]+'.sel', header=False, index=False) #create a sel file for each db
    
    print('sel file created in ' + str(thisdir) + '\\Databases\\GIM\\')