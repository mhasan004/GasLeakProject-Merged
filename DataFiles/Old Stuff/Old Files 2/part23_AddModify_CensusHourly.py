# Variables to chnage: csvConEdFile and for returnArray specify the Latitude and Longitude csv column names
########################################################################### PART 2:  CODE AFER CON EDOSN SCRAPER. Taking the csv file and then  #####################################################
# make a new csv that has the: censusTract, date, hour, report count for that tract for that hour
# census api url format:  https://geocoding.geo.census.gov/geocoder/geographies/coordinatesx=latitude&y=longitude&benchmark=&vintage=&format=json

from urllib.request import urlopen                                                      # Getting the json data from the url
import requests
import json
import pandas as pd                                                                     # To read and write csv files
import time                                                                             # maybe api calls will help if i slow a bit

csvConEdFile  = "GasHistory_ConEdisonTracts.csv"                                        # In part 2: will take this csv and will add the Census Tract, Census Block, Cunty Name, and Hour columns
csvOutFile    = "GasHistory_reportsPerCensusTract.csv"                                  # In Part 3: From the csv will create new csv based on number of reports per census tract per given hr

################################################################################### GETTING CENSUS DATA FROM COORDS AND ADDING TO CSV ##############################################################
# FUNCTION: Get Census Tract from Longitude and Latitude coordintes using the Census Beru's API which returns a JSON file 
def getCensusTract(longitude, latitude,retryRun=0):                                     # returns an array [censusTract, CensusBlock, CountyName]
    url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?y={0}&x={1}&benchmark=Public_AR_Current&vintage=Current_Current&format=json".format(longitude,latitude)
    response = requests.get(url)
    dataJSON = response.json()
    data = dataJSON["result"]

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
    returnArray = getCensusTract(float(df.loc[row]["Longitude"].item()), float(df.loc[row]["Latitude"].item()))
    censusTract.append(returnArray[0])
    censusBlock.append(returnArray[1])
    countyName.append(returnArray[2])

# c) Will make 3 new columns and will fill them up using the 3 census arrays
df['CensusTract'] = censusTract          
df['CensusBlock'] = censusBlock        
df['CountyName']  = countyName      
df.to_csv(csvConEdFile, index=False)                                

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

################################################################################### Part 3: Make new file based on hour and census tract and num of reps ###########################
# The new csv file is empty so will add the headers:
with open(csvOutFile, 'r') as csvOutFile:
        csv_dict = [row for row in csv.DictReader(csvOutFile)]
        if len(csv_dict) == 0:
            csvHeader = ["Date,Hour,CensusTract,NumberOfReports"]
            with open(csvOutFile, 'w', newline='') as outf:
                writer = csv.writer(outf)
                writer.writerow(csvHeader)


indexToSkip = []
noRepeatSet = set()
df = pd.read_csv(csvConEdFile) 
for row in range(0,len(df)):
    date = df.iloc[row]["Date"]
    if row not in indexToSkip:                                                                     # A) Do this Date if i didnt do so already: 
        dateDF = df[df.Date == date]                                                                    # 1) new df = target rows (which were recorded in the same date?)
        indexToSkip.extend(df.index[df["Date"] == date].tolist())                                       # 2) adding the index of those targeted rows so can skip them since we go down the entires

        hourToSkip = []
        for rowHour in range(0, len(dateDF)):
            hour = dateDF.iloc[rowHour]["Hour"]   
            if rowHour not in hourToSkip:                                                           # B) Do this Hour if i didnt do so already:                 
                hourlyDF = dateDF[dateDF.Hour == hour]                                                  # 1) new df = target rows (of those same date, which were recorded in the same hour?)                  
                hourToSkip.extend(dateDF.index[dateDF["Hour"] == hour].tolist())                        # 2) adding the index of those targeted rows so can skip when we go down the row for this date   
                
                tractToSkip = []
                s = ""
                for rowTract in range(0, len(hourlyDF)):                                    
                    tract = hourlyDF.iloc[rowTract]["CensusTract"]          
                    if rowTract not in tractToSkip:                                                 # C) Do this Census Tract if i didnt do so already: 
                        tractDF = hourlyDF[hourlyDF.CensusTract == tract]                               # 1) new df = target rows (of those same hours, which were recorded in the same census tract?)                  
                        tractToSkip.extend(hourlyDF.index[hourlyDF["CensusTract"] == tract].tolist())   # 2) adding the index of those targeted rows so can skip when we go down the row for this hour
                        if len(tractDF) >= 2:
                            print("----------"+str(len(tractDF) ))
                        s += tractDF.iloc[0]["Date"] + "," + str(tractDF.iloc[0]["Hour"]) + "," + str(tractDF.iloc[0]["CensusTract"]) + "," + str(len(tractDF)) # D) Index is 0 because im just counding how many there are in the df right now. Only need the Date, Hour, Tract, and count data
                        noRepeatSet.add(s)
                        s = ""

with open(csvOutFile,'a') as outCSV:                                                                # Write the stuff to the csv file
    for x in noRepeatSet:
        outCSV.write(x+"\n")

# there are only six 2's (manual check). If i had 783 before. And not i have 777. (783-777 = 6) so it all good