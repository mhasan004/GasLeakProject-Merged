# 4) 
import dash
import dash_core_components as dcc   # has a component for every HTML tag (html.H1() puts the string in a h1 html tag for ex)
import dash_html_components as html  # 
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import dash_html_components as html
from dash.dependencies import Input, Output
import json

from textwrap import dedent as d

corrCSVFile = "NYPD_Complaint_Data_Historic_WITH_CENSUS_DATA_Filtered_Corr.csv"
mergedFile  = "NYPD_Complaint_Data_Historic_WITH_CENSUS_DATA_Filtered_Merged.csv"


corr = pd.read_csv(corrCSVFile)
seasonalCrimeDF = pd.read_csv(mergedFile)
widthPlot  = 900
heightPlot = 900
chosenSeason = "ALL_SEASONS"

# 1) PLOT 1: corr plot
figALL = go.Figure(
    data = go.Scatter(
        x = corr['Crimes'],
        y = corr[chosenSeason],
        mode='markers',
    )
)
figALL.update_layout(
    title = '(Pearson r Correlation) Gas Reports of All Season VS Crimes',
    yaxis_title = "Correlation between Gas Reports per Census Tract ("+ chosenSeason +") vs Crime Variables",
    xaxis_title = "Crime Variables",
    width=widthPlot,
    height=heightPlot,
    margin=go.layout.Margin(
        l=50,
        r=50,
        b=500,
        t=90,
        pad=0
    )
)




# 2) A scatter plot function for any demograpic variable vs ALL_SEASON col
# nonDemoCols = ["Geoid","Spring","Summer","Autumn","Winter","ALL_SEASONS","Id","Geography"]
# cols = list(corr.columns)
# demoCols = []
# for col in cols:
#     if col not in nonDemoCols:
#         demoCols.append(col)

def returnDemoScatterFig(chosenCol):     
    fig = px.scatter(
        seasonalCrimeDF, 
        x = chosenSeason, 
        y = chosenCol, 
        width=1000, 
        height=800,
        # color="red"#chosenCol, 
        hover_data=['Geoid', chosenSeason, chosenCol ],     
        opacity=0.2
    )
    fig.update_layout(
        title = "Number of Reports Per Census Tract (All Seasons) vs "+chosenCol,
        xaxis_title = "Number of Reports Per Census Tract (All Seasons)",
        yaxis_title = chosenCol,
        # length = 200,
        # width  = 300,
    )
    # fig = go.Figure(
    #     data = go.Scatter(
    #         y = seasonalCrimeDF[chosenCol],
    #         x = seasonalCrimeDF[chosenSeason],
    #         mode='markers',
    #     )
    # )
    # fig.update_layout(
    #     title = '(Pearson r Correlation) Gas Reports of All Season VS'+ chosenCol,
    #     yaxis_title = "Correlation between Gas Reports per Census Tract ("+ chosenSeason +") vs Crime Variables",
    #     xaxis_title = "Crime Variables",
    #     width=widthPlot,
    #     height=heightPlot,
    #     margin=go.layout.Margin(
    #         l=50,
    #         r=50,
    #         b=500,
    #         t=90,
    #         pad=0
    #     )
    # )

    return fig

#__________________________________________________________________________________________________________________#

























#__________________________________________________________________________________________________________________#

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']           # external cssCSS file for Bootstraps
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)            # initialize app with the external CSS file
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
colors = {
    'text': 'white',
    'background': 'lightblue'
}
s = dict()
app.layout = html.Div(
    html.Div(                                                                   # 1. GLOBAL DIV STARTS
        style={'backgroundColor': colors['background']}, 

        children = [                                                            # 2. GLOBAL CHILDREN DIV START  
            html.H1(children='GAS REPORT DASHBOARD'),                                   # same as html.H1('Hello Dash')
            html.Div(children="somethign somethign something"),
            html.Div([ 
                dcc.Dropdown(
                    id='dropdown',
                    options=[
                        {'label': 'ALL SEASON', 'value': 'ALL_SEASONS'},
                        {'label': 'Summer', 'value': 'Summer'},
                        {'label': 'Spring', 'value': 'Spring'}
                    ],
                    # value='NYC'
                ),
            ], className = "row"),
            ############## ROW 1
            html.Div([                                                          # 3. ROW 1 DIV START
                html.Div([                                                      # 4. ROW 1 - half START
                    dcc.Graph(
                        id='ALL_SEASONS',                                                  # id of the graph
                        figure = figALL
                    )
                ], className="six columns"),                                    # 4. ROW 1 - half END
                
                html.Div([                                                      # 4. ROW 1 - half START
                    dcc.Graph(
                        id='DemoScatter',                                                  # id of the graph
                        figure = figALL#returnDemoScatterFig()
                    )
                ], className="six columns"),                                    # 4. ROW 1 - half END

            ], className = "row"),                                              # 3. ROW 1 DIV END
            
            html.Div(className='row', children=[
                html.Div([
                dcc.Markdown(d("""
                    **Hover Data**

                    Mouse over values in the graph.
                """)),
                html.Pre(id='hover-data', style=styles['pre'])
            ], className='row'),
            ])

        ############ END
        ],                                                                      # 1. GLOBAL CHILDREN DIV END
        className='ten columns offset-by-one'
    )                                                                           # 2. GLOBAL DIV END
)


#
@app.callback(
    dash.dependencies.Output('DemoScatter', 'figure'),
    [dash.dependencies.Input('ALL_SEASONS', 'hoverData')])    #getting the all seasons
    # [dash.dependencies.Input('hover-data', 'children')])    #getting the all seasons

def display_hover_data(hoverData):                              # hoverData is a json data
    json_string = json.dumps(hoverData)
    json_split = json_string.split(", ")                        # index 3 is the x data
    if len(json_split)>1:
        json_demoVar = json_split[3].replace('"', '').replace("x: ", '')
        return returnDemoScatterFig(json_demoVar)
    return figALL

# # dropdown
# @app.callback(
#     dash.dependencies.Output('DemoScatter', 'figure'),
#     [dash.dependencies.Input('dropdown', 'value')])    #getting the all seasons
# def display_hover_data(hoverData):                              # hoverData is a json data
#     json_string = json.dumps(hoverData)
#     json_split = json_string.split(", ")                        # index 3 is the x data
#     if len(json_split)>1:
#         json_demoVar = json_split[3].replace('"', '').replace("x: ", '')
#         return returnDemoScatterFig(json_demoVar)
#     return figALL

if __name__ == '__main__':
    app.run_server(port=8007,debug=True)











































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