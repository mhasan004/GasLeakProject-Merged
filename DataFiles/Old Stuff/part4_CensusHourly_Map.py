
#%%                           
import geopandas as gp
import os
import platform
import pandas as pd

sf = "NY_SP/tl_2019_36_tract.shp"
csvFile = "GasHistory_ReportFrequency_Hourly.csv"

dataf = pd.read_csv(csvFile)                   # Read the csv file and make a data frame
shapef = gp.read_file(sf)                      # Read the shape file and make a data frame
# for row in range(0, len(shapef)):              # not needed ADJUSTING SOME VALUES: shapef data frame has "Census Track <num>" vals so will chnage it to just numbers
#     shapeTract = float(shapef.iloc[row]["NAMELSAD"].split(" ")[2])  # The Census Tract Data is in "Census Tract <number>"
#     shapef.at[row,"NAMELSAD"] = shapeTract


newShapef = shapef.copy()
newShapef.drop(newShapef.index, inplace=True)                                       # copied shapef df and emptied it to get empty df. idk why but making empty df with the cols of shapdf dont work
# newShapef = pd.DataFrame(columns = list(shapef.columns))

for row in range(0, len(dataf)):
    onlyConEdTracts = shapef[shapef.NAME == str(int(dataf.loc[row]["CensusTract"]))] # Prints all GEOID's that has this Census Tract
    newShapef = newShapef.append(onlyConEdTracts)
print(newShapef)
newShapef.plot(cmap='rainbow')
shapef.plot()






# %%
