# Scraper v3: Will periodicly scrape the con edison website to find new gas leak reports, then use the Census Bureau API to find Census Data of those locations and append to my csv file. Will then read the file and make a new csv file to trck reports per hour per Census Tract per day and create a map.
# Part A (section 1 to 4, 6, 8): Mahmudul Hasan. Script to scrape JSON Gas Leak Data points from ConEdison everyday and put them into a csv file for further use
    # In the ConEdison Gas Leak Report Map, each report in the map represents a gas leak report. Each report has these seven keys: TicketNumber, Latitude, Longitude, Zipcode, Classification Type, Date Reported, Last Inspected.
    # a) We need to constantly add new repots to out list so what tickets do we currently have? read the ticket col of the "csvConEdFile" and add the tickets to "ticketSet"
    # b) Scrape the JSON html response and using pandas to put the contents into a dataframe called "jsonDF"
    # c) See if there is a new report, if there is create a new DF that stores info for those new tickets: 
        # Read the csv file and make a dataframe with pandas. Now compare the "TicketNumber" columns of both the "csvDF" and "jsonDF" using left merge and store it as a new DF - "mergedDF" -  which has the info of all the tickets and has a new column called "_merged" which shows what ticket are in both DF and what tickets are in only json response. 
        # Filter "mergedDF" where "_merged" col = ""left_only" (new tickets not in file) and print the list of ticket names to an array - "newTicketsArray" 
        # Create a new DF - "newTicketDF" - which will have the columns of my current csv file. Will use "newTicketArray" to go through the "jsonDf" and add the rows to "newTicketDF" so i have a DF that has all the new tickets
    # d) If there is a new report, add append the keys of that report into "csvConEdFile" and push the latest changes to github
# Part B (section 5):  Will edit the csv to have new columns for the Census Tract, Census Block, County Name and the hour only
    # Will use the census bureau api to get census data from the lat and lon coords using this url request:  https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x=LONGITUDE&y=LATITUDE&benchmark=Public_AR_Current&vintage=Current_Current&format=json
# Part C (section 7): Will create a new csv that lists the reports per census tract per hour for that day. Headers: Date, Hour, CensusTract, NumberOfReports


import json
import csv
import pandas as pd                                                                                 # to read csv file and store conent into a data frame. To turn json response string into a dataframe
import datetime,re                                                                                  # to turn Microsoft JSON date /Date()/ to normal date
import requests                                                                                     # Getting html data
from bs4 import BeautifulSoup                                                                       # Parse the HTML data
from apscheduler.schedulers.blocking import BlockingScheduler                                       # Sceduler. Will run a function every x seconds/minutes/hours
from git import Repo                                                                                # (GitPython) To push changes to gh


# SETTING UP GLOBAL VARIABLES: need to change the first eight variables below
csvFile = "GasHistory_ConEdisonTracts.csv"                                                          # add new tickets to the end of the csv file
csvHourlyFile = "GasHistory_ReportFrequency_Hourly.csv"                                              # In PART C we will turn the ticket history data to hourly data
jsonFile = "SOME_JSON_FILE.json"                                                                    # Normally the programm will be scrape JSOn data from a url but sometimes it might need to extract JSOn data from a file. See step 2)
url = 'https://apps.coned.com/gasleakmapweb/GasLeakMapWeb.aspx?ajax=true&'                          # Url to scrape JSOn data from
dropCol = True                                                                                      # If you want to drop a column, specify which ones in step 2 in WebscraperJsonToCSV()
replaceColWith = ["Date", "Time", "Hour", "CensusTract", "CensusBlock", "CountyName" ]              # Replacing column DateReported with these "Date", "Time", "Hour and Made 3 more cols for Part 2 Census data

PATH_OF_GIT_REPO = r'/home/pi/repositories/gh/GasLeakProject'                                       # the path to the .git file (.git location on my raspberry pi)
# PATH_OF_GIT_REPO = r'/home/hasan/repositories/gh/GasLeakProject'                                  # the path to the .git file (.git location on my Laptop)
COMMIT_MESSAGE = 'Automated Push - New Ticket Update'                                               # the commmit message when it is pushed
scrapingCount = 0                                                                                   # Just counting how many times i have scraped the website while this was running

