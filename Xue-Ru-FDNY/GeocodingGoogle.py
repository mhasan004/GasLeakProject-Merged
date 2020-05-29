# finding latitude and longitude using google api, make sure to use Locationlookup.py before this so we dont waste api query 
# on the data we already have processed. 


import pandas as pd
import googlemaps

df = pd.read_csv("unprocess.csv")

gmaps_key = googlemaps.Client(key = "")

for i in range(10,len(df)):
    geocode_res = gmaps_key.geocode(df.iat[i,1])
    try:
        lat = geocode_res[0]["geometry"]["location"]["lat"]
        lon = geocode_res[0]["geometry"]["location"]["lng"]
        df.at[i,"lat"] = lat
        df.at[i,"lon"] = lon
    except:
        lat = None
        lon = None

df.to_csv('unprocess.csv', encoding='utf-8',index=False)
