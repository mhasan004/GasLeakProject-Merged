#%%     
# PLOTTING WITH GEOID, WESTCHESTER SHP NOT FOUND YET
# Plotting the census tracts for all reports that appeared in a specific month                    
# import contextily as ctx
# import matploylib.pyplot as plt
import geopandas as gp
import os
import platform
import pandas as pd
import numpy as np

# shapeFile = "NYU_NYC_ShapeFile/nyu_2451_34513.shp"
shapeFile = "NYU_NYC_34505_SP/nyu_2451_34505.shp"
csvFile = "GasHistory_2010_ReportFrequency_Monthly.csv"
monthlyDF = pd.read_csv(csvFile)                                                                            # Read the csv file and make a data frame
shapeGDF = gp.read_file(shapeFile)                                                                           # Read the shape file and make a data frame
# shapeGDF.plot(figsize = (10,9))

GDF_GEOID_COL = "tractid"
DF_GEOID_COL  = "GEOID_SCT"
MIN_NUM_OF_BLOCKS_TO_PRINT = 200

# ADDING NEW COLS ND CHANGING DATATYPE OF COLS SO WE CAN COMPARE THEM:
shapeGDF["MonthYear"] = str                                                                               # adding two new cols to shapeGDF
shapeGDF["TotalMonthlyReport" ] = int
shapeGDF["CountyName"] = str 
shapeGDF["CensusBlockID_list"] = str  
shapeGDF["Ticket_list"] = str  
shapeGDF["Classification_list"] = str  
shapeGDF["Zipcode_list"] = str 
shapeGDF[[GDF_GEOID_COL]] = shapeGDF[[GDF_GEOID_COL]].apply(pd.to_numeric).astype(int)                                      # Turning GDF_GEOID_COL - the CensusTract number to numpy.int64 values so can query them
shapeGDF[['tractid']] = shapeGDF[['tractid']].apply(pd.to_numeric).astype(int)  
shapeGDF[['tractnum']] = shapeGDF[['tractnum']].apply(pd.to_numeric).astype(int)  
shapeGDF[['name']] = shapeGDF[['name']].apply(pd.to_numeric).astype(int) 
shapeGDF[['bcode']] = shapeGDF[['bcode']].apply(pd.to_numeric).astype(int) 
print("----------------------------------------------------------------- RAW:")
print(shapeGDF)
print("---------------------")
print(monthlyDF)


