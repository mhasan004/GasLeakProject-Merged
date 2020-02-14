#%%     
# Plotting the census tracts for all reports that appeared in a specific month                    
# import contextily as ctx
# import matploylib.pyplot as plt
import geopandas as gp
import os
import platform
import pandas as pd
import numpy as np

ny_shpfile          = "TIGER_2010_County_Shapefiles/NYCounty_2010SHP/tl_2010_36061_tract10.shp"
bronx_shpfile       = "TIGER_2010_County_Shapefiles/BronxCounty_2010SHP/tl_2010_36005_tract10.shp"
queens_shpfile      = "TIGER_2010_County_Shapefiles/QueensCounty_2010SHP/tl_2010_36081_tract10.shp"
brooklyn_shpfile    = "TIGER_2010_County_Shapefiles/BrooklynCounty_2010SHP/tl_2010_36047_tract10.shp"
statenIsland_shpfile= "TIGER_2010_County_Shapefiles/StatenIslanCounty_2010SHP/tl_2010_36085_tract10.shp"
westchester_shpfile = "TIGER_2010_County_Shapefiles/WestchesterCounty_2010SHP/tl_2010_36119_tract10.shp"

nyDGF    =  gp.read_file(ny_shpfile)  
bronxDGF =  gp.read_file(bronx_shpfile)  
queensDGF    =  gp.read_file(queens_shpfile)  
brooklynDGF =  gp.read_file(brooklyn_shpfile)  
statenDGF    =  gp.read_file(statenIsland_shpfile) 
westchesterGDF =  gp.read_file(westchester_shpfile)  

lineW = 0.2
edgeC = "lightgray"
# nyDGF.plot()
# bronxDGF.plot()
# queensDGF.plot( linewidth = 0.5, edgecolor='0.5')
# westchester.plot()

ax = nyDGF.plot(linewidth = lineW, edgecolor=edgeC, color="red")
ax = bronxDGF.plot(ax=ax, linewidth = lineW, edgecolor=edgeC, color="blue")
ax = queensDGF.plot(ax=ax, linewidth = lineW, edgecolor=edgeC, color="green")
ax = westchesterGDF.plot(ax=ax, linewidth = lineW, edgecolor=edgeC, color="purple")
ax = brooklynDGF.plot(ax = ax, alpha=0.5, color = "yellow")
statenDGF.plot(ax = ax, alpha=0.5, color="orange")
#%%