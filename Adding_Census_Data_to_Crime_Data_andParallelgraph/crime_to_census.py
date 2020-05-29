import pandas as pd
import censusdata
import numpy as np
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)
import statsmodels.formula.api as sm

from scipy import stats
import plotly.express as px         # plotting

from sodapy import Socrata             # NYC Open Data

from urllib.request import urlopen     # Turnign long an dlat to census geoids                                                  # Getting the json data from the url
import requests

crimeFile                  = "NYPD_Complaint_Data_Historic_2010_2011.csv"
crimeOutFile               = "NYPD_Complaint_Data_Historic_WITH_CENSUS_DATA.csv"
crimeOutFile_ColChanged    = "NYPD_Complaint_Data_Historic_WITH_CENSUS_DATA_ColChanged.csv"
crimeOutFile_Filtered      = "NYPD_Complaint_Data_Historic_WITH_CENSUS_DATA_Filtered.csv"

crimeDF = pd.read_csv(crimeFile)
csvHeader = ["Geoid","CrimeComplaint", "CrimeCount", "CountyName", "CensusTract_2010_NAME"]

OFFENSE_GROUP = "OFNS_DESC"
OFFENSE_NAME  = "PD_DESC"
REPORT_DATE   = "CMPLNT_FR_DT" 

# 1) Appending New Cols - Cols for census data:
# crimeDF["Geoid"] = int
# crimeDF["Date"]  = str         #rpt_dt
# crimeDF["Month"] = int
# crimeDF["Year"]  = int
# crimeDF["CrimeComplaint"] = str
# crimeDF["CountyName"]     = str 
# crimeDF["CensusTract_2010_NAME"] = str  
# censusCols = ["CountyName", "Geoid", "CensusTract_2010_NAME"]

# currCols = list(crimeDF.columns)
# for newCol in expandCols:
#     if newCol not in currCols:
#         crimeDF[newCol] = np.str
    
# # 2) Func
# def getCensusTract(longitude, latitude, retryRun=0):                                                                 # returns an array [censusTract, CensusBlock, CountyName]
#     url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={0}&y={1}&benchmark=Public_AR_Census2010&vintage=Census2010_Census2010&format=json".format(longitude,latitude)
#     if retryRun == 11:                                                                                              # Failed to get json data 11 times with this longitude and latitude so need to skip this one
#         print("*****Failed 11 times to get geodata so will insert 'error'*****")
#         return [str("error"), str("error"), str("error")]
#     try:
#         response = requests.get(url)
#         dataJSON = response.json()
#         data    = dataJSON["result"]
#         countyNAME    = data["geographies"]["Counties"][0]["NAME"] 
#         GEOID =  data["geographies"]["Census Tracts"][0]["GEOID"]
#         tractNAME     = data["geographies"]["Census Tracts"][0]["NAME"]
#         return [
#             str(countyNAME), 
#             str(GEOID), 
#             str(tractNAME)
#         ]
#     except:
#         retryRun+=1
#         print("_____Error on longitude, latitude: "+str(longitude)+","+str(latitude) + ".....retrying... "+str(retryRun))
#         return getCensusTract(longitude, latitude,retryRun)                                                         # need to return the recursive function
#     return

# # 3) Using Long and Lat to populate the Census Data Cols (WILL TAKE VERY LONG TO DO!)
# # print("...Getting Census Information of Crime Reports from Longitude and Latitude Coordinates...\n...Should take some a long time...")
# rowsToDel = []
# for row in range(0,len(crimeDF)):
#     retryRun = 0
#     lat = float(crimeDF.iloc[row]["Latitude"])
#     lon = float(crimeDF.iloc[row]["Longitude"])
#     if np.isnan(lon) or np.isnan(lat):
#         print("***This report has no Longitude and Latitude Data so will skip it and delete it from the df***")
#         rowsToDel.append(row)
#         continue
    
#     returnArray = getCensusTract(lon, lat)            
#     if len(censusCols) == len(returnArray):
#         for i in range(0, len(censusCols)):
#             crimeDF.at[row, censusCols[i]] = returnArray[i] 
#     else:
#         print("*** Number of col to add and values to polulate cols are not the same!! ******") 
#     if row%20 == 0:
#         print(row)
#         crimeDF.to_csv(crimeOutFile, index=False)   # Saving just in case 
# crimeDF.to_csv(crimeOutFile, index=False)   # Saving just in case 

