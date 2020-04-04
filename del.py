# jupyternotebook too slow so using straight from py
# # After dashboard3.py
# Using OpenData API: https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Historic/qgea-i56i
# GOAL - DASHBOARD 3: Adding new census tract data to 2017-2018 season csv and outputing to file. dashboard3.py will import file and run it in dash
import pandas as pd
import censusdata
import numpy as np
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)
import statsmodels.formula.api as sm   #others ^^
from scipy import stats
import plotly.express as px         # plotting
from sodapy import Socrata             # NYC Open Data
from urllib.request import urlopen     # Turnign long an dlat to census geoids                                                  # Getting the json data from the url
import requests

# def getCensusTract(longitude, latitude,retryRun=0):                                                                 # returns an array [censusTract, CensusBlock, CountyName]
#     #url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={0}&y={1}&benchmark=Public_AR_Current&vintage=Current_Current&format=json".format(longitude,latitude)
#     url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={0}&y={1}&benchmark=Public_AR_Census2010&vintage=Census2010_Census2010&format=json".format(longitude,latitude)
#     if retryRun == 11:                                                                                              # Failed to get json data 11 times with this longitude and latitude so need to skip this one
#         print("*****Failed 11 times to get geodata so will insert 'error'*****")
#         return [str("error"), str("error"), str("error")]
#     try:
#         response = requests.get(url)
#         dataJSON = response.json()
#         data    = dataJSON["result"]

#         tractNAME     = data["geographies"]["Census Tracts"][0]["NAME"]
#         tractBASENAME = data["geographies"]["Census Tracts"][0]["BASENAME"]
#         tractID       = data["geographies"]["Census Tracts"][0]["TRACT"]
#         countyNAME    = data["geographies"]["Counties"][0]["NAME"] 
#         blockGEOID =  data["geographies"]["Census Blocks"][0]["GEOID"]
#         blockNAME     = data["geographies"]["Census Blocks"][0]["NAME"] 
#         blockBASENAME = data["geographies"]["Census Blocks"][0]["BASENAME"]
#         blockID       = data["geographies"]["Census Blocks"][0]["BLOCK"]
#         # Returns: tractBASENAME, blockBASENAME, countyName, geoid, tractid and name, block id and name
#         return [
#             str(tractBASENAME), str(blockBASENAME), str(countyNAME), str(blockGEOID), 
#             str(tractID), str(tractNAME), str(blockID), str(blockNAME)
#         ]
#     except:
#         retryRun+=1
#         print("_____Error on longitude, latitude: "+str(longitude)+","+str(latitude) + ".....retrying... "+str(retryRun))
#         return getCensusTract(longitude, latitude,retryRun)                                                         # need to return the recursive function
#     return


crimeOutFile = "DataFiles/Crime and Demographics/Crime/ACS_10_5YR_S0101_With_Census_Data.csv"
# USERNAME = "mhasan0047@gmail.com"
# PASSWORD = "s0mePass212"
# APP_TOKEN = "I2iI5wKFvjnajBahyxLb5IjBz"
# MyAppToken = "I2iI5wKFvjnajBahyxLb5IjBz"

# # 1) Gettign Crime data from OpenData
# print("...Downloading Crime data...")
# client = Socrata("data.cityofnewyork.us",
#     APP_TOKEN,
#     username = USERNAME,
#     password = PASSWORD, 
#     timeout = 500
# )
# results = client.get(
#     "qgea-i56i", 
#     # query = "SELECT * WHERE boro_nm = 'MANHATTAN' OR boro_nm = 'QUEENS' OR boro_nm = 'BROOKLYN' OR boro_nm = 'BRONX' OR boro_nm = 'QUEENS'"
#     limit = 200000
# )
# crimeDF = pd.DataFrame.from_records(results)


# # 2) Appending New Cols - Cols for census data:
# crimeDF["Geoid"] = int
# crimeDF["Date"]  = str         #rpt_dt
# crimeDF["Month"] = int
# crimeDF["Year"]  = int
# crimeDF["CrimeComplaint"] = str
# expandCols = [ "CensusTract_2010", "CensusBlock_2010", "CountyName", "Geoid_FULL", 
#     "CensusTract_2010_ID", "CensusTract_2010_NAME", "CensusBlock_2010_ID", "CensusBlock_2010_NAME"]  
# currCols = list(crimeDF.columns)
# for newCol in expandCols:
#     if newCol not in currCols:
#         crimeDF[newCol] = np.str