#  POPULATE THE NEWLY CREATED COLS:
print("Populating new cols...")
skipMonthIndex = []
count = 0
thisMonthPlotGDF = shapeGDF.copy()
# 0) GO THROUGH EACH ROW OF THE MONTHLY CSV DATA AND PULL OUT ALL ROWS THAT ARE IN THE SAME MONTH -> FROM EACH MINI MONTH SEPERATED DF, SEPERATE FUTHER BY COUNTY NAME -> USE THE GEOID OF EACH COUNTY TO NAME THE GDF FILE
for row in range(0,len(monthlyDF)):
    thisMonthPlotGDF.drop(thisMonthPlotGDF.index, inplace=True)                           # resetting the month df for this new month
    if row in skipMonthIndex:
        continue

    # 1) SAME MONTH SEPERATION:
    thisMonthsDF = monthlyDF.loc[                                                                               # thisMonthsDF = df that contains all rows for that month-year
        (monthlyDF['MonthYear']  == monthlyDF['MonthYear'][row]) 
    ]      
    if len(thisMonthsDF) <= MIN_NUM_OF_BLOCKS_TO_PRINT:                                                                                  # If these r no reports for this month-year so skip
        continue
    skipMonthIndex.extend(thisMonthsDF.index.tolist())
    thisMonthsDF = thisMonthsDF.reset_index(drop=True)
    
    thisMonthGeoList = thisMonthsDF.GEOID_SCT.tolist()                                                          # need to put census tracts into an array, if i use directly from thisMonthsDF i get errors when there is no 
    thisMonthStr = monthlyDF['MonthYear'][row]
    # print("\n----------------------------------------------------------------------------thisMonths data\n")
    # print(thisMonthsDF)
    # print("\n------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- Break down:\n")

    # 2) SAME COUNTY SEPERATION:
    skipCountyIndex = []
    for row2 in range(0,len(thisMonthsDF)):
        if row2 in skipCountyIndex:
            continue
        thisMonthsCountyDF = thisMonthsDF.loc[                                                                               # thisMonthsCountyDF = df that contains all rows for that month-year
            (thisMonthsDF['CountyName_2010']  == thisMonthsDF['CountyName_2010'][row2]) 
        ]      
        if len(thisMonthsCountyDF) == 0:                                                                                  # If these r no reports for this month-year so skip
            print("----------------- NO BLOCK FOR THIS COUNTY: "+thisMonthsDF['CountyName_2010'][row2])
            continue
        skipCountyIndex.extend(thisMonthsCountyDF.index.tolist())
        thisMonthsCountyDF = thisMonthsCountyDF.reset_index(drop=True)
        thisCountyStr = monthlyDF['CountyName_2010'][row]
        # print("======================================================================================================== RAW DATA FOR "+thisMonthsCountyDF.iloc[0]["CountyName_2010"])
        # print(thisMonthsCountyDF)

        # 3) FROM THE SEPERATED COUNTY MINI DF -> FIND THE GEOID OF GDF AND POPULATE THE COLS
        skipCountyGeoIdIndex = []
        for row3 in range(0,len(thisMonthsCountyDF)):
            if row3 in skipCountyGeoIdIndex:
                continue
            thisMonthsCountyGeoGDF = shapeGDF.loc[                                                                               # thisMonthsCountyDF = df that contains all rows for that month-year
                (shapeGDF[GDF_GEOID_COL]  == thisMonthsCountyDF[DF_GEOID_COL][row3]) 
            ]      
            if len(thisMonthsCountyGeoGDF) == 0 and thisCountyStr != "Westchester County":                                                                                  # If these r no reports for this month-year so skip
                print("----------------- NO BLOCK FOR THIS COUNTY: ")#+thisMonthsCountyGeoGDF[GDF_GEOID_COL][row3])
                continue
            skipCountyGeoIdIndex.extend(thisMonthsCountyGeoGDF.index.tolist())
            thisMonthsCountyGeoGDF = thisMonthsCountyGeoGDF.reset_index(drop=True)

            # 4) POPULATING THE COLS I ADDED FROM THE ONTHLY CSV DATA FOR THE SAME GEOIDS
            if len(thisMonthsCountyGeoGDF) != 0:
                thisMonthsCountyGeoGDF.at[0, "MonthYear"] = thisMonthsCountyDF.loc[row3]["MonthYear"]
                thisMonthsCountyGeoGDF.at[0, "TotalMonthlyReport"] = thisMonthsCountyDF.loc[row3]["TotalReports"]
                thisMonthsCountyGeoGDF.at[0, "CountyName"] = thisMonthsCountyDF.loc[row3]["CountyName_2010"]
                thisMonthsCountyGeoGDF.at[0, "CensusBlockID_list"] = thisMonthsCountyDF.loc[row3]["CensusBlockID_list"]
                thisMonthsCountyGeoGDF.at[0, "Ticket_list"] = thisMonthsCountyDF.loc[row3]["Ticket_list"]
                thisMonthsCountyGeoGDF.at[0, "Classification_list"] = thisMonthsCountyDF.loc[row3]["Classification_list"]
                thisMonthsCountyGeoGDF.at[0, "Zipcode_list"] = thisMonthsCountyDF.loc[row3]["Zipcode_list"]

            thisMonthPlotGDF = thisMonthPlotGDF.append(thisMonthsCountyGeoGDF)
        thisMonthPlotGDF = thisMonthPlotGDF.reset_index(drop=True)
    # print("--------------------------plot:")
    # print(thisMonthPlotGDF)
    
    ax = shapeGDF.plot(alpha=0.08, figsize = (14,13))
    map = thisMonthPlotGDF.plot(column='TotalMonthlyReport',cmap = 'Reds', edgecolor='black', linewidth = 0.3, figsize = (14,11),legend = True, ax=ax)#, ax=ax, alpha=1) #10,8
    map.set_title(label = 'Number of Gas Leak Reports per Census Tract for\n{0}\n(Showing {1} Tracts, {2} GeoIDs)'.format(thisMonth, len(censusForThisMonth), len(thisMonthPlotGDF)), fontdict={'fontsize': 20}, loc='center')
    if len(censusForThisMonth) != 0 and len(thisMonthPlotGDF) != 0: #there is a month that has one tract but no geoid! so cant get the legend
        leg = map.get_legend()
        leg.set_title('Number Of Reports')
        leg.set_bbox_to_anchor((1.1,0.5,0.1,0.5))                                               # Adjusted numbers to find the best location and size of the legend

