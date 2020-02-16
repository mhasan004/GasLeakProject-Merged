
# Plotting per hour 
#%%                           
import geopandas as gp
import os
import platform
import pandas as pd

##########################################################
# def set_pandas_display_options() -> None:
#     # Ref: https://stackoverflow.com/a/52432757/
#     display = pd.options.display

#     display.max_columns = 1000
#     display.max_rows = 1000
#     display.max_colwidth = 199
#     display.width = None
#     # display.precision = 2  # set as needed

# set_pandas_display_options()

########################################e(monthYearStr)
    # print(monthYearStr#################


shapeFile = "NY_SP/tl_2019_36_tract.shp"
csvFile = "GasHistory_ReportFrequency_Hourly.csv"
shapeDF = gp.read_file(shapeFile)                                               # Read the shape file and make a data frame
hourlyDF = pd.read_csv(csvFile)                                                 # Read the csv file and make a data frame
shapeGDF["TotalMonthlyReport" ] = np.int
shapeGDF["MonthYear"] = np.str                                                                               # adding two new cols to shapeGDF


hourlyDF[['Month','Day', 'Year']] = hourlyDF.Date.str.split("/",expand=True)    # Splitng the "Date" column into "Month", "Day", "Year" for easier querying
hourlyDF[['Month','Day', 'Year', "CensusTract"]] = hourlyDF[['Month','Day', 'Year', 'CensusTract']].apply(pd.to_numeric).astype(int)  #Turning "Month", "Day", "Year" to numeric values so can query them
shapeGDF[['NAME']] = shapeGDF[['NAME']].apply(pd.to_numeric).astype(int)                                      # Turning "NAME" - the CensusTract number to numpy.int64 values so can query them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


# Making a new empty gdf for each month
thisMonthPlotGDF = shapeGDF.copy()
thisMonthPlotGDF.drop(thisMonthPlotGDF.index, inplace=True)                                                   # copied shapef df and emptied it to get empty df. idk why but making empty df with the cols of shapdDF dont work

# FIXING NEW PROBLEM: FOR THE CSV, I CHNAGED COL TYPE FO INT SO I HAVE DUPLICATE TRACTS, NEED TO SUM THEM: The "CensusTract" columsn ("NAME") in the shapefile is of int. The csv is of float. I turns csv to int. There could be two of the same CensusTract on the csv now. Ex: before 112.2 and 112.4 not both are 112
print("Creating a new hourlyDF without interger CensusTract duplicates...")
skipI = []                                                                                          
hourlyDF_withoutDups = pd.DataFrame(columns=list(hourlyDF.columns))                               # ceatign a new DF to hold the non duplicate of hourlyDF
count = 0
for row in range(0,len(hourlyDF)):
    if row in skipI:
        continue
    dupDF = hourlyDF.loc[                                                                           # thisMonthsDF = df that contains all rows for that month-year
        (hourlyDF['CensusTract']  == hourlyDF['CensusTract'][row]) &
        (hourlyDF['Month']  == hourlyDF['Month'][row])&
        (hourlyDF['Year']  == hourlyDF['Year'][row])
    ]  
    skipI.extend(dupDF.index.tolist()) 
    dupDF = dupDF.reset_index(drop=True)
    wasD = len(dupDF)
    reportSum = 0
    for dupRows in range(0, len(dupDF)):
        reportSum = reportSum + dupDF.iloc[dupRows]["NumberOfReports"]
    dupDF["NumberOfReports"] = reportSum
    dupDF = dupDF.drop_duplicates()
    hourlyDF_withoutDups = hourlyDF_withoutDups.append(dupDF)
hourlyDF = hourlyDF_withoutDups.reset_index(drop=True)                                            # New hourlyDF without the repeated Interger CensusTract per month, sumed the reports of those duplicates
print(hourlyDF)
print(shapeGDF)