# GIT PUSH FUNCTION: Setting up function to automatically push changes to github when there is a new ticket so that I can have access to the latest chnages
def git_push():
    repo = Repo(PATH_OF_GIT_REPO)
    try:
        repo.remotes.origin.pull()                                                                  # try pulling new changes from the github repo (if there are any) so i can push changes
    except:
        print("Couldnt pull from repo")
    repo.git.add(update=True)
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    try:
        origin.push()                                                                               # try pushing the changes to github
        print("******** PUSHED TO GITHUB for Run " + str(scrapingCount)+"********")
    except:
        print('Some error occured while pushing the code')  


# FUNCTION TO TURN MICROSOFT JSON DATE TO mm/dd/yyyy AND TIME: returns ["mm/dd/yyyy", "hh:mm AM/PM", "hh AM/PM"]
def turnToDateTimeHr(microsoftDate):         
    TimestampUtc = str(microsoftDate)
    TimestampUtc = re.split('\(|\)', TimestampUtc)[1][:10]
    dateRaw = datetime.datetime.fromtimestamp(int(TimestampUtc))
    dateFormatted = str(dateRaw.strftime('%m/%d/20%y %I:%M %p'))                                    # The datetime is of form: "mm/dd/tt hh:mm AM/PM"
    dateTimeSplit = dateFormatted.split(" ")                                                        # ["mm/dd/yyyy", "hh:mm", "AM/PM"]
    date = dateTimeSplit[0]                                                                         # Isolated the date string: "mm/dd/yyyy"
    time = dateTimeSplit[1] + " " + dateTimeSplit[2]                                                # Isolated the time string: "hh:mm AM/PM"
    hour = time.split(" ")[0].split(":")[0] + " " + dateTimeSplit[2]                                # Isolated the hour string: "hh AM/PM"   (will need for part 2)
    dateTimeHr = [date, time, hour]                                                                 # ["mm/dd/yyyy", "hh:mm AM/PM", "hh AM/PM"]
    return (dateTimeHr)                                                                

# PART B FUNCTION: Get [CensusTrack, CensusBlock, CountyName] from Longitude and Latitude coordintes using the Census Beru's API which returns a JSON file 
def getCensusTract(longitude, latitude,retryRun=0):                                                 # returns an array [censusTract, CensusBlock, CountyName]
    url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={0}&y={1}&benchmark=Public_AR_Current&vintage=Current_Current&format=json".format(longitude,latitude)
    if retryRun == 11:                                                                              # Failed to get json data 11 times with this longitude and latitude so need to skip this one
        print("*****Failed 11 times to get geodata so will insert 'error'*****")
        return [str("error"), str("error"), str("error")]
    try:
        response = requests.get(url)
        dataJSON = response.json()
        data = dataJSON["result"]
        track = data["geographies"]["Census Tracts"][0]["BASENAME"]
        block = data["geographies"]["2010 Census Blocks"][0]["BLOCK"]
        county = data["geographies"]["Counties"][0]["NAME"] 
        return [str(track), str(block), str(county)]
    except:
        retryRun+=1
        print("Error on longitude, latitude: "+str(longitude)+","+str(latitude) + ".....retrying... "+str(retryRun))
        return getCensusTract(longitude, latitude,retryRun)                                         # need to return the recursive function

