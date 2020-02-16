# PART 3: now making new csv that is based on time
# 1) df = get the csv data.
# 2) dateDF = loop throught the "Date" column and and make a new data frame for entries that has same Date
# 3) hourlyDF = for each dateDF, loop through the "Hour" column and make a new data frame for entries that has same Hour 
# 4) tractDF  = for each hourlyDF, loop through the "Census Tract" column and make a new data frame for entries that has same Hour 
import pandas as pd    
import csv

csvInFile  = "p3Tract.csv"#"GasHistory_ConEdisonTracts.csv"
csvOutFile = "p3Test.csv"

def turnTicketHistoryToHourlyReport():
    csvOutHasData = False                                                                               # Does the out file have data already? if so can get it and use it and modify it
    inDF = pd.read_csv(csvInFile)                                                                       # Read Tracts file
    csvHeader = ["Date","Hour","CensusTract","NumberOfReports"]                                         # My new csv need these headers        
    
    csvOutClear = open(csvOutFile, "w")
    csvOutClear.truncate()                                                                              # deleting everything in the file (will delete this code once i figure out how to update existing file)

    with open(csvOutFile, 'r') as csvFile:                                                              # Open the csv File so we can read it
        csvTable = [row for row in csv.DictReader(csvFile)]
        if len(csvTable) == 0:                                                                          # a) csv is empty so add my header: ['Date', 'Hour', 'CensusTract', 'NumberOfReports']
            with open(csvOutFile, 'w', newline='') as outf:
                writer = csv.writer(outf)
                writer.writerow(csvHeader)
                print("Added Header: "+str(csvHeader))
        else:
            csvHeader=list(pd.read_csv(csvOutFile).columns)                                             # b) Since the csv already had data, it means i will append new data to it so just use the header of that csv file.
            csvOutHasData = True                                                                        # There is data here, after i make a new DF using the tract csv i have, will go through the other csv and increment or keep the report counts

    outDF = pd.DataFrame(columns=csvHeader)                                                             # making newDF with the cols i want. This will be appended to the other csv
    skipIndex = [] 

    print("Turning the Gas Leak Report data into hourly reports...")
    for row in range(0,len(inDF)):
        if row in skipIndex:
            continue

        # This part is just to get the index value of the groupedDF so that i can know what index of "inDF" to skip since i already have them in "groupedDF"
        groupedDF_withIndex = pd.DataFrame(columns=csvHeader)
        groupedDF_withIndex = inDF.loc[   (inDF['Date'] == inDF['Date'][row]) & (inDF['Hour'] == inDF['Hour'][row]) & (inDF['CensusTract'] == float(inDF['CensusTract'][row]))    ] 
        skipIndex.extend(groupedDF_withIndex.index.tolist())              
        
        # Will now makw the dataframe with all the tickets with the same Date, Hour, Census track and append to outDF
        groupedDF = pd.DataFrame(columns=csvHeader)                                                     # Making a new dataframe and letting it have the columns i want. When i append "inDF" rows, the cols of "inDF" will be added to it. Will finally get rid of unwanted cols with filter().     
        groupedDF = groupedDF.append(inDF.loc[                                                          # groupedDF added tickets that have the same Census Tract, Hour, and Date. Will get rid of those unwanted cols from "inDF" next
            (inDF['Date'] == inDF['Date'][row]) & 
            (inDF['Hour'] == inDF['Hour'][row]) & 
            (inDF['CensusTract'] == float(inDF['CensusTract'][row]))    
            ], sort=False, ignore_index=True
        ) 
        groupedDF = groupedDF.filter(csvHeader)                                                         # Getting rid of those unwanted cols i got from "inDF"

        # Appending row to "outDF" by using small trick to get "groupDF" to one row to easily add it. Since all the rows will now have the same vals, will change the "NumberOfReports" cell and drop the other rows by droppping na's
        groupedDF.iloc[0, groupedDF.columns.get_loc("NumberOfReports")] = len(groupedDF)
        groupedDF = groupedDF.dropna()
        outDF = outDF.append(groupedDF, ignore_index=True, )


    # # Find there is data see if they need to be updated
    # if csvOutHasData == True:
    #     print("i am deleting the csv make sure to delete that code")
    #     csvOutDF = pd.read_csv(csvOutFile)   
    #     differencesDF = outDF.merge(csvOutDF.drop_duplicates(), on=["Date","Hour","CensusTract"], how='outer', indicator=True) 
    #     print("----------------------------a")
    #     newDataDF = differencesDF.loc[differencesDF['_merge']=="left_only"]
    #     print(newDataDF)
    #     print("----------------------------b")
    #     print(differencesDF.loc[differencesDF['_merge']=="right_only"])



    print("Printing hourly report to "+csvOutFile+"...")
    with open(csvOutFile,'a') as outCSV:                                                               # Turning the DF into csv and appending the new data to the file
        outCSV.write(outDF.to_csv(header=False, index=False))

turnTicketHistoryToHourlyReport()



