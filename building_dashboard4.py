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

csvFile_demoMerged = "DataFiles/FDNY/Seasonal2017_2018_Demographics.csv"
merged_demoDF = pd.read_csv(csvFile_demoMerged)
csvFile_demoCorr = "DataFiles/FDNY/Seasonal2017_2018_Demographic_Correlation.csv"
corr_demoDF = pd.read_csv(csvFile_demoCorr)

csvFile_crimeMerged  = "DataFiles/Crime and Demographics/Crime/ACS_10_5YR_S0101_With_Census_Data_FILTERED_Merged.csv"
merged_crimeDF = pd.read_csv(csvFile_crimeMerged)
csvFile_crimeCorr     = "DataFiles/Crime and Demographics/Crime/ACS_10_5YR_S0101_With_Census_Data_FILTERED_Corr.csv"
corr_crimeDF = pd.read_csv(csvFile_crimeCorr)

demoHeaders = list(corr_demoDF.columns) + list(merged_demoDF.columns) 
crimeHeaders = list(corr_crimeDF.columns) + list(merged_crimeDF.columns) 

# widthPlot_corr  = 900
# heightPlot_corr = 900

widthPlot  = 800
heightPlot = 900

heightPlot2 = 1200    # for the crime data to have space at bottom to show labels


season_to_show = "ALL_SEASONS"

######################################################################################################### DEMOGRAPHIC DATA
# A1) PLOT 1: Demographic Pearson R Correlation Scatter Plot
fig_demoCorr = px.scatter(
    corr_demoDF, x="DemographicVariable", y=season_to_show, 
    color=season_to_show, 
    color_continuous_scale=px.colors.sequential.RdBu,
    width=widthPlot, height=heightPlot,
    hover_data=['DemographicVariable', season_to_show])
fig_demoCorr.update_layout(
    title = '(Pearson r Correlation) '+"All Seasons"+' Reports VS Demographic Data',
    yaxis_title = "All Seasons"+' vs Demographic Variables Correlation',
    xaxis_title = "Demographic Variables",
)

# A2) PLOT 2: A scatter plot function for any Demograpic variable vs NYFD gas reports of a choosen season
def returnDemoScatterFig(chosenCol):     
    fig = px.scatter(
        merged_demoDF, x=season_to_show, y=chosenCol, 
        color=chosenCol,
        hover_data=['Geoid', season_to_show, "Geography" ],     
        opacity=0.2,     
        width=widthPlot, height=600)
    fig.update_layout(
        title = "Number of Reports Per Census Tract (All Seasons) vs "+chosenCol,
        xaxis_title = "Number of Gas Reports Per Census Tract ("+season_to_show+")",
        yaxis_title = chosenCol,
    )
    return fig

# ################################################################################################################################ CRIME DATA
# B1) PLOT 3:  Crime Pearson R Correlation Scatter Plot
fig_crimeCorr = px.scatter(
    corr_crimeDF, x="Crimes", y=season_to_show, 
    color=season_to_show, 
    width=widthPlot, height=heightPlot2)
fig_crimeCorr.update_layout(
    title = '(Pearson r Correlation) Gas Reports of '+season_to_show+' VS Crimes',
    yaxis_title = "Correlation between Gas Reports per Census Tract ("+season_to_show+") vs Crime Variables",
    xaxis_title = "Crime Variables",
)

# B2) PLOT 4: A scatter plot function for any Crime variable vs NYFD gas reports of a choosen season
def returnCrimeScatterFig(chosenCol):     
    fig = px.scatter(
        merged_crimeDF, x="ALL_SEASONS", y=chosenCol, 
        color=chosenCol, 
        hover_data=['Geoid', "ALL_SEASONS", "TotalCrime" ],
        opacity=0.2,
        width=widthPlot, height=700
        )
    fig.update_layout(
        title = "Number of Reports Per Census Tract ("+season_to_show+") vs "+chosenCol,
        xaxis_title = "Number of as Reports Per Census Tract ("+season_to_show+")",
        yaxis_title = chosenCol,
    )
    return fig

# ################################################################################################################################ 


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