# PART C FUNCTION: Make Hourly reports from the gas leak history csv file
def turnTicketHistoryToHourlyReport():
    global csvFile
    global csvHourlyFile
    csvOutHasData = False                                                                               # Does the out file have data already? if so can get it and use it and modify it
    inDF = pd.read_csv(csvFile)                                                                       # Read Tracts file
    csvHeader = ["Date","Hour","CensusTract","NumberOfReports"]                                         # My new csv need these headers        
    
    csvOutClear = open(csvHourlyFile, "w")
    csvOutClear.truncate()                                                                              # deleting everything in the file (will delete this code once i figure out how to update existing file)

    with open(csvHourlyFile, 'r') as csvFile:                                                              # Open the csv File so we can read it
        csvTable = [row for row in csv.DictReader(csvFile)]
        if len(csvTable) == 0:                                                                          # a) csv is empty so add my header: ['Date', 'Hour', 'CensusTract', 'NumberOfReports']
            with open(csvHourlyFile, 'w', newline='') as outf:
                writer = csv.writer(outf)
                writer.writerow(csvHeader)
                print("Added Header: "+str(csvHeader))
        else:
            csvHeader=list(pd.read_csv(csvHourlyFile).columns)                                             # b) Since the csv already had data, it means i will append new data to it so just use the header of that csv file.
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
              
        # groupedDF = pd.DataFrame(columns=csvHeader)                                                     # Making a new dataframe and letting it have the columns i want. When i append "inDF" rows, the cols of "inDF" will be added to it. Will finally get rid of unwanted cols with filter().     
        # groupedDF = groupedDF.append(inDF.loc[                                                          # groupedDF added tickets that have the same Census Tract, Hour, and Date. Will get rid of those unwanted cols from "inDF" next
        #     (inDF['Date'] == inDF['Date'][row]) & 
        #     (inDF['Hour'] == inDF['Hour'][row]) & 
        #     (inDF['CensusTract'] == float(inDF['CensusTract'][row]))    
        # ] 
        # skipIndex.extend(groupedDF.index.tolist())                                                      # already did this indexes so will skip them when "row" increments to them  
        # monthlyDF = monthlyDF.reset_index(drop=True)                                                    # resetting the index to restart from 0

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
    #     csvOutDF = pd.read_csv(csvHourlyFile)   
    #     differencesDF = outDF.merge(csvOutDF.drop_duplicates(), on=["Date","Hour","CensusTract"], how='outer', indicator=True) 
    #     print("----------------------------a")
    #     newDataDF = differencesDF.loc[differencesDF['_merge']=="left_only"]
    #     print(newDataDF)
    #     print("----------------------------b")
    #     print(differencesDF.loc[differencesDF['_merge']=="right_only"])

    print("Printing hourly report to "+csvHourlyFile+"...")
    with open(csvHourlyFile,'a') as outCSV:                                                               # Turning the DF into csv and appending the new data to the file
        outCSV.write(outDF.to_csv(header=False, index=False))


