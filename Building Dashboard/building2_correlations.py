import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# 1) ADD THE DEMOGRAPHICS COLS TO THE SESONAL 2017 AND 2018 CSV:
sesonalCSVFile = "DataFiles/FDNY/Season2017_18.csv"
demoCSVFile = "DataFiles/Crime and Demographics/filtered_CensusTract_Demographic_Data_NYCWestchester_filtered2.csv"
seasons = ["Spring","Summer","Autumn","Winter"]
seasonalDF  = pd.read_csv(sesonalCSVFile)  
demoDF  = pd.read_csv(demoCSVFile) 
# Sum up the count of the seasonal report counts and make  anew col:
allSum = []
for row in range(0, len(seasonalDF)):
    sum = 0
    for season in seasons:
        sum = sum + seasonalDF.iloc[row][season]
    allSum.append(sum)
seasonalDF["ALL_SEASONS"] = allSum

# 2) Merge
outCSVFile = "DataFiles/FDNY/Seasonal2017_2018_Demographics.csv"
GEOID_COL = "Geoid"
demoDF = demoDF.rename(columns={"Id2": GEOID_COL})
mergedDF = pd.merge(seasonalDF, demoDF, on=[GEOID_COL], how='left') 
mergedDF.to_csv(outCSVFile, index=False)

# 3) Get the DATA:
out2CSVFILE = "DataFiles/FDNY/Seasonal2017_2018_Demographic_Correlation.csv"
seasonalDemoCSV = "DataFiles/FDNY/Seasonal2017_2018_Demographics.csv"
seasonalDemoDF = pd.read_csv(seasonalDemoCSV)
seasonalDemoDF.set_index(GEOID_COL, inplace=True)     # setting index for correlation


# 4) PEARSON R CORRELATION:
corr = seasonalDemoDF.corr(method='pearson')
corr.index.name = 'DemographicVariable'                          # name the index column
corr = corr.reset_index()                                        # numbering the rows and setting DemographicVariable as a new coumn

# 5) Getting rid of the repeated season rows (they are repeated in the columns):
for i in seasons:
    corr = corr[corr.DemographicVariable != i] 
corr = corr[corr.DemographicVariable != "ALL_SEASONS"] 
        
# Need to delete the repeated columns (they are repeated in the rows)
delHeader = list(corr.columns)
for i in range(0, len(seasons)):
    delHeader.remove(seasons[i])
delHeader.remove("DemographicVariable")
delHeader.remove("ALL_SEASONS")
for i in range(0, len(delHeader)):
    corr = corr.drop(delHeader[i], axis=1)             
corr = corr.reset_index()
corr = corr.drop(['index'], axis=1)              # i have two indexes, so droping old one
corr.to_csv(out2CSVFILE, index=False)

# 6) PLOT 1:
season_to_do = "ALL_SEASONS"
fig = px.scatter(corr, x="DemographicVariable", y=season_to_do, color=season_to_do, 
    color_continuous_scale=px.colors.sequential.RdBu,
    width=900, height=1000)
fig.update_layout(
    title = '(Pearson r Correlation) '+"All Seasons"+' Reports VS Demographic Data',
    yaxis_title = "All Seasons"+' vs Demographic Variables Correlation',
    xaxis_title = "Demographic Variables",
)
fig.show()