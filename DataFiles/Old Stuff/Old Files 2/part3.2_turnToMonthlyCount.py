import csv
import pandas as pd                                                                                                 # to read csv file and store conent into a data frame. To turn json response string into a dataframe

csvHourlyFile = "GasHistory_ReportFrequency_Hourly.csv"                                                             # In PART C we will turn the ticket history data to hourly data
csvMonthlyFile = "GasHistory_ReportFrequency_Monthly.csv"                                                           # IN PART C weill will use the hourly csv to create the number of reports for the month
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# PART C FUNCTION: Make Hourly reports from the gas leak history csv file
def turnHourly_toMonthlyReport():
    global csvFile
    global csvHourlyFile
    hourlyDF = pd.read_csv(csvHourlyFile)                                                                                     # Read Tracts file
    hourlyDF[['Month','Day', 'Year']] = hourlyDF.Date.str.split("/",expand=True)                                            # Splitng the "Date" column into "Month", "Day", "Year" for easier querying
    hourlyDF[['Month','Day', 'Year']] = hourlyDF[['Month','Day', 'Year']].apply(pd.to_numeric)                              # Turning "Month", "Day", "Year" to numeric values so can query them
    # monthlyTractReportCountDF =  pd.DataFrame(columns=["MonthYear", "CensusTract", "TotalReports"]) 
    rowsForDF = []
    colsForDF = ["MonthYear", "CensusTract", "TotalReports"]



    # Going through the hourly DF and creating new DF that holds the reports for each month. Added them to an array for easy access
    skipIndex = []                                                                  # Array that stores the indexes i will skip. Will query for reports in the same month, the resulting rows will be appeneded to be skipped
    monthlyDFArray = []                                                             # For each month, there will be a dataframe of reports, will store each month's dataframe to this index
    for row in range(0,len(hourlyDF)):
        if row in skipIndex:
            continue
        monthlyDF = hourlyDF.loc[                                                   # Querying for all rows that has took place in the same year and month - aka df of monthly reports
            (hourlyDF['Year']  == hourlyDF['Year'][row]) &
            (hourlyDF['Month'] == hourlyDF['Month'][row])
        ]
        skipIndex.extend(monthlyDF.index.tolist())                                  # Since i have these rows already, can skip them
        monthlyDF = monthlyDF.reset_index(drop=True)                                # resetting the index of the df
        monthlyDFArray.append(monthlyDF)                                            # adding this month's df to the array so i can reference this later

    # Going through each monthly DF and making small temporary DF for each CensusTract for that month and outputing only one row for each censustract for each month that contaisn the totla report of that census tract for that month
    for dfRow in range(0,len(monthlyDFArray)):                                      # Going through each monthly DF that coneains a hourly reports of the month
        # Making a string that has the Month and yer
        monthIndex = monthlyDFArray[dfRow]["Month"][0]                              # Going through the monthlyDFArray and spiting out the month number, will use that month number to spit out the month name
        monthName = months[monthIndex-1]
        year = monthlyDFArray[dfRow]["Year"][0]  
        strMonthYr = monthName+"-"+str(year)

        skipIndexMonthlyTract = []
        reportSum = 0
        # Going through the month DF's rows and making small temporary DF to store each census tract. will count how any for that tract for this month
        for row in range(0, len(monthlyDFArray[dfRow])):                                                             
            if row in skipIndexMonthlyTract:
                continue
            monthlyTractDF = monthlyDFArray[dfRow].loc[                                                   # Querying for all rows that has same census tract - this new DF contains the same census tract rows of the month
                monthlyDFArray[dfRow]['CensusTract']  == monthlyDFArray[dfRow]['CensusTract'][row]
            ]
            skipIndexMonthlyTract.extend(monthlyTractDF.index.tolist())                                   # Since I am doing these tracts, can skip them next time
            reportSum = monthlyTractDF["NumberOfReports"].sum()                                           # Summing up the report count fileds of each report of that census tract for this month
            insertRow = [strMonthYr, monthlyDFArray[dfRow]['CensusTract'][row],reportSum ]                # Adding the rows for that census Report for this month
            rowsForDF.append(insertRow)
    
    monthlyTractReportCountDF =  pd.DataFrame(rowsForDF, columns=colsForDF)
    print("Printing monthly report to "+csvMonthlyFile+"...")
    csvOutClear = open(csvMonthlyFile, "w")                                                                          # clearing the file
    csvOutClear.truncate()  
    with open(csvMonthlyFile,'a') as outCSV:                                                                         # Turning the DF into csv and appending the new data to the file
        outCSV.write(monthlyTractReportCountDF.to_csv(header=True, index=False))

    
    














turnHourly_toMonthlyReport()