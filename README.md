# GasLeakCombined

## ConEdison Gas Leak Report Scraper program - `scraper_ConEdison.py` 
 * new version here: https://github.com/mhasan004/GasLeakProject/blob/master/Getting_GasLeak_Data/scraper_ConEdison.py
 * Get the latest gas leak reports using the ConEdison API and then retrieves the census location data using the Census Beru API and then updates all files in `GasLeakCombined/DataFiles/ConEdison`
 * `GasHistory_2010_ConEdisonTracts.csv` - record of all the gas leak report data with its respective census location data. 
 * `GasHistory_2010_ReportFrequency_Hourly.csv`  - lists how many gas leaks reports there were per hour, per census tract, per day 
 * `GasHistory_2010_ReportFrequency_Monthly.csv` - lists how many gas leaks reports there were per month, per census tract



## Correlation Comparison Program - Easily Check Relevancy of a Dataset
Dashboard to check relevancy of a dataset before use. Compares the correlation of all fields of a dataset against our gas leak report data for all seasons, Summer only, Autumn only, Winter only, Fall only. Can use this program to easy find which field, if any, of the dataset can be usable. Fields with high correlation are usable. 

<img src=PicGifs/dashboard_demo_faster.gif width="800">

### To run:
1) Make Enviornment: 

    `virtualenv gasEnv`

    `source gasEnv/bin/activate`

2) Install Dependencies: 
    
    `pip3 install -r requirements.txt`

3) Run dashboard: 
    
    `python3 Dashboard.py`


## Files:
* Data files can be found in `/Datafiles`
* `Map_2010_ConEdison_MonthlyPlots.ipynb` - Shows the frequency map of ConEdison gas leak reports from December - February
<img src=PicGifs/MapPic_Conedison_Jan2020.PNG width="500">

