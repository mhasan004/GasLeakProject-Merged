# This is the scraper with Part 2 and Part 3 Code: Will scrape data, add the Census data columns and then make a new csv
# Part 1: Mahmudul Hasan. Script to scrape JSON Gas Leak Data points from ConEdison everyday and put them into a csv file for further use
    # In the ConEdison Gas Leak Report Map, each report in the map represents a gas leak report. Each report has these seven keys: TicketNumber, Latitude, Longitude, Zipcode, Classification Type, Date Reported, Last Inspected.
    # a) We need to constantly add new repots to out list so what tickets do we currently have? read the ticket col of the "csvConEdFile" and add the tickets to "ticketSet"
    # b) Scrape the JSON html response and using pandas to put the contents into a dataframe called "jsonDF"
    # c) See if there is a new report: Loop through each JSON obbject in "jsonDF" and compare it to the reports are already exists in "ticketSet"
    # d) If there is a new report, add append the keys of that report into "csvConEdFile", "ticketListFile" and push the latest changes to github
# Part 2:  Will edit the csv to have new columns for the Census Tract, Census Block, County Name and the hour only
    # Will use the census api to get census data from the lat and lon coords using this url request:  https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x=LONGITUDE&y=LATITUDE&benchmark=Public_AR_Current&vintage=Current_Current&format=json
# Part 3: Will create a new csv that lists the reports per census tract per hour for that day. Headers: Date, Hour, Census Tract, Number of Reports

import json
import csv
import pandas as pd                                                                     # to read csv file and store conent into a data frame. To turn json response string into a dataframe
import datetime,re                                                                      # to turn Microsoft JSON date /Date()/ to normal date
import requests                                                                         # Getting html data
from bs4 import BeautifulSoup                                                           # Parse the HTML data
from apscheduler.schedulers.blocking import BlockingScheduler                           # Sceduler. Will run a function every x seconds/minutes/hours
from git import Repo                                                                    # (GitPython) To push changes to gh


# SETTING UP GLOBAL VARIABLES: need to change the first eight variables below
csvFile = "test.csv"#"GasHistory_ConEdison.csv"                                         # add new tickets to the end of the csv file
ticketListFile = "test.txt"#"conEd_TicketList.txt"                                      # add to end (just for me to see what i got)
jsonFile = "SOME_JSON_FILE_WITH_SAME_KEYS.json"                                         # Normally the programm will be scrape JSOn data from a url but sometimes it might need to extract JSOn data from a file. See step 2)
url = 'https://apps.coned.com/gasleakmapweb/GasLeakMapWeb.aspx?ajax=true&'              # Url to scrape JSOn data from
dropCol = True                                                                          # If you want to drop a column, specify which ones in step 2 in WebscraperJsonToCSV()
addCols = ["Date", "Time", "Hour"]                                                   # Replacing column DateReported with these cols
# csvHeader = ["TicketNumber","Longitude","Latitude","Zipcode","Classification","Date", "Time", "Hour"]
# keys= [                                                                                 # The JSON report keys( better to use key iteration, instead i went through the columns of the dictionary with this)
#     "TicketNumber",
#     "Latitude",
#     "Longitude",
#     "Zip",
#     "ClassificationType",
#     "DateReported",
#     "LastInspected"
# ]

PATH_OF_GIT_REPO = r'/home/pi/repositories/gh/GasLeakProject'                           # the path to the .git file (.git location on my raspberry pi)
#PATH_OF_GIT_REPO = r'/home/hasan/repositories/gh/GasLeakProject'                       # the path to the .git file (.git location on my Laptop)
COMMIT_MESSAGE = 'Automated Push - New Ticket Update'                                   # the commmit message when it is pushed
ticketSet = set()                                                                       # need to add what i got in the csv atm
scrapingCount = 0                                                                       # Just counting how many times i have scraped the website while this was running