# # 3) Using Long and Lat to populate the Census Data Cols
# crimeDFALL     = crimeDF.copy()
# crimeDF        = crimeDF[0:10000]
# print("...Getting Census Information of Crime Reports from Longitude and Latitude Coordinates...\n...Should take some a long time...")
# rowsToDel = []
# for row in range(0,len(crimeDF)):
#     retryRun = 0
#     lat = float(crimeDF.iloc[row]["latitude"])
#     lon = float(crimeDF.iloc[row]["longitude"])
#     if np.isnan(lon) or np.isnan(lat):
#         print("***This report has no Longitude and Latitude Data so will skip it and delete it from the df***")
#         rowsToDel.append(row)
#         continue
#     returnArray = getCensusTract(lon, lat)            # returnArray = [tractBASENAME, blockBASENAME, countyName, geoid, tract id, tract name, block id, block name]
#     # Make sure the "expandCols" index and "returnArray" index are the same so it prints to right cols
#     if len(expandCols) == len(returnArray):
#         for colToWrite in range(0, len(expandCols)):
#             crimeDF.at[row, expandCols[colToWrite]] = returnArray[colToWrite] 
#     else:
#         print("*** Number of col to add and values to polulate cols are not the same!! ******") 
#     if row%10 == 0:
#         print(row)
#         crimeDF.to_csv(crimeOutFile, index=False)   # Saving just in case 





# DEL:
crimeDF = pd.read_csv("DataFiles/Crime and Demographics/Crime/ACS_10_5YR_S0101_With_Census_Data.csv")
# rowsToDel = []
# for row in range(0,len(crimeDF)):
#     lat = float(crimeDF.iloc[row]["latitude"])
#     lon = float(crimeDF.iloc[row]["longitude"])
#     if np.isnan(lon) or np.isnan(lat):
#         rowsToDel.append(row)
#         continue
# print("done 1")







# # 4) Delete rows of crime reports that had to long and lat data:
# for rowToDel in rowsToDel:
#     crimeDF = crimeDF.drop([rowToDel])  
# crimeDF = crimeDF.reset_index(drop=True)   
# crimeDF.to_csv(crimeOutFile, index=False)
# print("done 2")

#################################### # 5) Populate the Geoid (exclude block id from, Date, Month, Year, and CrimeComplaint Cols
# print("doing")
# for row in range(0,len(crimeDF)):
#     crimeDF.at[row, "Geoid"] = str(str(crimeDF.iloc[row]["Geoid_FULL"])[0:11])
#     crimeDF.at[row, "CrimeComplaint"] = "["+str(crimeDF.iloc[row]["ofns_desc"])+"] " + str(crimeDF.iloc[row]["pd_desc"] )
#     date = crimeDF.iloc[row]["rpt_dt"].split("T")[0].split("-")
#     dateMDY = date[2]+"-"+date[1]+"-"+date[0]
#     crimeDF.at[row, "Date"] = dateMDY
#     crimeDF.at[row, "Year"] = int(date[0])
#     crimeDF.at[row, "Month"] = int(date[1])
# crimeDF = crimeDF.sort_values(by=['Year', 'Month', 'ofns_desc', 'CrimeComplaint', 'CountyName','Geoid'], ascending=False)
# crimeDF = crimeDF.reset_index(drop=True)   
# crimeDF.to_csv(crimeOutFile, index=False)
# print("done 3")
# crimeDF
########################3
rowsToDel = []
print(len(crimeDF))
crimeDF2 = crimeDF.copy() 
print("doing")
delCount = 0

skipIndex = []  
for row in range(0,len(crimeDF)):
    if row in skipIndex:
            continue
    monthlyDF = crimeDF.loc[                                                                                   # Querying for all rows that has took place in the same year and month - aka df of monthly reports
        crimeDF["CensusBlock_2010_NAME"] != "<class 'str'>"        ]
    skipIndex.extend(monthlyDF.index.tolist())
    crimeDF = crimeDF
    break






# for row in range(0,len(crimeDF)):
#     if row%100 == 0:
#         print("      "+str(row))
#     d = crimeDF.loc[crimeDF["CensusBlock_2010_NAME"] != "<class 'str'>"]
#     print(d)
#     if crimeDF.iloc[row]["CensusBlock_2010_NAME"] == "<class 'str'>":
#         #rowsToDel.append(row)
#         crimeDF2 = crimeDF2.drop([row])  
#         delCount  =delCount+1
#         if delCount == 100:
#             print("                   printed")
#             crimeDF2.to_csv(crimeOutFile, index=False)
#         continue

    

# print("done 1")
# # for rowToDel in rowsToDel:
# #     crimeDF = crimeDF.drop([rowToDel])  
# crimeDF2 = crimeDF2.reset_index(drop=True)   
# crimeDF2.to_csv(crimeOutFile, index=False)
# print("done 2")
