import dash
import dash_core_components as dcc   # has a component for every HTML tag (html.H1() puts the string in a h1 html tag for ex)
import dash_html_components as html  # 
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

corrCSVFile = "DataFiles/FDNY/Seasonal2017_2018_Demographic_Correlation.csv"
corr = pd.read_csv(corrCSVFile)



# 6) PLOT 1:
season_to_do = "ALL_SEASONS"
figALL = px.scatter(corr, x="DemographicVariable", y=season_to_do, color=season_to_do, 
    color_continuous_scale=px.colors.sequential.RdBu,
    width=900, height=1000)
figALL.update_layout(
    title = '(Pearson r Correlation) '+"All Seasons"+' Reports VS Demographic Data',
    yaxis_title = "All Seasons"+' vs Demographic Variables Correlation',
    xaxis_title = "Demographic Variables",
)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']   # external cssCSS file
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)    # initialize app with the external CSS file
app.layout = html.Div(
    children = [                            # children is like an array. html components and a graph.
        html.H1(children='Hello Dash A'),     # same as html.H1('Hello Dash')
        html.Div(children="Dash: A web application framework for Python."),
        
        dcc.Graph(
            id='parallel',     #id of the graph
            figure = figALL
        )

    ]
)

if __name__ == '__main__':
    app.run_server(port=8002,debug=True)












































# import dash
# import dash_core_components as dcc   # has a component for every HTML tag (html.H1() puts the string in a h1 html tag for ex)
# import dash_html_components as html  # 

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']   # external cssCSS file
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)    # initialize app with the external CSS file

# app.layout = html.Div(
#     children = [                            # children is like an array. html components and a graph.
#         html.H1(children='Hello Dash'),     # same as html.H1('Hello Dash')
#         html.Div(children="Dash: A web application framework for Python."),

#         dcc.Graph(
#             id='bar_graph',     #id of the graph
#             figure={
#                 'data': [
#                     # 'x': [what x location is the bars?]
#                     # 'Y': set: [height of bars/points]
#                     {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Bar Graph A'},
#                     {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Bar Graph B'},
#                     {'x': [1, 2, 3], 'y': [5, 2, 3], 'type': 'bar', 'name': 'Bar Graph C'},],
#                 'layout': {
#                     'title': 'Dash Data Visualization',
#                     'xaxis' : dict(
#                         title='x Axis',
#                         titlefont=dict(
#                         family='Courier New, monospace',
#                         size=20,
#                         color='#7f7f7f')),
#                     'yaxis' : dict(
#                         title='y Axis',
#                         titlefont=dict(
#                         family='Helvetica, monospace',
#                         size=20,
#                         color='#7f7f7f' ))
#                 }
#             }
#         ),
#     ]
# )

# if __name__ == '__main__':
#     app.run_server(debug=True)