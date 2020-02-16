
#%%     
# Plotting the census tracts for all reports that appeared in a specific month                    
import geopandas as gp
import os
import platform
import pandas as pd
import numpy as np
import contextily as ctx

shapeFile = "NY_SP/tl_2019_36_tract.shp"
csvFile = "GasHistory_ReportFrequency_Monthly.csv"
monthlyDF = pd.read_csv(csvFile)                                                                            # Read the csv file and make a data frame
shapeGDF = gp.read_file(shapeFile)                                                                           # Read the shape file and make a data frame
shapeGDF["TotalMonthlyReport" ] = np.int
shapeGDF["MonthYear"] = np.str                                                                               # adding two new cols to shapeGDF

# INTRODUCING A NEW PROBLEM: Changing the datatype of some columns to int to to making querying easier
monthlyDF[['Month', 'Year']] = monthlyDF.MonthYear.str.split("-",expand=True)                               # Splitng the "MonthYear" column into "Month", "Year" for easier querying
monthlyDF[['Year', 'CensusTract']] = monthlyDF[['Year', 'CensusTract']].apply(pd.to_numeric).astype(int)    # Turning "Year" and "CensusTract" to numpy.int64 values so can query them (NAME col is in int while CensusTract is in float)
shapeGDF[['NAME']] = shapeGDF[['NAME']].apply(pd.to_numeric).astype(int)                                      # Turning "NAME" - the CensusTract number to numpy.int64 values so can query them

# Making a new empty gdf for each month
thisMonthPlotGDF = shapeGDF.copy()
thisMonthPlotGDF.drop(thisMonthPlotGDF.index, inplace=True)                                                   # copied shapef df and emptied it to get empty df. idk why but making empty df with the cols of shapdDF dont work
shapeGDF.plot()
# FIXING NEW PROBLEM: FOR THE CSV, I CHNAGED COL TYPE FO INT SO I HAVE DUPLICATE TRACTS, NEED TO SUM THEM: The "CensusTract" columsn ("NAME") in the shapefile is of int. The csv is of float. I turns csv to int. There could be two of the same CensusTract on the csv now. Ex: before 112.2 and 112.4 not both are 112
print("Creating a new monthlyDF without interger CensusTract duplicates...")
skipI = []                                                                                          
monthlyDF_withoutDups = pd.DataFrame(columns=list(monthlyDF.columns))                               # ceatign a new DF to hold the non duplicate of monthlyDF
count = 0
for row in range(0,len(monthlyDF)):
    if row in skipI:
        continue
    dupDF = monthlyDF.loc[                                                                           # thisMonthsDF = df that contains all rows for that month-year
        (monthlyDF['CensusTract']  == monthlyDF['CensusTract'][row]) &
        (monthlyDF['MonthYear']  == monthlyDF['MonthYear'][row])
    ]  
    skipI.extend(dupDF.index.tolist()) 
    dupDF = dupDF.reset_index(drop=True)
    wasD = len(dupDF)
    reportSum = 0
    for dupRows in range(0, len(dupDF)):
        reportSum = reportSum + dupDF.iloc[dupRows]["TotalReports"]
    
    dupDF["TotalReports"] = reportSum
    dupDF = dupDF.drop_duplicates()
    monthlyDF_withoutDups = monthlyDF_withoutDups.append(dupDF)
monthlyDF = monthlyDF_withoutDups.reset_index(drop=True)                                            # New monthlyDF without the repeated Interger CensusTract per month, sumed the reports of those duplicates

