# Using the con ed report data to make hourly and monthly freq report count csv files:
from urllib.request import urlopen                                                      # Getting the json data from the url
import requests
import json
import pandas as pd                                                                     # To read and write csv files
import numpy as np
import csv
csvFile         = "GasHistory_2010_ConEdisonTracts.csv"
csvHourlyFile   = "GasHistory_2010_ReportFrequency_Hourly.csv"                                                             # In PART C we will turn the ticket history data to hourly data
csvMonthlyFile  = "GasHistory_2010_ReportFrequency_Monthly.csv"                                                             # In PART C we will turn the ticket history data to hourly data

# PART C1 FUNCTION: Make Hourly reports from the gas leak history csv file
def turnTickeyHistory_toHourlyReport():
    global csvFile
    global csvHourlyFile
    csvOutHasData = False                                                                                           # Does the out file have data already? if so can get it and use it and modify it
    conDF = pd.read_csv(csvFile)                                                                                     # Read Tracts file
    for row in range(0, len(conDF)):
        conDF["NumberOfReports"] = int
        conDF["Year"] = int

    csvHeader = ["Year", "Date", "Hour", "CensusTract_2010","NumberOfReports", 
        "CensusTract_2010_ID", "CensusTract_2010_NAME"]                                                             # My new csv need these headers        
    csvOutClear = open(csvHourlyFile, "w")
    csvOutClear.truncate()                                                                                          # deleting everything in the file (will delete this code once i figure out how to update existing file)
    
    with open(csvHourlyFile, 'r') as csvFile:                                                                       # Open the csv File so we can read it
        csvTable = [row for row in csv.DictReader(csvFile)]
        if len(csvTable) == 0:                                                                                      # a) csv is empty so add my header: ['Date', 'Hour', 'CensusTract_2010', 'NumberOfReports']
            with open(csvHourlyFile, 'w', newline='') as outf:
                writer = csv.writer(outf)
                writer.writerow(csvHeader)
        else:
            csvHeader=list(pd.read_csv(csvHourlyFile).columns)                                                      # b) Since the csv already had data, it means i will append new data to it so just use the header of that csv file.
            csvOutHasData = True                                                                                    # There is data here, after i make a new DF using the tract csv i have, will go through the other csv and increment or keep the report counts

    outDF = pd.DataFrame(columns=csvHeader)                                                                         # making newDF with the cols i want. This will be appended to the other csv
    skipIndex = [] 
    print("Turning the Gas Leak Report csv into hourly reports DF...")
    for row in range(0,len(conDF)):
        if row in skipIndex:
            continue

        # This part is just to get the index value of the groupedDF so that i can know what index of "conDF" to skip since i already have them in "groupedDF"
        groupedDF = pd.DataFrame(columns=csvHeader)
        groupedDF = conDF.loc[   
            (conDF['Date'] == conDF['Date'][row]) & 
            (conDF['Hour'] == conDF['Hour'][row]) & 
            (conDF['CensusTract_2010_ID'] == float(conDF['CensusTract_2010_ID'][row]))    ] 
        skipIndex.extend(groupedDF.index.tolist())    
        groupedDF = groupedDF.reset_index(drop=True)      
        groupedDF = groupedDF.filter(csvHeader)                                                                     # Getting rid of those unwanted cols i got from "conDF"

        # Appending row to "outDF" by using small trick to get "groupDF" to one row to easily add it. Since all the rows will now have the same vals, will change the "NumberOfReports" cell and drop the other rows by droppping na's
        # Since the groupedDF was new and the conDF both didnt have "NumberOfReorts" column, it was exclused, will now add it back!
        groupedDF.iloc[0, groupedDF.columns.get_loc("NumberOfReports")] = len(groupedDF)                           # This DF will have the same rows but NumberOFRep and Year will be na, will only push the first row after modifying it and delte na rows.
        groupedDF.iloc[0, groupedDF.columns.get_loc("Year")] = int(groupedDF.iloc[0]["Date"].split("/")[2])
        groupedDF = groupedDF.drop(groupedDF.index[1:len(groupedDF)])                                               # **taking out the first orw and appending it
        outDF = outDF.append(groupedDF, ignore_index=True, sort = False)
    outDF = outDF.reset_index(drop=True)
    print("Printing hourly report DF to "+csvHourlyFile+"...")
    with open(csvHourlyFile,'a') as outCSV:                                                                         # Turning the DF into csv and appending the new data to the file
        outCSV.write(outDF.to_csv(header=False, index=False))

