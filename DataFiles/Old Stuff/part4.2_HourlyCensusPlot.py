
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

########################################e(plotTitle)
    # print(plotTitle#################






shapeFile = "NY_SP/tl_2019_36_tract.shp"
csvFile = "GasHistory_ReportFrequency_Hourly.csv"

shapeDF = gp.read_file(shapeFile)                                               # Read the shape file and make a data frame
hourlyDF = pd.read_csv(csvFile)                                                 # Read the csv file and make a data frame
hourlyDF[['Month','Day', 'Year']] = hourlyDF.Date.str.split("/",expand=True)    # Splitng the "Date" column into "Month", "Day", "Year" for easier querying
hourlyDF[['Month','Day', 'Year']] = hourlyDF[['Month','Day', 'Year']].apply(pd.to_numeric) #Turning "Month", "Day", "Year" to numeric values so can query them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

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
    
newShapeDF = shapeDF.copy()
newShapeDF.drop(newShapeDF.index, inplace=True)                                       # copied shapef df and emptied it to get empty df. idk why but making empty df with the cols of shapdf dont work
shapeDF.plot()
# print(monthlyDFArray[len(monthlyDFArray)-1])




for dfRow in range(0,len(monthlyDFArray)):
    monthIndex = monthlyDFArray[dfRow]["Month"][0]                              # Going through the monthlyDFArray and spiting out the month number, will use that month number to spit out the month name
    monthName = months[monthIndex-1]
    year = monthlyDFArray[dfRow]["Year"][0]  
    plotTitle = "For "+monthName+" "+str(year)
    
    tract = []                                                                     # *****will contain all CensusTract ids for this entire months frequency data (there will be duplicates s0 need to delete them)
    for row in range(0, len(monthlyDFArray[dfRow])):
        tract.append(monthlyDFArray[dfRow].iloc[row]["CensusTract"])                         # This array has all the census tracts that exists in this month
    
    for row in range(0, len(tract)):
        newShapeDF = newShapeDF.append(shapeDF[shapeDF.NAME == str(int(tract[row]))])         # Prints all GEOID's (prints all blocks) that has this Census Tract
    # newShapeDF.set_title(plotTitle)
    print(plotTitle)

    newShapeDF.plot(cmap='rainbow')
    print("------------------------------------------------------------------------------------"+plotTitle+"     Block in Tract:"+str(len(newShapeDF))+ "       reports# in month: "+str(len(monthlyDFArray[dfRow])))

    # print(newShapeDF)
    newShapeDF.drop(newShapeDF.index, inplace=True) 
   
# %%

















    # if row ==0:
    #     # print(hourlyDF['CensusTract'] == 92.0)
    #     print(hourlyDF['Date'] == "2019")

    # hourlyDF.loc[  (hourlyDF['Date'][2] == "2019")   &   (hourlyDF['Date'][0] == "01")  ]

    # hourlyDF[hourlyDF['Date'].str.split("/")[0] =="1"]
    # monthlyDF = hourlyDF.loc[  
    #     (hourlyDF['Date'].str.split("/")[row][2] == "2019") 
    #     # &(hourlyDF['Date'].str.split("/")[row][1] == "01")
    # ]
    # if row >=0 and row<=100:
    #     print(
    #         str(row)+"     "+str(hourlyDF['Date'].str.split("/")[row][2] == "2019")
    #     )

    #     print("--------------------------")
    # print(monthlyDF)


    # b = hourlyDF.query('`Date`.str.endswith("2019")')
    # print("---------------------------")
    
    # monthlyDF = hourlyDF.loc[   type((hourlyDF['Date']) == hourlyDF['Date'][row])  ] 
    
    # skipIndex.extend(monthlyDF.index.tolist())
    







    # # This part is just to get the index value of the groupedDF so that i can know what index of "hourlyDF" to skip since i already have them in "groupedDF"
    # groupedDF_withIndex = pd.DataFrame(columns=csvHeader)
    # groupedDF_withIndex = hourlyDF.loc[   (hourlyDF['Date'] == hourlyDF['Date'][row]) & (hourlyDF['Hour'] == hourlyDF['Hour'][row]) & (hourlyDF['CensusTract'] == float(hourlyDF['CensusTract'][row]))    ] 
    # skipIndex.extend(groupedDF_withIndex.index.tolist())              
    
    # # Will now makw the dataframe with all the tickets with the same Date, Hour, Census track and append to outDF
    # groupedDF = pd.DataFrame(columns=csvHeader)                                                     # Making a new dataframe and letting it have the columns i want. When i append "hourlyDF" rows, the cols of "hourlyDF" will be added to it. Will finally get rid of unwanted cols with filter().     
    # groupedDF = groupedDF.append(hourlyDF.loc[                                                          # groupedDF added tickets that have the same Census Tract, Hour, and Date. Will get rid of those unwanted cols from "hourlyDF" next
    #     (hourlyDF['Date'] == hourlyDF['Date'][row]) & 
    #     (hourlyDF['Hour'] == hourlyDF['Hour'][row]) & 
    #     (hourlyDF['CensusTract'] == float(hourlyDF['CensusTract'][row]))    
    #     ], sort=False, ignore_index=True
    # ) 
    # groupedDF = groupedDF.filter(csvHeader)                                                         # Getting rid of those unwanted cols i got from "hourlyDF"

    # # Appending row to "outDF" by using small trick to get "groupDF" to one row to easily add it. Since all the rows will now have the same vals, will change the "NumberOfReports" cell and drop the other rows by droppping na's
    # groupedDF.iloc[0, groupedDF.columns.get_loc("NumberOfReports")] = len(groupedDF)
    # groupedDF = groupedDF.dropna()
    # outDF = outDF.append(groupedDF, ignore_index=True, )
















# newShapeDF = shapeDF.copy()
# newShapeDF.drop(newShapeDF.index, inplace=True)                                       # copied shapeDF hourlyDF and emptied it
# for row in range(0, len(hourlyDF)):
#     onlyConEdTracts = shapeDF[shapeDF.NAME == str(int(hourlyDF.loc[row]["CensusTract"]))] # Prints all GEOID's that has this Census Tract
#     newShapeDF = newShapeDF.append(onlyConEdTracts)

# print(newShapeDF)
# newShapeDF.plot(cmap='rainbow')
# shapeDF.plot()







