#%%     
# PLOTTING WITH GEOID, WESTCHESTER SHP NOT FOUND YET
# Plotting the census tracts for all reports that appeared in a specific month                    
# import contextily as ctx
# import matploylib.pyplot as plt
import geopandas as gp
import os
import platform
import pandas as pd
import numpy as np

nycFile     = "NYU_NYC_34505_SP/nyu_2451_34505.shp"
newyorkGDF  = 
csvFile     = "GasHistory_2010_ReportFrequency_Monthly.csv"
monthlyDF   = pd.read_csv(csvFile)                                                                            # Read the csv file and make a data frame
nycGDF      = gp.read_file(nycFile)                                                                           # Read the shape file and make a data frame


GDF_GEOID_COL = "tractid"
DF_GEOID_COL  = "GEOID_SCT"
MIN_NUM_OF_BLOCKS_TO_PRINT = 200