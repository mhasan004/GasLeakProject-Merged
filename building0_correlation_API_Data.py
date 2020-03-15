# sesonalCSVFile = "DataFiles/FDNY/Season2017_18.csv"
# # sesonalDF  = pd.read_csv(sesonalCSVFile)  
# # print(sesonalDF)

##################################################################  https://pypi.org/project/census-api/ GETTIGN GEOIDS #########
import plotly.express as px
import numpy as np
import pandas as pd
from datascience import *   # needed for census api
import config               # to get the safely stored api key fro the config.py file that git ignores
import census_api           # the api. need to pip install addfips to get it to work

# storing key safely to a file named config.py, which git will ignore
# MY_API_KEY = "067c44396ba567ce59864bc393709f84f9f88e21"
# with open("config.py", "w+") as f:
#     f.write("""api_key = \"{}\"""".format(MY_API_KEY))

# c = census_api.CensusQuery(config.api_key, "acs5", out="pd")                 #class instance
# df2018 = c.query(["NAME"], "NY", year=2018)
# print(list(df2018.columns))
# print(df2018)




###################################################################### https://pypi.org/project/CensusData/ ########3

# import pandas as pd
# import censusdata
# pd.set_option('display.expand_frame_repr', False)
# pd.set_option('display.precision', 2)
# import statsmodels.formula.api as sm


# # statedata = censusdata.download
# # (
# #     'acs', 
# #     2015, 
# #     censusdata.censusgeo([('state', 'New York')]),
# #     ['B19083_001E']#, 'B19013_001E', 'B19083_001E','C17002_001E', 'C17002_002E', 'C17002_003E', 'C17002_004E','B03002_001E', 'B03002_003E', 'B03002_004E', 'B03002_012E',]
# # )
# # # print( getattr(censusdata.download,'name') )


# c = censusdata.download('acs5', 2015, censusdata.censusgeo([('county', 'Kings County')]),
#                                    ['B01001_001E', 'B01001_020E'])
# print(c.describe())


###############################################
import pandas as pd
import censusdata
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)
import statsmodels.formula.api as sm

#Adding all the age columns
ageTableCols = censusdata.search('acs1', 2018, 'concept', 'age')
tableColDict = dict()
tableColCodeArray = []
for i in range(0,len(ageTableCols)):  
    tableColCode = str(ageTableCols[i]).split(", ")[0].strip("(").strip(")").strip("'")
    tableColSection = str(ageTableCols[i]).split(", ")[1].strip("(").strip(")").strip("'")
    tableColVar = str(ageTableCols[i]).split(", ")[2].strip("(").strip(")").strip("'")
    tableColDict.update( {tableColCode: [tableColSection,tableColVar]} )
    tableColCodeArray.append(tableColCode)

a = ['B01001A_001E', 'B01]1A_002E', 'B01001A_003E', 'B01001A_004E', 'B01001A_005E']
ageDF = censusdata.download('acs5', 2018,
                             censusdata.censusgeo([('state', '36'), ('county', '047'), ('block group', '*')]),
                              tableColCodeArray[300:600]
                            )
# ageDF['population'] = ageDF.B01003_001E #/ ageDF.B23025_003E * 100
# # ageDF['percent_nohs'] = (ageDF.B01003_001E)

# ageDF = ageDF[['population']]#, 'percent_nohs']]
# nunique = ageDF.apply(pd.Series.nunique)
# cols_to_drop = nunique[nunique == 1].index
# ageDF.drop(cols_to_drop, axis=1)

# ageDF = ageDF.mask(ageDF.eq('None')).dropna()                                     # drop all cols that has None
print(ageDF)
