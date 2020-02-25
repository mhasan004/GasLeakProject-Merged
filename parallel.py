import plotly.express as px
import numpy as np
import pandas as pd
import textwrap  

df = px.data.iris()
print(df)
fig = px.parallel_coordinates(
    df, 
    color="species_id",
    dimensions=['sepal_width', 'sepal_length', 'petal_width','petal_length'],
    color_continuous_scale=px.colors.diverging.Tealrose,
    color_continuous_midpoint=2
)
fig.show()