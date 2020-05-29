import plotly.express as px
import numpy as np
import pandas as pd  
import plotly.graph_objects as go


demoCsvFile = "DataFiles/Crime and Demographics/filtered_CensusTract_Demographic_Data_for_ConEd.csv"
demoDF  = pd.read_csv(demoCsvFile)  

x = 25199
y = 10870
z = 14329
fig = go.Figure(data=
    go.Parcoords(
        line = dict(
            color = demoDF['Id'],
            #    colorscale = [[0,'purple'],[0.5,'lightseagreen'],[1,'gold']]
            ),
        dimensions = list([
            dict(
                range = [0,15000],
                constraintrange = [0, x],
                label = 'Total Population', values = demoDF['Total; Estimate; Total population']),
            dict(range = [0,y],
                label = 'Total Male Population', values = demoDF['Male; Estimate; Total population']),
            dict(range = [0,z],
                label = 'Total Female Population', values = demoDF['Female; Estimate; Total population'])
        
        ])
    )
)




# fig.update_layout(
#     plot_bgcolor = 'white',
#     paper_bgcolor = 'white'
# )

fig.show()