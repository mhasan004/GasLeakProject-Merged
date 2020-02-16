# Variables to chnage: csvConEdFile and for returnArray specify the Latitude and Longitude csv column names
# PART 2 CODE AFER CON EDOSN SCRAPER. Taking the csv file and then 
# a) make a new csv that has the: censusTract, date, hour, report count for that tract for that hour
# Census API doc:         https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf
# census api url format:  https://geocoding.geo.census.gov/geocoder/geographies/coordinatesx=longitude&y=latitude&benchmark=&vintage=&format=json
# census api url example: https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x=-78.8543293&y=41.6567756&benchmark=Public_AR_Current&vintage=Current_Current&format=json
    # json result of the top search given this random lat long coordinate is results: input and geographies. geographics has: 2010 census blocks, states, countries, census tracts

from urllib.request import urlopen                                                      # Getting the json data from the url
import requests
import json
import pandas as pd                                                                     # To read and write csv files

csvConEdFile  = "GasHistory_ConEdisonTracts.csv"
################################################################################### GETTING CENSUS DATA FROM COORDS AND ADDING TO CSV ##############################################################
# FUNCTION: Get Census Tract from Longitude and Latitude coordintes using the Census Beru's API which returns a JSON file 
def getCensusTract(longitude, latitude,retryRun=0):                                     # returns an array [censusTract, CensusBlock, CountyName]
    # try:
    url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={0}&y={1}&benchmark=Public_AR_Current&vintage=Current_Current&format=json".format(longitude,latitude)
    # response = urlopen(url)
    # dataJSON = json.loads(response.read())
    response = requests.get(url)
    dataJSON = response.json()
    data = dataJSON["result"]
    # except:
    #     print("Couldnt get response, will retry...")
    #     time.sleep(10)
    #     return getCensusTract(longitude, latitude)
    if retryRun == 11:                                                                  # Failed to get json data 11 times with this longitude and latitude so need to skip this one
        print("*****Failed 11 times to get geodata so will print insert 'error'*****")
        return [str("error"), str("error"), str("error")]
    try:
        track = data["geographies"]["Census Tracts"][0]["BASENAME"]
        block = data["geographies"]["2010 Census Blocks"][0]["BLOCK"]
        county = data["geographies"]["Counties"][0]["NAME"] 
        return [str(track), str(block), str(county)]
    except:
        retryRun+=1
        print("******** Error on longitude, latitude: "+str(longitude)+","+str(latitude) + " ------ retrying "+str(retryRun))
        return getCensusTract(longitude, latitude,retryRun)                             # *****need to return the recursive function

# a) Will modify GasHistory_ConEdison.csv to have the CensusTract, CensusBlock, and CountyName columns
censusTract = []
censusBlock = []
countyName = []
df = pd.read_csv(csvConEdFile)                                                          # read the csv file and store to df
for row in range(0,len(df)):
    retryRun = 0
    # b) using the lat and long coords of each entry to find the census data and adding to the respective arrays to add to csv col later
    returnArray = getCensusTract(float(df.iloc[row]["Longitude"].item()), float(df.iloc[row]["Latitude"].item()))
    censusTract.append(returnArray[0])
    censusBlock.append(returnArray[1])
    countyName.append(returnArray[2])

# c) Will make 3 new columns and will fill them up using the 3 census arrays
df['CensusTract'] = censusTract          
df['CensusBlock'] = censusBlock        
df['CountyName']  = countyName      
df.to_csv(csvConEdFile, index=False))                                

#################################################################################### CHANGING DATETIME COL TO DATE AND TIME AND HOUR COL ####################################################################
df = pd.read_csv(csvConEdFile)  
dateArray = []                                                          # adding new date column:    mm/dd/yyyy
timeArray = []                                                          # adding new time column:    hh:mm AM/PM
hourArray = []                                                          # adding new hour column:    h                                   
for row in range(0,len(df)):
    dateTime = df["DateReported"][row].split(' ')                       # [mm/dd/yyyy, time, am/pm]
    dateArray.append(dateTime[0])
    timeArray.append(dateTime[1]+" "+dateTime[2])
    hourArray.append(dateTime[1].split(":")[0]+" "+dateTime[2])
df['Date'] = dateArray          
df['Time'] = timeArray    
df['Hour'] = hourArray    
df.to_csv(csvConEdFile, index=False))  

