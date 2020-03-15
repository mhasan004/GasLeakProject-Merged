import plotly.express as px
import numpy as np
import pandas as pd
from scipy import stats

# 1) ADD THE DEMOGRAPHICS COLS TO THE SESONAL 2017 AND 2018 CSV:
    # sesonalCSVFile = "DataFiles/FDNY/Season2017_18.csv"
    # demoCSVFile = "DataFiles/Crime and Demographics/filtered_CensusTract_Demographic_Data_NYCWestchester_filtered2.csv"
    # outCSVFile = "DataFiles/FDNY/Seasonal2017_2018_Demographics.csv"
    # seasonalDF  = pd.read_csv(sesonalCSVFile)  
    # demoDF  = pd.read_csv(demoCSVFile) 

    # # To do a merge need to have same cols so changing demoDF
    # GEOID_COL = "Geoid"
    # demoDF = demoDF.rename(columns={"Id2": GEOID_COL})

    # mergedDF = pd.merge(seasonalDF, demoDF, on=[GEOID_COL], how='left') 
    # mergedDF.to_csv(outCSVFile, index=False)

# 2) PEARSOM R COLLERATION:
out2CSVFILE = "DataFiles/FDNY/Seasonal2017_2018_Demographic_Correlation.csv"
seasonalDemoCSV = "DataFiles/FDNY/Seasonal2017_2018_Demographics.csv"
seasonalDemoDF = pd.read_csv(seasonalDemoCSV)
seasonalDemoDF.set_index('Geoid', inplace=True)     # setting index for correlation

print(stats.pearsonr(seasonalDemoDF.Spring, seasonalDemoDF['Total; Estimate; Total population']))
corr = seasonalDemoDF.corr(method='pearson')
# corr.to_csv(out2CSVFILE)





