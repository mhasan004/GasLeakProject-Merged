# PART 3: now making new csv that is based on time
# 1) df = get the csv data.
# 2) dateDF = loop throught the "Date" column and and make a new data frame for entries that has same Date
# 3) hourlyDF = for each dateDF, loop through the "Hour" column and make a new data frame for entries that has same Hour 
# 4) tractDF  = for each hourlyDF, loop through the "Census Tract" column and make a new data frame for entries that has same Hour 
import pandas as pd    

csvInFile  = "GasHistory_ConEdisonTracts.csv"
csvOutFile = "GasHistory_reportsPerCensusTract.csv"

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
df = pd.read_csv(csvInFile) 
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