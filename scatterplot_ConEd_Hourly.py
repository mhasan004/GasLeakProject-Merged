
#%%
import plotly.express as px
import numpy as np
import pandas as pd

csvFile   = "DataFiles/GasHistory_2010_ReportFrequency_Hourly.csv"
hourlyDF = pd.read_csv(csvFile)  
hourlyDF = hourlyDF.sort_values("Date", ascending=True)
csvHeader = ['MonthYear', 'Hours', 'NumberOfReports'] 

hourArray = ['1 AM', '2 AM', '3 AM', '4 AM', '5 AM', '6 AM', '7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 AM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM', '10 PM', '11 PM', '12 PM']
MIN_NUM_TRACTS_NEEDED_TO_PRINT = 140


skipMonthIndex = []
# 0) GO THROUGH EACH ROW OF THE MONTHLY CSV DATA AND PULL OUT ALL ROWS THAT ARE IN THE SAME MONTH -> FROM EACH MINI MONTH SEPERATED DF, SEPERATE FUTHER BY COUNTY NAME -> USE THE GEOID OF EACH COUNTY TO NAME THE GDF FILE
for row in range(0,len(hourlyDF)):
    if row in skipMonthIndex:
        continue
    # 1) SAME MONTH SEPERATION:
    thisMonthsDF = hourlyDF.loc[                                                                               # thisMonthsDF = df that contains all rows for that month-year
        (hourlyDF['MonthYear']  == hourlyDF['MonthYear'][row])
    ]  
    if len(thisMonthsDF) <= MIN_NUM_TRACTS_NEEDED_TO_PRINT:                                                                                  # If these r no reports for this month-year so skip
        continue
    skipMonthIndex.extend(thisMonthsDF.index.tolist())
    thisMonthsDF = thisMonthsDF.reset_index(drop=True)
    thisMonthYrStr = hourlyDF['MonthYear'][row]

    # 2) Go thru the hours and make a counter
    thisMonthHourFreqDF = pd.DataFrame(columns=csvHeader)  
    for hour in range(0, len(hourArray)):
        # 1) SAME MONTH SEPERATION:
        thisHourMonthDF = thisMonthsDF.loc[                                                                               # thisMonthsDF = df that contains all rows for that month-year
            (thisMonthsDF["Hour"]  == hourArray[hour]) 
        ]  
        thisHourMonthDF = thisHourMonthDF.reset_index(drop=True)
        thisHour = hourArray[hour]
        
        # 3) Sum up the reports for that hour:
        thisHourDF = pd.DataFrame(columns=csvHeader)  
        thisHourDF.at[0,"MonthYear"] = thisMonthYrStr
        thisHourDF.at[0,"Hours"]     = thisHour
        thisHourDF.at[0,"NumberOfReports"] = len(thisHourMonthDF)
        thisMonthHourFreqDF = pd.concat([thisMonthHourFreqDF,thisHourDF])
    thisMonthHourFreqDF = thisMonthHourFreqDF.reset_index(drop=True)             
    # print("--------------------------------------"+thisMonthYrStr)
    # print(thisMonthHourFreqDF)
    fig = px.scatter(thisMonthHourFreqDF, x="Hours", y="NumberOfReports")
    fig.update_layout(title='Number of Con Edison Gas Leak Reports Every Hour in '+thisMonthYrStr)
    fig.show() 


#%%