# GIT PUSH FUNCTION: Setting up function to automatically push changes to github when there is a new ticket so that I can have access to the latest chnages
def git_push():
    repo = Repo(PATH_OF_GIT_REPO)
    try:
        repo.remotes.origin.pull()                                                      # try pulling new changes from the github repo (if there are any) so i can push changes
    except:
        print("Couldnt pull from repo")
    repo.git.add(update=True)
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    try:
        origin.push()                                                                   # try pushing the changes to github
        print("******** PUSHED TO GITHUB for Run " + str(scrapingCount)+"********")
    except:
        print('Some error occured while pushing the code')  
  

# FUNCTION TO TURN MICROSOFT JSON DATE TO mm/dd/yyyy AND TIME: returns ["mm/dd/yyyy", "hh:mm AM/PM", "hh AM/PM"]
def turnToDateTimeHr(microsoftDate):         
    TimestampUtc = str(microsoftDate)
    TimestampUtc = re.split('\(|\)', TimestampUtc)[1][:10]
    dateRaw = datetime.datetime.fromtimestamp(int(TimestampUtc))
    dateFormatted = str(dateRaw.strftime('%m/%d/20%y %I:%M %p'))                        # The datetime is of form: "mm/dd/tt hh:mm AM/PM"
    dateTimeSplit = dateFormatted.split(" ")                                            # ["mm/dd/yyyy", "hh:mm", "AM/PM"]
    date = dateTimeSplit[0]                                                             # Isolated the date string: "mm/dd/yyyy"
    time = dateTimeSplit[1] + " " + dateTimeSplit[2]                                    # Isolated the time string: "hh:mm AM/PM"
    hour = time.split(" ")[0].split(":")[0] + " " + dateTimeSplit[2]                    # Isolated the hour string: "hh AM/PM"   (will need for part 2)
    dateTimeHr = [date, time, hour]                                                     # ["mm/dd/yyyy", "hh:mm AM/PM", "hh AM/PM"]
    return (dateTimeHr)                                                                