# THE SCHEDULER WILL RUN THIS MAIN FUNCTION EVER X SECONDS/MINUTES/HOURS
def WebscraperJsonToCSV():  
    global scrapingCount                                                                            # Setting up the web scraping global iteration counter for debugging purposes
    scrapingCount = scrapingCount + 1 
    # 1) GET JSON DATA: Webscrape the html response which is usually just the JSON data from the url and add to the JSON Dataframe: 
    # jsonDF = pd.read_json(jsonFile, orient='records')                                             # If im getting data from json file, comment out the rest of this section.
    try:
        res = requests.get(url)
        html_data = res.content                                                                     # Getting the HTML JSON data from the url 
        soup = BeautifulSoup(html_data, 'html.parser')                                              # parsing the html data with html parcer (can do stuuf like soup.title to get the title, soup.div, soup.li etc)
        text = soup.find_all(text=True)                                                             # Getting all the text thats in the soup
        jsonStr = ''                                                                                # turning text to string from so i can use pandas to turn it to a dataframe
        for t in text:
            jsonStr += '{} '.format(t)
        jsonDF = pd.read_json(jsonStr, orient='records')                                            # Turning the json string to a pandas dataframe
        print("Run Starting " + str(scrapingCount) + "       Reports Scraped: "+str(len(jsonDF)))
    except:
        print("Couldnt get the json data so will re-run function. This is Run "+ str(scrapingCount))
        return WebscraperJsonToCSV()


    # 2) MODIFY CSV FILE: a) CSV IS EMPTY: print the the headers I want. b) CSV NOT EMPTY: Get the header and that is what we will work with. Im also droping columns from json DF and adding new col titles to csvHeader array
    # My csv will not have the "LastInspected" and "DateReported" cols. Will drop "LastInspeccted" but will keep "DateReported" as we will break it down into three cols for my csv file: "Date,Time,Hour" and then will drop it at the end
    jsonDF = jsonDF.drop(columns=["LastInspected"])                                                 # Dropping this col fom the jsonDF                         
    csvHeader = list(jsonDF.drop(columns=["DateReported"]).columns.values)                          # (this change will be replced is csv has header) Title: "DateReported" Will be replaced by "Date,Time,Hour" So will now 
    csvHeader.extend(replaceColWith)                                                                # (this change will be replced is csv has header) Title: Adding the "Date,Time,Hour" to the title
    with open(csvFile, 'r') as csvfile:                                                             # Open the csv File so we can read it
        csvTable = [row for row in csv.DictReader(csvfile)]
        if len(csvTable) == 0:                                                                      # a) csv is empty so add my header: [TicketNumber,Latitude,Longitude,Zip,ClassificationTyp,Date,Time,Hour
            with open(csvFile, 'w', newline='') as outf:
                writer = csv.writer(outf)
                writer.writerow(csvHeader)
                print("Added Header: "+str(csvHeader))
        else:
            csvHeader=list(pd.read_csv(csvFile).columns)                                            # b) Since the csv already had data, it means i will append new data to it so just use the header of that csv file.
            

    # 3) FIND THE NEW TICKETS 
    csvDF = pd.read_csv(csvFile)                                                                    # Reading the list of tickets i current have on file and making a dataframe to read them
    mergedDF = jsonDF.merge(csvDF.drop_duplicates(), on=['TicketNumber'], how='left', indicator=True) # Will take all the keys of jsonDF. Will merge with keys of right DF (wont display) and will keep only the merged keys 
    newTicketsArray = list(mergedDF.loc[mergedDF['_merge']=="left_only", "TicketNumber"])           # This array holds all the tickets i dont have in my file
    newTicketDF = pd.DataFrame(columns=csvHeader)                                                   # Making empty dataframe that has the columns of my csv file. This will be the df that will be modified and pushed to my csv
    if len(newTicketsArray) == 0:                                                                   # No new Tickets, can end this iteration
        return

    for row in range(0,len(newTicketsArray)):                                                       # Going through the array of new ticket number and adding only their rows to th new data frame
        print(newTicketsArray[row] + " not in set so adding it-----")
        newTicketDF = newTicketDF.append(jsonDF[jsonDF.TicketNumber == newTicketsArray[row]], sort=False, ignore_index=True)

    # 4 &) TURN THE MICROSOFT DATE IN "DateReported" INTO STANDARD FORMAT AND SEPERATE INTO "Date", "Time", "Hour" COLUMNS AND THEN DROP COLUMN "DateReported" :
    # 5) WILL USE THE CENSUS BUREAU API TO GET CENSUS DATA BASED ON EACH TICKET'S LONGITUDE AND LATITUDE DATA:             
    for row in range(0, len(newTicketDF)):                                                          # Replacing DateReported with Date, Time, Hour columns
        dateTimeHr = turnToDateTimeHr(str(newTicketDF["DateReported"][row]))                        # Takes the microsoft date and returns: ["mm/dd/yyyy", "hh:mm AM/PM", "hh AM/PM"]
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("Date")] = dateTimeHr[0]                  # Adding the Date, Time, Hour values to the appropriate cells
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("Time")] = dateTimeHr[1]
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("Hour")] = dateTimeHr[2]
        print("Getting Census data...")
        returnArray = getCensusTract(float(newTicketDF.loc[row]["Longitude"].item()), float(newTicketDF.loc[row]["Latitude"].item()))   # returns: [CensusTrack, CensusBlock, CountyName] from Census Beru's API
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("CensusTract")] = returnArray[0]          # Adding the CensusTrack, CensusBlock, CountyName values to the appropriate cells
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("CensusBlock")] = returnArray[1]
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("CountyName")] =  returnArray[2]
    newTicketDF = newTicketDF.drop(columns=["DateReported"])                                        # Finally dropping the "DateReported" column    

    # 6) WRITE TO CSV FILE:
    print("Appending new Gas Leak reports to file...")
    with open(csvFile,'a') as outCSV:                                                               # Turning the DF into csv and appending the new data to the file
        outCSV.write(newTicketDF.to_csv(header=False, index=False))
    
    # 7) WRITING NEW HOURLY FILE BASED ON GAS LEAK HISTORY FILE AND PUSHING TO GH
    turnTicketHistoryToHourlyReport()
    git_push()



# 8) RESCAN FOR TICKETS every x time using sceduler
scheduler = BlockingScheduler()
scheduler.add_job(WebscraperJsonToCSV, 'interval', minutes=30) # need to give enough time to go the entire process
scheduler.start()


# Notes: Turning the Gas Leak Report data into hourly reports...) process took forever, need to make it do it faster