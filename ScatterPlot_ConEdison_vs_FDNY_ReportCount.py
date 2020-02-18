#%%
import plotly.express as px
import numpy as np
import pandas as pd
import textwrap                                                 # need this to make the long title


csvConed = "DataFiles/GasHistory_2010_ReportFrequency_Monthly.csv"
csvFDNY  = "DataFiles/FDNY/Geoid_Count2018.csv"#"DataFiles/FDNY/FDNY2018.csv"
conedMonthlyDF  = pd.read_csv(csvConed)  
fdnyMonthlyDF  = pd.read_csv(csvFDNY)  
csvHeader = ['Geoid', 'MonthYear_ConEd', 'NumberOfReports_ConEd', 
# 'MonthYear_FDNY', 'NumberOfReports_FDNY', 
'CountyName', 'CensusTract', "Month"] 
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
vsDF = pd.DataFrame()
for col in range(0, len(csvHeader)):
    vsDF[csvHeader[col]] = str


MIN_NUM_TRACTS_NEEDED_TO_PRINT = 140
coned_CENSUS_TRACT_COL = "CensusTract_2010"
coned_TOTAL_REPORT     = "TotalReports"
coned_COUNTY_NAME      = "CountyName_2010"
coned_GEOID            = "GEOID_SCT"
fdny_TOTAL_REPORT      = "NumberOfReports"
fdny_GEOID             = "Geoid"


# FIXING FDNY DATA: Spliting Time col to Month and Year and then adding new col that is Month-yyyy string like my con ed data 
fdnyMonthlyDF[['Month', 'Year']] = fdnyMonthlyDF.Time.str.split("/",expand=True)                                    
fdnyMonthlyDF[['Month', 'Year']] = fdnyMonthlyDF[['Month', 'Year']].apply(pd.to_numeric)                     
fdnyMonthlyDF = fdnyMonthlyDF.sort_values(by=['Year', 'Month'], ascending=False).drop(columns=['Time'])
fdnyMonthlyDF = fdnyMonthlyDF.reset_index(drop=True)  
fdnyMonthlyDF["MonthYear"] = str
for row in range(0, len(fdnyMonthlyDF)): 
    monthYearStr = months[int(fdnyMonthlyDF.iloc[row]["Month"])-1]+"-"+str(fdnyMonthlyDF.iloc[row]["Year"])
    fdnyMonthlyDF.at[row, "MonthYear"] = monthYearStr

# CONEDISON: POPULATING COLUMNS FOR CON EDISON AND OTHERS: Need to do this to seperate usable months that got enough data in my conedison monthly csv 
skipMonthIndex = []
conedMonthList = list()
for row in range(0,len(conedMonthlyDF)):
    if row in skipMonthIndex:
        continue
    # SAME MONTH SEPERATION:
    thisMonthsDF = conedMonthlyDF.loc[                                                                               
        (conedMonthlyDF['MonthYear']  == conedMonthlyDF['MonthYear'][row])
    ]  
    if len(thisMonthsDF) <= MIN_NUM_TRACTS_NEEDED_TO_PRINT:                                                                                  
        continue
    skipMonthIndex.extend(thisMonthsDF.index.tolist())
    thisMonthsDF = thisMonthsDF.reset_index(drop=True)
    thisMonthYrStr = conedMonthlyDF['MonthYear'][row]  
    thisMonths_vsDF = pd.DataFrame(columns=csvHeader)  
    for row in range(0,len(thisMonthsDF)): 
        tempDF = pd.DataFrame(columns=csvHeader)  
        tempDF.at[0,"MonthYear_ConEd"]       = thisMonthsDF.iloc[row]["MonthYear"]
        tempDF.at[0,"Geoid"]                 = int(thisMonthsDF.iloc[row][coned_GEOID])
        tempDF.at[0,"NumberOfReports_ConEd"] = thisMonthsDF.iloc[row][coned_TOTAL_REPORT]
        tempDF.at[0,"CountyName"]            = thisMonthsDF.iloc[row][coned_COUNTY_NAME]
        tempDF.at[0,"CensusTract"]           = thisMonthsDF.iloc[row][coned_CENSUS_TRACT_COL]
        tempDF.at[0,"Month"]                 = int(thisMonthsDF.iloc[row]["Month"])
        thisMonths_vsDF = pd.concat([thisMonths_vsDF,tempDF])
    thisMonths_vsDF = thisMonths_vsDF.reset_index(drop=True)     
    
    # # print(thisMonths_vsDF.to_string())
    # fig = px.scatter(thisMonths_vsDF, x="ConEd_NumberOfReports", y="FDNY_NumberOfReports", color="CountyName", hover_data=['MonthYear', 'geoid',"CensusTract" ])
    # fig.update_layout(title='Number of Con Edison Gas Leak Reports Every Hour in ')
    # fig.show() 
    vsDF = pd.concat([vsDF,thisMonths_vsDF])
vsDF = vsDF.reset_index(drop=True)    
vsDF[['Geoid', 'Month', 'CensusTract', 'NumberOfReports_ConEd']] = vsDF[['Geoid', 'Month', 'CensusTract', 'NumberOfReports_ConEd']].apply(pd.to_numeric) 
fdnyMonthlyDF = fdnyMonthlyDF.rename(columns={"NumberOfReports": "NumberOfReports_FDNY", "MonthYear": "MonthYear_FDNY"})

# print("----------------------------------------------------------------------------------------- 1")
# print(vsDF)
# print("----------------------------------------------------------------------------------------- 2")
# print(fdnyMonthlyDF)
# print("----------------------------------------------------------------------------------------- 3")``

vsDF = vsDF.merge(fdnyMonthlyDF, left_on=['Geoid','Month'], right_on=['Geoid','Month'])
# print(vsDF)

import textwrap
split_text = textwrap.wrap('This is a very long title and it would be great to have it on three lines', width=30)

# PLOT:
fig = px.scatter(vsDF, x="NumberOfReports_ConEd", y="NumberOfReports_FDNY", color="CountyName", hover_data=['MonthYear_ConEd', 'MonthYear_FDNY', 'Geoid', "CensusTract" ])
titleStr =  'Number of Inspections Conducted by ConEdison (Dec2019-Feb2020) \nvs \nNumber of Gas Leak Reports made to NYFD (Jan, Feb, Dec 2018)'
print("***TITLE OF SCATTER PLOT:*** \n"+titleStr)
fig.update_layout(title=titleStr)
fig.show() 

#%%