# 4) Populate the Geoid (exclude block id from, Date, Month, Year, and CrimeComplaint Cols
crimeDF = pd.read_csv(crimeOutFile)
print("...Filling the Month, Date, Yr, CrimeComplaint Cols")
noCrimeDesc = []
for row in range(0,len(crimeDF)):
    try:
        crimeDF.at[row, "Geoid"] = int(crimeDF.iloc[row]["Geoid"])
    except:
        print('error'+ "    "+str(crimeDF.iloc[row]["Geoid"]))
        crimeDF.at[row, "Geoid"] = 0
    ROW_OFFENSE_GROUP = crimeDF.iloc[row][OFFENSE_GROUP] 
    ROW_OFFENSE_NAME  = crimeDF.iloc[row][OFFENSE_NAME]
    
    if (pd.isnull(ROW_OFFENSE_GROUP) == False) and (pd.isnull(ROW_OFFENSE_NAME) == False):
        crimeDF.at[row, "CrimeComplaint"] = "[" + ROW_OFFENSE_GROUP + "] " + ROW_OFFENSE_NAME
    elif (pd.isnull(ROW_OFFENSE_GROUP) == False) and (pd.isnull(ROW_OFFENSE_NAME) == True):
        crimeDF.at[row, "CrimeComplaint"] = "[" + ROW_OFFENSE_GROUP + "] " + "Not Stated"
    elif (pd.isnull(ROW_OFFENSE_GROUP) == True) and (pd.isnull(ROW_OFFENSE_NAME) == False):
        crimeDF.at[row, "CrimeComplaint"] = ROW_OFFENSE_NAME
    else:
        noCrimeDesc.append(row)
        continue
        
    date = crimeDF.iloc[row][REPORT_DATE].split("/")
    dateMDY = date[2]+"-"+date[1]+"-"+date[0]
    crimeDF.at[row, "Date"] = dateMDY
    crimeDF.at[row, "Year"] = int(date[0])
    crimeDF.at[row, "Month"] = int(date[1])
crimeDF = crimeDF.sort_values(by=['Year', 'Month', OFFENSE_GROUP, 'CrimeComplaint', 'CountyName','Geoid'], ascending=False)
print(noCrimeDesc)
crimeDF = crimeDF.reset_index(drop=True)   
crimeDF.to_csv(crimeOutFile_ColChanged, index=False)


# 5) Filtering 1: Filter the rows by geoiid and the crimes
crimeDF = pd.read_csv(crimeOutFile_ColChanged)
filteredDF = pd.DataFrame(columns=csvHeader)  

print("...Filtering crime data...")
skipIndex = [] 
for row in range(0,len(crimeDF)):
    if row in skipIndex:
        continue
    geoidDF = crimeDF.loc[   
        (crimeDF['Geoid'] == crimeDF['Geoid'][row]) &
        (crimeDF['CrimeComplaint'] == crimeDF['CrimeComplaint'][row]) 
    ] 
    skipIndex.extend(geoidDF.index.tolist())  
    geoidDF = geoidDF.filter(csvHeader)    
    geoidDF = geoidDF.reset_index(drop=True)
    
    geoidDF = geoidDF[0:1]
    geoidDF["CrimeCount"] = len(geoidDF)
    filteredDF = filteredDF.append(geoidDF, sort=False)
    if len(geoidDF)>10:
        print("---------------------------------"+str(geoidDF.iloc[0]['Geoid'])+"-------------"+str(len(geoidDF))+"\n")
filteredDF = filteredDF.sort_values(by=['CountyName','CrimeComplaint', 'Geoid'], ascending=False)
filteredDF = filteredDF.reset_index(drop=True)
filteredDF.to_csv(crimeOutFile_Filtered, index=False)
print("DONE1")


# 6) Filtering 2: Need to make the CrimeComplaint the columns not the rows
crimeDF = pd.read_csv(crimeOutFile_Filtered)
crimeCompCols = set(crimeDF.CrimeComplaint)
for newCol in crimeCompCols:
    crimeDF[newCol] = 0
crimeDF["TotalCrime"] = 0

csvHeader = list(crimeDF.columns) 
filteredDF = pd.DataFrame(columns=csvHeader)  

# Here im collecting all rows that got the same geoid. Will list all the unique crimes there. Will set the sum of each into the cols of the first row, drop the rest, append the df to the filteredDF and put into csv
skipIndex = [] 
for row in range(0,len(crimeDF)):
    if row in skipIndex:
        continue
    geoidDF = crimeDF.loc[   
        (crimeDF['Geoid'] == crimeDF['Geoid'][row])
    ] 
    skipIndex.extend(geoidDF.index.tolist())  
    geoidDF = geoidDF.reset_index(drop=True)
    geoidDF.at[0, "TotalCrime"] = geoidDF.CrimeCount.sum()
    
    crimeCols = list(geoidDF.CrimeComplaint)
    crimeCategory = dict()
    for row in range(0,len(geoidDF)):
        crime = geoidDF.iloc[row]["CrimeComplaint"]
        crimeCategory[crime] = geoidDF.iloc[row]["CrimeCount"]
        
    for crimeName in crimeCols:
        geoidDF.at[0,crime] = crimeCategory[crime]
    geoidDF = geoidDF[0:1]
    filteredDF = filteredDF.append(geoidDF, sort=False)
filteredDF
filteredDF = filteredDF.sort_values(by=['CountyName','CrimeComplaint', 'Geoid'], ascending=False)
filteredDF = filteredDF.reset_index(drop=True)
filteredDF = filteredDF.drop(columns=['CrimeComplaint', 'CrimeCount'])
filteredDF.to_csv(crimeOutFile_Filtered, index=False)
print("DONE2")