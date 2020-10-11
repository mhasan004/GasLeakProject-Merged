# GasLeakCombined
### Project: examine socioeconomic conditions that affect reporting of gas leaks 

## A) ConEdison Gas Leak Report Scraper program - `scraper_ConEdison.py` 
 * New version here: https://github.com/mhasan004/GasLeakProject/blob/master/Getting_GasLeak_Data/scraper_ConEdison.py
 1) Gets the latest gas leak reports from Kings, Queens, Manhattan, Bronx, and Westchestrer counties using the Con Edison API
 2) Retrieves the 2010 census tract data for each report using the Census Bureau API 
 3) Updates all files in `GasLeakCombined/DataFiles/ConEdison`
     * `GasHistory_2010_ConEdisonTracts.csv` - record of all the gas leak report data with its respective census location data. 
     * `GasHistory_2010_ReportFrequency_Hourly.csv`  - lists how many gas leaks reports there were per hour, per census tract, per day 
     * `GasHistory_2010_ReportFrequency_Monthly.csv` - lists how many gas leaks reports there were per month, per census tract

## B) Correlation Comparison Program - Easily Check Relevancy of a Dataset
* Dashboard to check the relevancy of a dataset before use. Compares the correlation of all fields of a dataset against our gas leak report data for any season. 
* Can use this program to easy find which field of the dataset, if any, of the dataset can be usable. Fields with high correlation are usable. 

<img src=PicGifs/dashboard_demo_faster.gif width="800">

* This program easily checks the correlation between all fields of a dataset with our gas leak dataset. Field with little correlation aren't researched further. 
* In this example, we are finding correlations between our gas leak dataset and all fields of the demographic and crime datasets
* We can test with all seasons of our gas leak dataset, or pick individual seasons to test again
* **Pearson R Correlation Graph (Left Graph):** The graph on the left shows the Pearson R Correlation between our gas leak dataset (datasetA) and each fields of another dataset (datasetB). The higher the dot, the higher the correlation. Hovering over a dot shows the field of the datasetB that is being shows and the correlation value.
  * Example: we can see how correlated our gas leak data for a season is compared to all field of a population dataset (ex: our data vs total population, our data vs population of males, our data vs population of females, etc)
* **Selected Scatter Graph (Middle Graph):** When a correlation dot is selected, the graph in the middle will generate a scatter plot of the number of reports per census tract vs the field of datasetB. Each dot represents a census tract. Hovering over the dot shows the census tract number and location, the gas report number, and the datasetB field for that census tract.
* **Census Tract Parallel Coordinate Graph (Third Graph):** The third graph of the first row shows the gas leak data for all seasons and the total crime report for a selected census tract. 
* **Dropdown:** Can test datasetB with different seasons of our gas leak report data
 
### To run:
1) Make Enviornment:  `virtualenv gasEnv`, `source gasEnv/bin/activate`
    
2) Install Dependencies: 
    `pip3 install -r requirements.txt`

3) Run dashboard: 
    `python3 Dashboard.py`

## C) Files:
* Data files can be found in `/Datafiles`
* `Map_2010_ConEdison_MonthlyPlots.ipynb` - Shows the frequency map of ConEdison gas leak reports from December - February
<img src=PicGifs/MapPic_Conedison_Jan2020.PNG width="500">