print("creating GEO Plot GDF for each tract...")
skipIndex = []
count = 0
for row in range(0,len(monthlyDF)):
    thisMonthPlotGDF.drop(thisMonthPlotGDF.index, inplace=True)                           # resetting the month df for this new month
    if row in skipIndex:
        continue

    # 1) Getting all the census tracts of this month
    thisMonthsDF = monthlyDF.loc[                                                                           # thisMonthsDF = df that contains all rows for that month-year
        (monthlyDF['MonthYear']  == monthlyDF['MonthYear'][row]) 
    ]  
    if len(thisMonthsDF) == 0:                                                                              # If these r no reports for this month-year so skip
        continue
    skipIndex.extend(thisMonthsDF.index.tolist()) 
    thisMonthsDF = thisMonthsDF.reset_index(drop=True)

    censusForThisMonth = thisMonthsDF.CensusTract.tolist()                                                  # need to put census tracts into an array, if i use directly from thisMonthsDF i get errors when there is no 
    thisMonth = monthlyDF['MonthYear'][row]
    
    # 2) FIND BLOCKS FOR EACH TRACT: We have the list of census tracts for this month. Will find all census block geometries for each tract in array. Will put all block geometries that make up the particular tract in tractShapesGDF and append it to thisMonthPlotGDF to have geometries for all tracts of the month
    for tractRow in range(0, len(censusForThisMonth)):
        tractShapesGDF = shapeGDF.loc[                                                                         # this df that contains all census block geometries to make each tract
            np.equal(shapeGDF['NAME'], censusForThisMonth[tractRow])
        ]  
        # tractShapesGDF = tractShapesGDF
        if len(tractShapesGDF) == 0:
            print("*** No geoid/census block for this CensusTract: "+str(censusForThisMonth[tractRow])+" ***") 
            continue
        thisMonthPlotGDF = thisMonthPlotGDF.append(tractShapesGDF)                                          # append the block geometries gdf to this months gdf so we can plot this tract
    thisMonthPlotGDF = thisMonthPlotGDF.reset_index(drop=True)  
    
    # 3) Now that i have the census Tract geometires for this month, Go through the the GDF and edit the "MonthYear" and "TotalMonthlyReport" 
    for gdfRow in range(0, len(thisMonthPlotGDF)):
        # if thisMonth == "January-2019":
        gdfRow_tract = thisMonthPlotGDF.iloc[gdfRow]["NAME"]
        rowN = np.where(thisMonthsDF['CensusTract']==gdfRow_tract)[0]
        gotRepNum = int(str(list(thisMonthsDF.iloc[rowN]['TotalReports'])).strip('[').strip(']'))#.strip("""'""").strip(' ') #got report number from the thisMonthsDF by getting the row were the Census Tract is from the PlotGDF and using the row# and TotalReports col name to get the report number
        thisMonthPlotGDF.at[gdfRow, "TotalMonthlyReport"] = gotRepNum
        thisMonthPlotGDF.at[gdfRow, "MonthYear"] = thisMonth
    # 4) Now that i have the geo dataframe to plot all the census tracts of the month, can now plot them:
    # print(thisMonthPlotGDF.loc[                                                                         # What geoids have a TotalMonthlyReport of x?
    #         np.equal(thisMonthPlotGDF['TotalMonthlyReport'], 10)
    # ])

    # m = shapeGDF.to_crs(epsg=3857)
    # ax = m.plot(color='green', alpha=0.02, edgecolor='k')
    # ctx.add_basemap(ax)
    # map = thisMonthPlotGDF.plot(column='TotalMonthlyReport',cmap = 'Reds', edgecolor='lightgray', linewidth = 0.1, figsize = (14,11),legend = True)#, ax=ax, alpha=1) #10,8
    # map.set_title(label = 'Number of Gas leak Reports per Census Tract for\n{0}\n(Showing {1} Tracts, {2} GeoIDs)'.format(thisMonth, len(censusForThisMonth), len(thisMonthPlotGDF)), fontdict={'fontsize': 20}, loc='center')
    # leg = map.get_legend()
    # leg.set_title('Number Of Reports')
    # leg.set_box_to_anchor((1.1,0.5,0.1,0.5))                          # Adjusted numbers to find the best location and size of the legend
# %%
