# make sure we dont reprocess the data we already have, so this looks up information that we already have


import os
import pandas as pd

data2018 = pd.read_csv('processed.csv')
data2017 = pd.read_csv('FDNY_2017.csv')

#data2017['lat'] = 0.0
#data2017['lon'] = 0.0
#data2017['CountyName'] = '0'
#data2017['Geoid2010'] = 0

for row in range(0,len(data2017)):
    ind = data2018.loc[data2018['alarm_box_location'] == data2017['alarm_box_location'][row]].index
    if len(ind) is not 0:
        data2017.at[row,'lat'] = data2018['lat'][ind[0]]
        data2017.at[row,'lon'] = data2018['lon'][ind[0]]
        data2017.at[row,'CountyName'] = data2018['CountyName'][ind[0]]
        data2017.at[row,'Geoid2010'] = data2018['Geoid2010'][ind[0]]

data2017.to_csv('FDNY_2017.csv', encoding='utf-8',index=False)
