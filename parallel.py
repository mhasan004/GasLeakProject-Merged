import plotly.express as px
import numpy as np
import pandas as pd  
import plotly.graph_objects as go


demoCsvFile = "DataFiles/Crime and Demographics/filtered_CensusTract_Demographic_Data_for_ConEd.csv"
demoDF  = pd.read_csv(demoCsvFile)  
# print(demoDF)
# s = ["HC01_EST_VC01",	"HC02_EST_VC01",	"HC03_EST_VC01",	"HC01_EST_VC03"]

# fig = px.parallel_coordinates(
#     demoDF, 
#     # color="GEO.display-label",
#     dimensions=s,
#     # color_continuous_scale=px.colors.diverging.Tealrose,
#     color_continuous_midpoint=2
# )
# fig.show()



fig = go.Figure(data=
    go.Parcoords(
        # line = dict(color = demoDF['GEO.id2']), colorscale = [[0,'purple'],[0.5,'lightseagreen'],[1,'gold']]),
        dimensions = list([
            dict(
                # range = [0,8],
                # constraintrange = [4,8],
                label = 'Sepal Length', values = demoDF['HC01_EST_VC01']),
            dict(range = [0,8],
                label = 'Sepal Width', values = demoDF['HC02_EST_VC01']),
            dict(range = [0,8],
                label = 'Petal Length', values = demoDF['HC03_EST_VC01'])
        
        ])
    )
)

# fig.update_layout(
#     plot_bgcolor = 'white',
#     paper_bgcolor = 'white'
# )

fig.show()