# PART C2 FUNCTION: Trung the Hourly Frequency report into monthly report
def turnHourly_toMonthlyReport():
    global csvHourlyFile
    global csvMonthlyFile
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    hourlyDF = pd.read_csv(csvHourlyFile)                                                                            # Read Tracts file
    for row in range(0, len(hourlyDF)):                                                                             # adding empty cols to the hourly df so can merge with the empty monthly df and have these cols
        hourlyDF["MonthYear"] = str
        hourlyDF["TotalReports"] = int

    csvHeader = ["MonthYear", "CensusTract_2010", "TotalReports", "CensusTract_2010_ID", "CensusTract_2010_NAME"]
    outDF = pd.DataFrame(columns=csvHeader)                                                                         # making newDF with the cols i want. This will be appended to the other csv
    
    csvOutClear = open(csvMonthlyFile, "w")
    csvOutClear.truncate()    
    with open(csvMonthlyFile, 'w', newline='') as outf:
        writer = csv.writer(outf)
        writer.writerow(csvHeader)

    hourlyDF[['Month','Day', 'Year']] = hourlyDF.Date.str.split("/",expand=True)                                    # Splitng the "Date" column into "Month", "Day", "Year" for easier querying
    hourlyDF[['Month','Day', 'Year']] = hourlyDF[['Month','Day', 'Year']].apply(pd.to_numeric)                      # Turning "Month", "Day", "Year" to numeric values so can query them
    
    # Going through the hourly DF and creating new DF that holds the reports for each month. ADDING THESE DFs TO AN ARRAY TO EASILY ACCESS EACH MONTH'S DF:
    skipIndex = []                                                                                                  # Array that stores the indexes i will skip. Will query for reports in the same month, the resulting rows will be appeneded to be skipped
    monthlyDFArray = []                                                                                             # For each month, there will be a dataframe of reports, will store each month's dataframe to this index
    print("Turning Hourly Freq csv to Monthly DFs...")
    for row in range(0,len(hourlyDF)):
        if row in skipIndex:
            continue
        monthlyDF = hourlyDF.loc[                                                                                   # Querying for all rows that has took place in the same year and month - aka df of monthly reports
            (hourlyDF['Year']  == hourlyDF['Year'][row]) &
            (hourlyDF['Month'] == hourlyDF['Month'][row])
        ]
        skipIndex.extend(monthlyDF.index.tolist())                                                                  # Since i have these rows already, can skip them
        monthlyDF = monthlyDF.reset_index(drop=True)                                                                # resetting the index of the df (didnt do this in the other function)
        monthlyDFArray.append(monthlyDF)                                                                            # adding this month's df to the array so i can reference this later

    # Going through each monthly DF and making small temporary DF for each CensusTract for that month and outputing only one row for each censustract for each month that contaisn the totla report of that census tract for that month
    for dfRow in range(0,len(monthlyDFArray)):                                                                      # Going through each monthly DF that coneains a hourly reports of the month
        # Making a string that has the Month and yer
        monthIndex = monthlyDFArray[dfRow]["Month"][0]                                                              # Going through the monthlyDFArray and spiting out the month number, will use that month number to spit out the month name
        monthName = months[monthIndex-1]
        year = monthlyDFArray[dfRow]["Year"][0]  
        strMonthYr = monthName+"-"+str(year)
        thisMonthCensusDF = pd.DataFrame(columns=csvHeader)                                                                         # making newDF with the cols i want. This will be appended to the other csv


        skipIndexMonthlyTract = []
        reportSum = 0
        
        # monthlyTractDF = Spitting out one row that has the the Census total for the particular month-year:
        # Going through the month DF's rows and making small temporary DF to store each census tract. will count how any for that tract for this month
        for row in range(0, len(monthlyDFArray[dfRow])):                                                             
            if row in skipIndexMonthlyTract:
                continue
            monthlyTractDF = monthlyDFArray[dfRow].loc[                                                             # Querying for all rows that has same census tract - this new DF contains the same census tract rows of the month
                monthlyDFArray[dfRow]['CensusTract_2010_ID']  == monthlyDFArray[dfRow]['CensusTract_2010_ID'][row]
            ]
            skipIndexMonthlyTract.extend(monthlyTractDF.index.tolist())                                             # Since I am doing these tracts, can skip them next time
            reportSum = monthlyTractDF["NumberOfReports"].sum()                                                     # Summing up the report count fileds of each report of that census tract for this month
            monthlyTractDF = monthlyTractDF.filter(csvHeader)                                                                     # Getting rid of those unwanted cols i got from "conDF"
            monthlyTractDF = monthlyTractDF.reset_index(drop=True)
            monthlyTractDF.iloc[0, monthlyTractDF.columns.get_loc("TotalReports")] = reportSum                          # This DF will have the same rows but NumberOFRep and Year will be na, will only push the first row after modifying it and delte na rows.
            monthlyTractDF.iloc[0, monthlyTractDF.columns.get_loc("MonthYear")] = strMonthYr 
            monthlyTractDF = monthlyTractDF.drop(monthlyTractDF.index[1:len(monthlyTractDF)])                                               # **taking out the first orw and appending it
            thisMonthCensusDF = thisMonthCensusDF.append(monthlyTractDF)
        outDF = outDF.append(thisMonthCensusDF)
    outDF = outDF.sort_values(by=['MonthYear', 'CensusTract_2010_ID'])
    outDF = outDF.reset_index(drop=True)
    print("Printing monthly report DFs to "+csvMonthlyFile+"...")
    with open(csvMonthlyFile,'a') as outCSV:                                                                         # Turning the DF into csv and appending the new data to the file
        outCSV.write(outDF.to_csv(header=False, index=False))

turnTickeyHistory_toHourlyReport()
# turnHourly_toMonthlyReport()