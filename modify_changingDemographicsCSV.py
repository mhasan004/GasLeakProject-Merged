import plotly.express as px
import numpy as np
import pandas as pd
import textwrap  

demoCsvFile = "DataFiles/Crime and Demographics/ACS_10_5YR_S0101_with_ann.csv"
newCSV      = "DataFiles/Crime and Demographics/filtered_CensusTract_Demographic_Data_NYCWestchester.csv"

demoDF  = pd.read_csv(demoCsvFile)  
targetCounties = ["Bronx County", "Westchester County", 'New York County', 'Queens County', 'Kings County', 'Richmond County' ]

print(demoDF)
dfCols = list(demoDF.columns)

# DROPPING ALL COLUMNS THAT LISTS THE MARGIN OF ERROR
deleteCols = []
for col in range(0, len(list(demoDF.columns))):
    secondColName = demoDF.iloc[0][dfCols[col]]
    secondStr = secondColName.split("; ")
    if len(secondStr) >1:
        if secondStr[1] == "Margin of Error":
            deleteCols.append(dfCols[col])
demoDF = demoDF.drop(columns=deleteCols)
print(demoDF)
dfCols = list(demoDF.columns)

# DROPPING ALL COLUMNS THAT LISTS len(demoDF)-2 number of (X)'s...aka UNKNOWNS
deleteCols = []
for col in range(0, len(list(demoDF.columns))):
    count = 0    
    print("--- Filtering Col: "+str(col)+" / "+str(len(dfCols)-1))    
    for row in range(0, len(demoDF)):
        if demoDF.iloc[row][dfCols[col]] == "(X)":
            count = count +1
        if count == len(demoDF)-2:              # since proces tkes so long, it made it -2 the len of the df. if there are that many x's, col is useless so delete it
            deleteCols.append(dfCols[col])
        if row == 2 and count == 0:
            continue
demoDF = demoDF.drop(columns=deleteCols)
print(demoDF)
dfCols = list(demoDF.columns)


# DROPPING ALL ROWS THAT ARNT IN NYC
deleteRows = []
for row in range(0, len(demoDF)):
    colStr = demoDF.iloc[row]["GEO.display-label"]
    secondStr = colStr.split(", ")
    if len(secondStr)>1:
        countyStr = secondStr[1]
        if countyStr not in targetCounties:
            deleteRows.append(demoDF.index[demoDF['GEO.display-label'] == colStr].tolist()[0])
demoDF = demoDF.drop(index=deleteRows)
demoDF = demoDF.reset_index(drop=True)


# ----NVM JUST USE EXCELL TO DELETE THE ROWS THAT HAS ALL "-,-,-,-,-,-,-,-" # DROPPING ALL ROWS THAT HAS over 10 "-" ONLY
# deleteRows = set()
# # randomCol = "HC01_EST_VC39"
# for row in range(0, len(demoDF)):
#     count = 0
#     for col in range(0, len(list(demoDF.columns))):
#     # if demoDF.iloc[row][randomCol] == "-":

#         rowsToDel = demoDF.index[demoDF[dfCols[col]] == "-"].tolist()
#         for i in range(0, len(rowsToDel)):
#             deleteRows.add(rowsToDel[i])

# deleteRows = list(deleteRows)
# deleteRows.sort(reverse = False)   
# demoDF = demoDF.drop(index=deleteRows)
# demoDF = demoDF.reset_index(drop=True)
# print(deleteRows)

print(demoDF)
demoDF.to_csv(newCSV, index=False )





    

