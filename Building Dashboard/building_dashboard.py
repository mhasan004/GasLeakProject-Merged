# 3) from bbuilding_Demographic_Scatter.ipynb
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

widthPlot  = 900
heightPlot = 900
# 1) PLOT 1: ALL SEASONS
season_to_do = "ALL_SEASONS"
figALL = px.scatter(corr, x="DemographicVariable", y=season_to_do, color=season_to_do, 
    color_continuous_scale=px.colors.sequential.RdBu,
    width=widthPlot, height=heightPlot,
    hover_data=['DemographicVariable', "ALL_SEASONS"]
)
figALL.update_layout(
    title = '(Pearson r Correlation) '+"All Seasons"+' Reports VS Demographic Data',
    yaxis_title = "All Seasons"+' vs Demographic Variables Correlation',
    xaxis_title = "Demographic Variables",
)

# 2) 4 PLOTS: 4 SEASON'S figs IN A DICT 
corrDict = dict()
seasons = ["Spring","Summer","Autumn","Winter"]
for season in seasons:
    fig = px.scatter(corr, x="DemographicVariable", y=season, color=season, 
                    color_continuous_scale=px.colors.sequential.RdBu,
                    width=widthPlot, height=heightPlot)
    fig.update_layout(
        title = '(Pearson r Correlation) '+season+' Reports VS Demographic Data',
        yaxis_title = season+' vs Demographic Variables Correlation',
        xaxis_title = "Demographic Variables",
    )
    corrDict[season] = fig


# #######################################################

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']           # external cssCSS file for Bootstraps
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)            # initialize app with the external CSS file

colors = {
    'text': 'white',
    'background': 'lightblue'
}

app.layout = html.Div(
    html.Div(                                                                   # 1. GLOBAL DIV STARTS
        style={'backgroundColor': colors['background']}, 

        children = [                                                            # 2. GLOBAL CHILDREN DIV START  
            html.H1(children='GAS REPORT DASHBOARD'),                                   # same as html.H1('Hello Dash')
            html.Div(children="somethign somethign something"),
            
            ############## ROW 1
            html.Div([                                                          # 3. ROW 1 DIV START
                html.Div([                                                      # 4. ROW 1 - half START
                    dcc.Graph(
                        id='parallel',                                                  # id of the graph
                        figure = figALL
                    )
                ], className="six columns"),                                    # 4. ROW 1 - half END

                html.Div([                                                      # 4. ROW 1 - half START
                    dcc.Graph(
                        id=seasons[0],                                                 # id of the graph
                        figure = corrDict[seasons[0]]
                    )
                ], className="six columns"),                                    # 4. ROW 1 - half END            
            ], className = "row"),                                              # 3. ROW 1 DIV END

            ############## ROW 2
            html.Div([                                                          # 3. ROW 1 DIV START
                html.Div([                                                      # 4. ROW 1 - half START
                    dcc.Graph(
                        id=seasons[1],                                                  # id of the graph
                        figure = corrDict[seasons[1]]
                    )
                ], className="six columns"),                                    # 4. ROW 1 - half END

                html.Div([                                                      # 4. ROW 1 - half START
                    dcc.Graph(
                        id=seasons[2],                                                  # id of the graph
                        figure = corrDict[seasons[2]]
                    )
                ], className="six columns"),                                    # 4. ROW 1 - half END            
            ], className = "row"),                                              # 3. ROW 1 DIV END


        ############ END
        ],                                                                      # 1. GLOBAL CHILDREN DIV END
        className='ten columns offset-by-one'
    )                                                                           # 2. GLOBAL DIV END
)

if __name__ == '__main__':
    app.run_server(port=8003,debug=True)












































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