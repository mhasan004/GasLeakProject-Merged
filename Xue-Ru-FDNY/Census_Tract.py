## after getting long/lat find census tract using this


from urllib.request import urlopen                       # Getting the json data from the url
import requests
import json
import pandas as pd                                     # To read and write csv files
import time

csvfile = "unprocess.csv"


### GETTING CENSUS DATA FROM COORDS AND ADDING TO CSV ####

# FUNCTION: Get Census Tract from Longitude and Latitude coordintes using the Census Beru's API which returns a JSON file
def getCensusTract(longitude, latitude, retryRun=0):  # returns an array [CensusTrack, CensusBlock, CountyName]
    url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={0}&y={1}&benchmark=Public_AR_Census2010&vintage=Census2010_Census2010&format=json".format(
        longitude, latitude)
    if retryRun == 11:  # Failed to get json data 11 times with this longitude and latitude so need to skip this one
        print("failed 11 times")
        return [str(0), str(0)]
    try:
        response = requests.get(url)
        dataJSON = response.json()
        data = dataJSON["result"]
        county = data["geographies"]["Counties"][0]["BASENAME"]
        geoid = data["geographies"]["Census Tracts"][0]["GEOID"]
        #county = data["geographies"]["Counties"][0]["NAME"]
        return [str(county), str(geoid)]
    except:
        retryRun += 1
        print("******** Error on longitude, latitude: " + str(longitude) + "," + str(
            latitude) + " ------ retrying " + str(retryRun))
        return getCensusTract(longitude, latitude, retryRun)  # *****need to return the recursive function


# a) Will modify GasHistory_ConEdison.csv to have the CensusTract, CensusBlock, and CountyName columns

df = pd.read_csv(csvfile)  # read the csv file and store to df
df["CountyName"] = "0.0"

for row in range(0, len(df)):
    # b) using the lat and long coords of each entry to find the census data and adding to the respective arrays to add to csv col later
    returnArray = getCensusTract(float(df.loc[row]["lon"].item()),
                                 float(df.loc[row]["lat"].item()))  # data.iat[i,4] = lat   # data.iat[i,5] = lon
    df.at[row, "CountyName"] = returnArray[0]
    df.at[row, "Geoid2010"] = returnArray[1]
    if row % 100 == 0:
        print(row)

print(df)
df.to_csv("processed.csv", encoding='utf-8',index=False)