# THE SCHEDULER WILL RUN THIS MAIN FUNCTION EVER X SECONDS/MINUTES/HOURS
def WebscraperJsonToCSV():  
    # Set up the web scraping iteration counter for debugging purposes
    global scrapingCount                                                                # Indicate that im using the global value
    scrapingCount = scrapingCount + 1 
    isNewTicket = False
        
    # 1) GET JSON DATA: Webscrape the html response which is usually just the JSON data from the url and add to the JSON Dataframe: 
    # jsonDF = pd.read_json(jsonFile, orient='records')                               # If im getting data from json file, comment out the rest of this section. form: jsonDF[keys[i]/colStr(report keys)][j/rowsnumber(reports)]
    try:
        res = requests.get(url)
        html_data = res.content                                                         # Getting the HTML JSON data from the url 
        soup = BeautifulSoup(html_data, 'html.parser')                                  # parsing the html data with html parcer (can do stuuf like soup.title to get the title, soup.div, soup.li etc)
        text = soup.find_all(text=True)                                                 # Getting all the text thats in the soup
        
        jsonStr = ''                                                                    # turning text to string from so i can use pandas to turn it to a dataframe
        for t in text:
            jsonStr += '{} '.format(t)
        jsonDF = pd.read_json(jsonStr, orient='records')                              # Turning the json string to a pandas dataframe
    except:
        print("Couldnt get the json data so will re-run function. This is Run "+ str(scrapingCount))
        return WebscraperJsonToCSV()
    

    # 2) If the csv is empty, print the header. Im also droping columns from json DF and adding new col titles to csvHeader array
    if dropCol == True:
        jsonDF = jsonDF.drop(columns=["LastInspected"])                                 # Dropping this col fom the jsonDF                         
    csvHeader = list(jsonDF.drop(columns=["DateReported"]).columns.values)              # "DateReported" Will be replaced by "Date,Time,Hour" So will now 
    csvHeader.extend(addCols)

    with open(csvFile, 'r') as csvfile:
        csv_table = [row for row in csv.DictReader(csvfile)]
        if len(csv_table) == 0:
            with open(csvFile, 'w', newline='') as outf:
                writer = csv.writer(outf)
                writer.writerow(csvHeader)
        
    # 3) CHECK WHAT TICKETS WE ALREADY GOT FROM THE .CSV FILE AND ADD NEW TICKETS TO ticketSet and .txt file: Read the csv file and add "TicketNumbers" to the "ticketSet" and print ticketNumber to ticketList.txt" for storage: 
    csvDF = pd.read_csv(csvFile)                                                      # ***csvDF[colStr][rowNumber]
    outTXT = open(ticketListFile,"w+")                                                  # Settign up to write to txt file
    for row in range(0,len(csvDF)):
        ticketSet.add(str(csvDF["TicketNumber"][row]))    
        outTXT.write(str(csvDF["TicketNumber"][row])+"\n")                            # there is an error so cant continue so end this

    # 4) CHECK IF NEW TICKET: See if the tickets in "jsonDF" are in "ticketDict". If we have have it, add to "ticketDic", and .txt and .csv file for stoage. If we have it, skip this row since we have this info already. 
    for row in range(0, len(jsonDF)):
        if jsonDF["TicketNumber"][row] not in ticketSet:                              # If we DONT have this ticket add it
            isNewTicket = True                                                          # This is a new ticket so push the new files
            print(str(jsonDF["TicketNumber"][row])+ " not in set so adding it")
            ticketSet.add(jsonDF["TicketNumber"][row])
            outTXT.write(jsonDF["TicketNumber"][row]+"\n")                            # add new ticket to txt file  
            with open(csvFile,'a') as outCSV:                                           # Write the new Ticket object to csv file
                s=""
                for col in jsonDF.columns:                                       # go through each column property of the report. len(keys) -1 because im skipping the last key which is "LastInspected" (not needed)
                    if col == "DateReported":                                     # Need to change the Microsoft time to mm/dd/yyyy
                        dateTimeHr = turnToDateTimeHr(str(jsonDF[col][row]))    # Takes the microsoft date and returns: ["mm/dd/yyyy", "hh:mm AM/PM", "hh AM/PM"]
                        s+=dateTimeHr[0]+","+dateTimeHr[1]+","+dateTimeHr[2]
                    else: 
                        s+=str(jsonDF[col][row])
                    s+=","
                # for col in range(0, len(csvHeader)-1):                                       # go through each column/report property. len(keys) -1 because im skipping the last key which is "LastInspected" (not needed)
                #     if csvHeader[col] == "DateReported":                                     # Need to change the Microsoft time to mm/dd/yyyy
                #         dateTimeHr = turnToDateTimeHr(str(jsonDF[csvHeader[col]][row]))    # Takes the microsoft date and returns: ["mm/dd/yyyy", "hh:mm AM/PM", "hh AM/PM"]
                #         s+=dateTimeHr[0]+","+dateTimeHr[1]+","+dateTimeHr[2]
                #     else: 
                #         s+=str(jsonDF[csvHeader[col]][row])
                #     if col != len(csvHeader)-2:
                #         s+=',' 
                s = s[:-1]                                                                # Deleting the last comma for the row
                s += "\n"
                outCSV.write(s)                                                         # add new ticket obj to csv file 
                
                
                
                
                
                
                                                       
    # # 5) PUSH TO GITHUB IF WE HAVE A NEW TICKET:
    # # if (isNewTicket == True):
    # #     git_push()
    # #     isNewTicket == False
    print("Run Done " + str(scrapingCount) + "       Reports Scraped: "+str(len(jsonDF)))







# 6) RESCAN FOR TICKETS every x time using sceduler
scheduler = BlockingScheduler()
scheduler.add_job(WebscraperJsonToCSV, 'interval', seconds=1)
scheduler.start()