app.layout = html.Div(
    html.Div(                                                      
        style={'backgroundColor': colors['background']}, 

        children = 
        [                                                             
            html.H1(children='GAS REPORT DASHBOARD'),                
            html.Div(children="somethign somethign something"),
            
            #_______________________________________________________________________________________________ ROW 1: drop down
            html.Div(
                style={'backgroundColor': colors['text']},                         # background fo graph to be white
                children = [ 
                    dcc.Dropdown(
                        id='dropdown',
                        options=[
                            {'label': 'ALL SEASON', 'value': 'All Seasons'},
                            {'label': 'Summer', 'value': 'Summer'},
                            {'label': 'Spring', 'value': 'Spring'},
                            {'label': 'Winter', 'value': 'Winter'},
                            {'label': 'Fall', 'value': 'Autumn'}
                        ],
                    ),
            ], className = "row"),

            #_______________________________________________________________________________________________ ROW 2: scatter 
            html.Div(
                style={'backgroundColor': colors['text']},                         # white backgroud of graph
                children = [                                             
                    html.Div([                                                      
                        dcc.Graph( id='Demo_ScatterPlot_Corr', figure = fig_demoCorr)
                    ], className="six columns"),                                    
                    
                    html.Div([                                                      
                        dcc.Graph( id='Demo_ScatterPlot', figure = fig_demoCorr   # will be replaced by fig from returnDemoScatterFig()
                        )
                    ], className="six columns"),                                   
            ], className = "row"),                                              
     
            #_______________________________________________________________________________________________ ROW 3:
            html.Div(
                style={'backgroundColor': colors['text']},                         # white backgroud of graph
                children = [                                             
                    html.Div([                                                      
                        dcc.Graph( id='Crime_ScatterPlot_Corr', figure = fig_crimeCorr)
                    ], className="six columns"),                                    
                    
                    html.Div([                                                      
                        dcc.Graph( id='Crime_ScatterPlot', figure = fig_crimeCorr # will be replaced by fig from returnCrimeScatterFig()
                        )
                    ], className="six columns"),                                   
            ], className = "row"),                                              
     
            # html.Div(className='row', children=[
            #     html.Div([
            #     dcc.Markdown(d("""
            #         **Hover Data**
            #         Mouse over values in the graph.
            #     """)),
            #     html.Pre(id='hover-data', style=styles['pre'])
            # ], className='row'),
            # ])
            
            #_______________________________________________________________________________________________ ROW 4:
            html.Div(
                style={'backgroundColor': colors['text']},                         # white backgroud of graph
                children = [                                             
                    html.Div([                                                      
                    ], className="six columns"),                                                        
                    html.Div([                                                      
                    ], className="six columns"),                                   
            ], className = "row"),   

        #_______________________________________________________________________________________________ END
        ],                                                                     
        className='ten columns offset-by-one'
    )# 2. GLOBAL DIV END
)



@app.callback(
    dash.dependencies.Output('Demo_ScatterPlot', 'figure'),               # Output: graph id im targetting, the property of id im targetting 
    [dash.dependencies.Input('Demo_ScatterPlot_Corr', 'hoverData')])      # Input: when i hover of a dot in this graph, activate this fucntion. get the 'hoverdata' 
def display_hover_data(hoverData):                              # hoverData = json data of each point. It holds the hover data i specified for each point
    if hoverData == None:
        return fig_demoCorr
    json_string = json.dumps(hoverData)
    jsonDict = json.loads(json_string)
    try:
        json_demoVar = jsonDict["points"][0]["x"]
        return returnDemoScatterFig(json_demoVar)      
    except:    
        return fig_demoCorr
    

@app.callback(
    dash.dependencies.Output('Crime_ScatterPlot', 'figure'),               # Output: graph id im targetting, the property of id im targetting 
    [dash.dependencies.Input('Crime_ScatterPlot_Corr', 'hoverData')])      # Input: when i hover of a dot in this graph, activate this fucntion. get the 'hoverdata' 
def display_hover_data(hoverData):                              # hoverData = json data of each point. It holds the hover data i specified for each point
    if hoverData == None:
        return fig_crimeCorr
    json_string = json.dumps(hoverData)
    jsonDict = json.loads(json_string)
    try:
        json_crimeVar = jsonDict["points"][0]["x"]
        return returnCrimeScatterFig(json_crimeVar)      
    except:    
        return fig_crimeCorr
    












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
#     return fig_demoCorr

if __name__ == '__main__':
    app.run_server(port=8038,debug=True)








































