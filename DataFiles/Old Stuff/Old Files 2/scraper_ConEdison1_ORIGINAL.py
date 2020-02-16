# Mahmudul Hasan. Script to scrape JSON Gas Leak Data points from ConEdison everyday and put them into a csv file for further use
# In the ConEdison Gas Leak Report Map, each dot in the map represents a gas leak report. Each report has these seven keys: TicketNumber, Latitude, Longitude, Zipcode, Classification Type, Date Reported, Last Inspected.
# a) We need to constantly add new repots to out list so what tickets do we currently have? read the ticket col of the "csvFile" and add the tickets to "ticketSet"
# b) Scrape the JSON html response and add it to a python dictionary: "jsonDict" = contents of json response
# c) See if there is a new report: Loop through each JSON obbject in "jsonDict" and compare it to the reports are already exists in "ticketSet"
# d) If there is a new report, add append the keys of that report into "csvFile", "ticketListFile" and push the latest changes to github

import json
import csv
import pandas as pd                 # to trun the json string to a python dictionary and to read fromcsv files and pu the data into python dictionary
import datetime,re                  # to turn Microsoft JSON date /Date()/ to normal date
import requests                     # Getting html data
from bs4 import BeautifulSoup       # Parse the HTML data
from apscheduler.schedulers.blocking import BlockingScheduler # Sceduler. Will run a function every x seconds/minutes/hours
from git import Repo                # (GitPython) To push changes to gh


# SETTING UP GLOBAL VARIABLES: need to change the first eight variables below
jsonFile = "SOME_JSON_FILE_WITH_SAME_KEYS.json"          # Normally the programm will be scrape JSOn data from a url but sometimes it might need to extract JSOn data from a file. See step 2)
url = 'https://apps.coned.com/gasleakmapweb/GasLeakMapWeb.aspx?ajax=true&' # Url to scrape JSOn data from
csvFile = "GasHistory_ConEdison.csv"                                       # add new tickets to the end of the csv file
ticketListFile = "conEd_TicketList.txt"                                 # add to end (just for me to see what i got)
keys= [                                                                 # The JSON dot keys( better to use key iteration, instead i went through the columns of the dictionary with this)
    "TicketNumber",
    "Latitude",
    "Longitude",
    "Zip",
    "ClassificationType",
    "DateReported",
    "LastInspected"
]
PATH_OF_GIT_REPO = r'/home/pi/repositories/gh/GasLeakProject'           # the path to the .git file (.git location on my raspberry pi)
#PATH_OF_GIT_REPO = r'/home/hasan/repositories/gh/GasLeakProject'       # the path to the .git file (.git location on my Laptop)
COMMIT_MESSAGE = 'Automated Push - New Ticket Update'                   # the commmit message when it is pushed
ticketSet = set()                                                       # need to add what i got in the csv atm
jsonDict  = []                                                          # json file to dict: #jsonDict["TicketNumber/Long/lat/etc"][int index of the dot]) 
scrapingCount = 0                                                       # Just counting how many times i have scraped the website while this was running

# GIT PUSH FUNCTION: Setting up function to automatically push changes to github when there is a new ticket so that I can have access to the latest chnages
def git_push():
    repo = Repo(PATH_OF_GIT_REPO)
    try:
        repo.remotes.origin.pull()                                      # try pulling new changes from the github repo (if there are any) so i can push changes
    except:
        print("Couldnt pull from repo")
    repo.git.add(update=True)
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    try:
        origin.push()                           # try pushing the chnages to github
        print("******** PUSHED TO GITHUB for Run " + str(scrapingCount)+"********")
    except:
        print('Some error occured while pushing the code')  
  

# Function to turn Microsoft JSON date to mm/dd/yy and time:
def turnToDatetime(microsoftDate):         
    TimestampUtc = str(microsoftDate)
    TimestampUtc = re.split('\(|\)', TimestampUtc)[1][:10]
    date = datetime.datetime.fromtimestamp(int(TimestampUtc))
    return str(date.strftime('%m/%d/20%y %I:%M %p'))                    # mm/dd/yyyy time am/pm

