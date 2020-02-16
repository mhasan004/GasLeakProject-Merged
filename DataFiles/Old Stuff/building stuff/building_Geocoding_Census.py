# Census API doc: https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf
# census api url format: https://geocoding.geo.census.gov/geocoder/geographies/coordinatesx=longitude&y=latitude&benchmark=&vintage=&format=json
# census api url example: https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x=-78.8543293&y=41.6567756&benchmark=Public_AR_Current&vintage=Current_Current&format=json
    # json result of the top search given this random lat long coordinate is results: input and geographies. geographics has: 2010 census blocks, states, countries, census tracts

from urllib.request import urlopen
import json

# 1) Using the census api, getting census tract for each 
longitude = -73.864082
latitude = 40.680828
url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={0}&y={1}&benchmark=Public_AR_Current&vintage=Current_Current&format=json".format(longitude,latitude)
response = urlopen(url)
dataJSON = json.loads(response.read())
data = dataJSON["result"]

censusTract = str(data["geographies"]["Census Tracts"][0]["BASENAME"])      
countyName  = str(data["geographies"]["Counties"][0]["NAME"])     
censusBlock = str(data["geographies"]["2010 Census Blocks"][0]["BLOCK"])     
print(censusTract)
print(censusBlock)
print(countyName)