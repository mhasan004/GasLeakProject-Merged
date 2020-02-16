# Geocoder didnt work for me

# google api tutorial: https://chrisalbon.com/python/data_wrangling/geocoding_and_reverse_geocoding/
# census api url: https://geocoding.geo.census.gov/geocoder/geographies/coordinatesx=longitude&y=latitude&benchmark=&vintage=&format=json
# census api url: https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x=-75.8543293&y=40.6567756&benchmark=Public_AR_ACS2019&vintage=Current_ACS2019&format=json
    # json result of the top search given this random lat long coordinate is results: input and geographies. geographics has: 2010 census blocks, states, countries, census tracts

from pygeocoder import Geocoder # geo functionality
import pandas as pd             # dataframe structure
import numpy  as np             # for the missing value (np.nan) functionality

# 1) Simulating some geo data using a dictionary that has five long and lat strings:
data = {
    'Site 1': '31.336968, -109.560959',
    'Site 2': '31.347745, -108.229963',
    'Site 3': '32.277621, -107.734724',
    'Site 4': '31.655494, -106.420484',
    'Site 5': '30.295053, -104.014528'
}

# 2) Convert the dictionary into a pandas dataframe (row => key and the string of lat and long value)
df = pd.DataFrame.from_dict(data, orient='index')   # will print a table with the keys and the vals. df[0][0 to whatever to access the row values]

# 3) converting the long and lat string into a lat and lon array so can access them
lat = []
lon = []
for row in df[0]:
    try:
        # Split the value by commas and split the left side to lat, and right side to lon
        lat.append(float(row.split(',')[0]))   
        lon.append(float(row.split(',')[1]))
    except:
        # If there is an error, append a missing value to lat or lon
        lat.append(np.NaN)              
        lon.append(np.NaN)

# Create two new columns from lat and lon and add them into df
df['latitude'] = lat
df['longitude'] = lon

# 4) REVERSE GEOCODING: finding location from long and lat data
results = Geocoder("AIzaSyC9sswVlnncMor_88S7i2K_6NiUX2-5dvU").reverse_geocode(df['latitude'][0], df['longitude'][0])
# results = Geocoder().reverse_geocode(df['latitude'][0], df['longitude'][0])