#%%


    















# ## SEE WHAT TRACTS ARE IN CONED SITE BUT NOT IN THE SHAPE FILE:
# conSet = set()
# shpSet = set()
# westchesterCounty = set()
# for i in range(0, len(monthlyDF)):
#     if monthlyDF.iloc[i]["CountyName_2010"] != "Westchester County":
#         conSet.add(monthlyDF.iloc[i][DF_GEOID_COL])
#         westchesterCounty.add(monthlyDF.iloc[i][DF_GEOID_COL])                      # this is a list of the westchester counties
# for i in range(0, len(shapeGDF)):
#     shpSet.add(shapeGDF.iloc[i][GDF_GEOID_COL])
# conSet = list(conSet)
# shpSet = list(shpSet)
# westchesterCounty = list(westchesterCounty)
# conSet.sort()
# noneCount = 0
# s=""
# noneTracts = []
# for i in range(0, len(conSet)):
#     if conSet[i] not in shpSet:
#         s=s+str(conSet[i])+", "
#         noneTracts.append(float(conSet[i]))
#         noneCount = noneCount +1
# # print("Census Tracts not in GDF:\n"+s+"\n")
# print("Number of Census Tracts in ConEdison data: "+str(len(conSet)))
# print("Number of Census Tracts in Shapefile:      "+str(len(shpSet)))
# print("Number of Census Tracts missing from Shapefile: "+str(noneCount))
# print("------------------------------------------------------")

# # Making a new empty gdf for each month
# thisMonthPlotGDF = shapeGDF.copy()
# print("Creating GDF for particular months in monthly report freq data...")
# skipIndex = []
# count = 0
# for row in range(0,len(monthlyDF)):
#     thisMonthPlotGDF.drop(thisMonthPlotGDF.index, inplace=True)                           # resetting the month df for this new month
#     if row in skipIndex:
#         continue

#     # 1) SAME MONTH SEPERATION:
#     thisMonthsDF = monthlyDF.loc[                                                                           # thisMonthsDF = df that contains all rows for that month-year
#         (monthlyDF['MonthYear']  == monthlyDF['MonthYear'][row]) 
#     ]      
#     if len(thisMonthsDF) == 0:                                                                              # If these r no reports for this month-year so skip
#         continue
#     skipIndex.extend(thisMonthsDF.index.tolist())
#     thisMonthsDF = thisMonthsDF.reset_index(drop=True)
#     thisMonthGeoList = thisMonthsDF.GEOID_SCT.tolist()                                                  # need to put census tracts into an array, if i use directly from thisMonthsDF i get errors when there is no 
#     thisMonthStr = monthlyDF['MonthYear'][row]
    