#%%
# Make an array that holds the DF of all reports of an hour of a day
skipIndex = []                                                                  # Array that stores the indexes i will skip. Will query for reports in the same month, the resulting rows will be appeneded to be skipped
thisDayHourArray = []                                                             # Will hold the DF of each hour for that day
for row in range(0,len(hourlyDF)):
    thisMonthPlotGDF.drop(thisMonthPlotGDF.index, inplace=True)                           # resetting the month df for this new month
    if row in skipIndex:
        continue
    
    # 1) Getting all the census tracts of this month
    thisDayHourDF = hourlyDF.loc[                                                   # Querying for all rows that has took place in the same day and hour
        (hourlyDF['Date']  == hourlyDF['Date'][row]) &
        (hourlyDF['Hour'] == hourlyDF['Hour'][row]) 
    ]
    skipIndex.extend(thisDayHourDF.index.tolist())                                  # Since i have these rows already, can skip them
    thisDayHourDF = thisDayHourDF.reset_index(drop=True)                                # resetting the index of the df
    thisDayHourArray.append(thisDayHourDF)                                            # adding this month's df to the array so i can reference this later

for dfRow in range(0,len(thisDayHourArray)):
    monthIndex = thisDayHourArray[dfRow]["Month"][0]                              # Going through the thisDayHourArray and spiting out the month number, will use that month number to spit out the month name
    monthName = months[monthIndex-1]
    thisyear = thisDayHourArray[dfRow]["Year"][0]  
    thisMonthYearStr = "For "+monthName+" "+str(year)
    thisCensusTract = thisDayHourArray[dfRow]["CensusTract"][0]  
    thisHour = thisDayHourArray[dfRow]["Hour"][0]    
    # 2) FIND BLOCKS FOR EACH TRACT: We have the list of census tracts for this month. Will find all census block geometries for each tract in array. Will put all block geometries that make up the particular tract in tractShapesGDF and append it to thisMonthPlotGDF to have geometries for all tracts of the month
    tractShapesGDF = shapeGDF.loc[                                                                         # this df that contains all census block geometries to make each tract
        np.equal(shapeGDF['NAME'], thisCensusTract)
    ]  
    if len(tractShapesGDF) == 0:
        print("*** No geoid/census block for this CensusTract: "+str(censusForThisMonth[dfRow])+" ***") 
        continue
    thisMonthPlotGDF = thisMonthPlotGDF.append(tractShapesGDF)                                          # append the block geometries gdf to this months gdf so we can plot this tract
    thisMonthPlotGDF = thisMonthPlotGDF.reset_index(drop=True)  
        
    # 3) Now that i have the census Tract geometires for this month, Go through the the GDF and edit the "MonthYear" and "TotalMonthlyReport" 
    for gdfRow in range(0, len(thisMonthPlotGDF)):
        gdfRow_tract = thisMonthPlotGDF.iloc[gdfRow]["NAME"]
        rowN = np.where(thisDayHourArray[dfRow]['CensusTract'] == gdfRow_tract)[0]
        gotRepNum = int(str(list(thisMonthsDF.iloc[rowN][0['NumberOfReports'])).strip('[').strip(']'))#.strip("""'""").strip(' ') #got report number from the thisMonthsDF by getting the row were the Census Tract is from the PlotGDF and using the row# and TotalReports col name to get the report number
        thisMonthPlotGDF.at[gdfRow, "NumberOfReports"] = gotRepNum
        thisMonthPlotGDF.at[gdfRow, "MonthYear"] = thisMonth








#%%


    tract = []                                                                     # *****will contain all CensusTract ids for this entire months frequency data (there will be duplicates s0 need to delete them)
    for row in range(0, len(thisDayHourArray[dfRow])):
        tract.append(thisDayHourArray[dfRow].iloc[row]["CensusTract"])                         # This array has all the census tracts that exists in this month
    
    for row in range(0, len(tract)):
        thisMonthPlotGDF = thisMonthPlotGDF.append(shapeDF[shapeDF.NAME == str(int(tract[row]))])         # Prints all GEOID's (prints all blocks) that has this Census Tract
    # thisMonthPlotGDF.set_title(monthYearStr)
    print(monthYearStr)

    thisMonthPlotGDF.plot(cmap='rainbow')
    print("------------------------------------------------------------------------------------"+monthYearStr+"     Block in Tract:"+str(len(thisMonthPlotGDF))+ "       reports# in month: "+str(len(thisDayHourArray[dfRow])))

    # print(thisMonthPlotGDF)
    thisMonthPlotGDF.drop(thisMonthPlotGDF.index, inplace=True) 
   























#%%

#     # if row ==0:
#     #     # print(hourlyDF['CensusTract'] == 92.0)
#     #     print(hourlyDF['Date'] == "2019")

#     # hourlyDF.loc[  (hourlyDF['Date'][2] == "2019")   &   (hourlyDF['Date'][0] == "01")  ]

#     # hourlyDF[hourlyDF['Date'].str.split("/")[0] =="1"]
#     # hourlyDF = hourlyDF.loc[  
#     #     (hourlyDF['Date'].str.split("/")[row][2] == "2019") 
#     #     # &(hourlyDF['Date'].str.split("/")[row][1] == "01")
#     # ]
#     # if row >=0 and row<=100:
#     #     print(
#     #         str(row)+"     "+str(hourlyDF['Date'].str.split("/")[row][2] == "2019")
#     #     )

#     #     print("--------------------------")
#     # print(hourlyDF)


#     # b = hourlyDF.query('`Date`.str.endswith("2019")')
#     # print("---------------------------")
    
#     # hourlyDF = hourlyDF.loc[   type((hourlyDF['Date']) == hourlyDF['Date'][row])  ] 
    
#     # skipIndex.extend(hourlyDF.index.tolist())
    







#     # # This part is just to get the index value of the groupedDF so that i can know what index of "hourlyDF" to skip since i already have them in "groupedDF"
#     # groupedDF_withIndex = pd.DataFrame(columns=csvHeader)
#     # groupedDF_withIndex = hourlyDF.loc[   (hourlyDF['Date'] == hourlyDF['Date'][row]) & (hourlyDF['Hour'] == hourlyDF['Hour'][row]) & (hourlyDF['CensusTract'] == float(hourlyDF['CensusTract'][row]))    ] 
#     # skipIndex.extend(groupedDF_withIndex.index.tolist())              
    
#     # # Will now makw the dataframe with all the tickets with the same Date, Hour, Census track and append to outDF
#     # groupedDF = pd.DataFrame(columns=csvHeader)                                                     # Making a new dataframe and letting it have the columns i want. When i append "hourlyDF" rows, the cols of "hourlyDF" will be added to it. Will finally get rid of unwanted cols with filter().     
#     # groupedDF = groupedDF.append(hourlyDF.loc[                                                          # groupedDF added tickets that have the same Census Tract, Hour, and Date. Will get rid of those unwanted cols from "hourlyDF" next
#     #     (hourlyDF['Date'] == hourlyDF['Date'][row]) & 
#     #     (hourlyDF['Hour'] == hourlyDF['Hour'][row]) & 
#     #     (hourlyDF['CensusTract'] == float(hourlyDF['CensusTract'][row]))    
#     #     ], sort=False, ignore_index=True
#     # ) 
#     # groupedDF = groupedDF.filter(csvHeader)                                                         # Getting rid of those unwanted cols i got from "hourlyDF"

#     # # Appending row to "outDF" by using small trick to get "groupDF" to one row to easily add it. Since all the rows will now have the same vals, will change the "NumberOfReports" cell and drop the other rows by droppping na's
#     # groupedDF.iloc[0, groupedDF.columns.get_loc("NumberOfReports")] = len(groupedDF)
#     # groupedDF = groupedDF.dropna()
#     # outDF = outDF.append(groupedDF, ignore_index=True, )
















# # thisMonthPlotGDF = shapeDF.copy()
# # thisMonthPlotGDF.drop(thisMonthPlotGDF.index, inplace=True)                                       # copied shapeDF hourlyDF and emptied it
# # for row in range(0, len(hourlyDF)):
# #     onlyConEdTracts = shapeDF[shapeDF.NAME == str(int(hourlyDF.loc[row]["CensusTract"]))] # Prints all GEOID's that has this Census Tract
# #     thisMonthPlotGDF = thisMonthPlotGDF.append(onlyConEdTracts)

# # print(thisMonthPlotGDF)
# # thisMonthPlotGDF.plot(cmap='rainbow')
# # shapeDF.plot()