# The sceduler will run this main funtion ever x seconds/minutes/hours
def WebscraperJsonToCSV():  
    # Set up the web scraping iteration counter for debugging purposes
    global scrapingCount                                                # Indicate that im using the global value
    scrapingCount = scrapingCount + 1 
    isNewTicket = False

    # 1) If the csv is empty, print the header
    with open(csvFile, 'r') as csvfile:
        csv_dict = [row for row in csv.DictReader(csvfile)]
        if len(csv_dict) == 0:
            csvHeader = ["TicketNumber","Longitude","Latitude","Zipcode","Classification","DateReported"]
            with open(csvFile, 'w', newline='') as outf:
                writer = csv.writer(outf)
                writer.writerow(csvHeader)
    
    # 2) GET JSON DATA: from a JSON file and add to the JSON Dictionary: 
    # jsonDict = pd.read_json(jsonFile, orient='records')               # ***jsonDict[keys[i]/colStr(dot keys)][j/rowsnumber(dots)]
    
    # 2) GET JSON DATA: Webscrape the html response which is usually just the JSON data from the url and add to the JSON Dictionary: 
    res = requests.get(url)
    html_data = res.content                                             # Getting the HTML JSOn data 
    soup = BeautifulSoup(html_data, 'html.parser')                      # parsing the html data with html parcer (can do stuuf like soup.title to get the title, soup.div, soup.li etc)
    text = soup.find_all(text=True)                                     # Getting all the text thats in the soup

    jsonStr = ''                                                        # turning text to string from so i can use pandas to turn it to dictionary
    try:
        for t in text:
            jsonStr += '{} '.format(t)
        jsonDict = pd.read_json(jsonStr, orient='records')              # Turning the json string to a dictionary
    except:
        print("Couldnt get the json data so will re-run function. This is Run "+ str(scrapingCount))
        WebscraperJsonToCSV()
        return
    
    # 3) CHECK WHAT TICKETS WE ALREADY GOT FROM THE .CSV FILE AND ADD NEW TICKETS TO ticketSet and .txt file: Read the csv file and add "TicketNumbers" to the "ticketSet" and print ticketNumber to ticketList.txt" for storage: 
    csvDict = pd.read_csv(csvFile)                                      # ***csvDict[colStr][rowNumber]
    outTXT = open(ticketListFile,"w+")                                  # Settign up to write to txt file
    for row in range(0,len(csvDict)):
        ticketSet.add(str(csvDict["TicketNumber"][row]))    
        outTXT.write(str(csvDict["TicketNumber"][row])+"\n")                                                       # there is an error so cant continue so end this

    # 4) CHECK IF NEW TICKET: See if the tickets in "jsonDict" are in "ticketDict". If we have have it, add to "ticketDic", and .txt and .csv file for stoage. If we have it, skip this row since we have this info already. 
    for row in range(0, len(jsonDict)):
        if jsonDict["TicketNumber"][row] not in ticketSet:              # If we DONT have this ticket add it
            isNewTicket = True                                          # This is a new ticket so push the new files
            print(str(jsonDict["TicketNumber"][row])+ " not in set so adding it")
            ticketSet.add(jsonDict["TicketNumber"][row])
            outTXT.write(jsonDict["TicketNumber"][row]+"\n")            # add new ticket to txt file  
            with open(csvFile,'a') as outCSV:                           # Write the new Ticket object to csv file
                s=""
                for col in range(0, len(keys)-1):                       # go through each column/dot property
                    if keys[col] == "DateReported":                     # Need to change the Microsoft time to mm/dd/yyyy
                        s+=turnToDatetime(str(jsonDict[keys[col]][row]))# key iteration would be a better implentation :(
                    else: 
                        s+=str(jsonDict[keys[col]][row])
                    if col != len(keys)-2:                              # trims off the "/n" from the line terminator
                        s+=',' 
                s+="\n"
                outCSV.write(s)                                         # add new ticket obj to csv file  
    # 5) Push to Github if we have a new ticket
    if (isNewTicket == True):
        git_push()
        isNewTicket == False
    print("Run Done " + str(scrapingCount) + "       Reports Scraped: "+str(len(jsonDict)))

# 6) RESCAN FOR TICKETS every x time using sceduler
scheduler = BlockingScheduler()
scheduler.add_job(WebscraperJsonToCSV, 'interval', seconds=1)
scheduler.start()















#431 dec 25 2 18apm
#421 tickets atm 12/25/19 1:16am




