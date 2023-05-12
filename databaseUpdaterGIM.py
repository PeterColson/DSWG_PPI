# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 10:49:09 2023

@author: jacob.smith

Updated by Luke Pate 08/02/2023 - generalising to allow for pulling from GIM, GEM and GCS

This function extracts the latest database from the GIM/GEM/GCS using a batch file and the mdl programming language under the hood to create csvs for inputs into the GROM
It uses sel files produced by a function called sel() which is taken from the BuildSelFiles script.

WARNING: The address for one of the models contains a backslash n, which is special escape character. Just make sure it"s interpreted as a raw character with r"character string"
one of the models
ReadMe for MDL: http://tools.oxfordeconomics.com/mdl/readme.html
Example mdl code: mdl export -d MyDatabase.db -s MySelection.sel -m C:\MyModelDirectory -o MyExport.csv
"""
import subprocess
import os
from os import listdir
from os.path import isfile, join
import pandas as pd
from BuildSelFilesGIM import sel

def databaseUpdater(start, end, seldict, var, agg):
    MyModel = 'GIM'
    cwd = os.getcwd()
    #Options
    Years = str(start)+" -e "+str(end) #select what years
    
    #Use the sel() function defined in the BuildSelFiles script to update the batch files for the model in question
    sel(seldict, var, agg)
    
    #Point the file to the relevant model directory on your machine
    DependencyFile = r"C:\OxfordGlobalIndustry"
    
    #Point to the batch file - this needs to already be created, just edited here
    batchFile = cwd + r"\var_grabber.bat"
    
    #Create mdl code
    mdl_code = ""
    db = [f for f in listdir(join('Databases\\',MyModel)) if isfile(join('Databases\\', MyModel, f)) and '.db' in f]
    scen = [d.replace('.db', '') for d in db]
    for s in scen:
        mdl_code += "mdl export -d "+cwd+"\Databases\\"+MyModel+"\\"+s+".db"+" -s "+cwd+"\Databases\\"+MyModel+"\\"+s+".sel -m "+DependencyFile+" -y "+Years+" -o " +cwd+"\Databases\\"+MyModel+"\\"+s+".csv -f Classic_v" + "\n"
 
    #Creating the batch file
    myBat = open(batchFile,"w+")
    myBat.write(mdl_code) #add in the mdl code written above
    myBat.close()
    
    #Running the batch file
    #tries to run the batch file and returns some errors if it cooks itself
    try:
        subprocess.check_output(batchFile)
    except subprocess.CalledProcessError as e:
        print(e.output)

    # output data to a dataframe
    df = pd.read_csv(cwd+"\Databases\\"+MyModel+"\\"+s+".csv", header=None)
    return df