#     # 2) SAME MOTH DF -> SAME COUNTY SEPERATION DF:
#     for tractRow in range(0, len(thisMonthGeoList)):
#         tractShapesGDF = shapeGDF.loc[                                                                         # this df that contains all census block geometries to make each tract
#             np.equal(shapeGDF[GDF_GEOID_COL], thisMonthGeoList[tractRow])
#         ]  
#         if len(tractShapesGDF) == 0:
#             if thisMonthGeoList[tractRow] not in noneTracts:
#                 print("*** No geoid/census block for this CensusTract: " + str(thisMonthGeoList[tractRow]) + " --------- this block is from: "+thisMon)
#             continue
#         thisMonthPlotGDF = thisMonthPlotGDF.append(tractShapesGDF)                                          # append the block geometries gdf to this months gdf so we can plot this tract
#     thisMonthPlotGDF = thisMonthPlotGDF.reset_index(drop=True) 

#     print(thisMonthPlotGDF)



















    # # 2) MERGING SIMILAR CENSUS TRACT SEPERATION: FIND BLOCKS FOR EACH TRACT: We have the list of census tracts for this month. Will find all census block geometries for each tract in array. Will put all block geometries that make up the particular tract in tractShapesGDF and append it to thisMonthPlotGDF to have geometries for all tracts of the month
    # for tractRow in range(0, len(thisMonthGeoList)):
    #     tractShapesGDF = shapeGDF.loc[                                                                         # this df that contains all census block geometries to make each tract
    #         np.equal(shapeGDF[GDF_GEOID_COL], thisMonthGeoList[tractRow])
    #     ]  
    #     if len(tractShapesGDF) == 0:
    #         if thisMonthGeoList[tractRow] not in noneTracts:
    #             print("*** No geoid/census block for this CensusTract: " + str(thisMonthGeoList[tractRow]) + " *********************** NOT EXPECTED!")
    #         continue
    #     thisMonthPlotGDF = thisMonthPlotGDF.append(tractShapesGDF)                                          # append the block geometries gdf to this months gdf so we can plot this tract
    # thisMonthPlotGDF = thisMonthPlotGDF.reset_index(drop=True)  
    # print("----------------------------------2222222222--------------"+thisMonthStr)
    # print(thisMonthPlotGDF)

#     # 3) Now that i have the census Tract geometires for this month, Go through the the GDF and edit the "MonthYear" and "TotalMonthlyReport" 
#     for gdfRow in range(0, len(thisMonthPlotGDF)):
#         # if thisMonthStr == "January-2019":
#         gdfRow_tract = thisMonthPlotGDF.iloc[gdfRow][GDF_GEOID_COL]
#         rowN = np.where(thisMonthsDF[DF_GEOID_COL] == gdfRow_tract)[0]
#         gotRepNum = int(str(list(thisMonthsDF.iloc[rowN]['TotalReports'])).strip('[').strip(']'))#.strip("""'""").strip(' ') #got report number from the thisMonthsDF by getting the row were the Census Tract is from the PlotGDF and using the row# and TotalReports col name to get the report number
#         thisMonthPlotGDF.at[gdfRow, "TotalMonthlyReport"] = gotRepNum
#         thisMonthPlotGDF.at[gdfRow, "MonthYear"] = thisMonthStr
#     print(thisMonthPlotGDF)
# #%%
#     # 4) Now that i have the geo dataframe to plot all the census tracts of the month, can now plot them:
#     ax = shapeGDF.plot(alpha=0.08, figsize = (14,13))
#     map = thisMonthPlotGDF.plot(column='TotalMonthlyReport',cmap = 'Reds', edgecolor='black', linewidth = 0.3, figsize = (14,11),legend = True, ax=ax)#, ax=ax, alpha=1) #10,8
#     map.set_title(label = 'Number of Gas Leak Reports per Census Tract for\n{0}\n(Showing {1} Tracts, {2} GeoIDs)'.format(thisMonthStr, len(thisMonthGeoList), len(thisMonthPlotGDF)), fontdict={'fontsize': 20}, loc='center')
#     if len(thisMonthGeoList) != 0 and len(thisMonthPlotGDF) != 0: #there is a month that has one tract but no geoid! so cant get the legend
#         leg = map.get_legend()
#         leg.set_title('Number Of Reports')
#         leg.set_bbox_to_anchor((1.1,0.5,0.1,0.5))                                               # Adjusted numbers to find the best location and size of the legend

# # %%

# %%
