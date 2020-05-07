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

widthPlot  = 700
heightPlot = 900

heightPlot2 = 1200    # for the crime data to have space at bottom to show labels
season_to_show_deafult = "ALL_SEASONS"

######################################################################################################### DEMOGRAPHIC DATA
# A1) PLOT 1: Demographic Pearson R Correlation Scatter Plot
def returnDemoCorrFig(season_to_show): 
    fig_demoCorr = px.scatter(
        corr_demoDF, x="DemographicVariable", y=season_to_show, 
        color=season_to_show, 
        # color_continuous_scale=px.colors.sequential.RdBu,
        width=widthPlot, height=heightPlot,
        hover_data=['DemographicVariable', season_to_show])
    fig_demoCorr.update_layout(
        title = '(Pearson r Correlation) Gas Reports of '+season_to_show+' VS Demographic Data',
        yaxis_title = "Gas Reports per Tract ("+season_to_show+") vs Demographic Variables Correlation",
        xaxis_title = "Demographic Variables",
    )
    return fig_demoCorr

# A2) PLOT 2: A scatter plot function for any Demograpic variable vs NYFD gas reports of a choosen season
def returnDemoScatterFig(chosenCol='Total; Estimate; Total population', season_to_show="ALL_SEASONS"):     
    fig = px.scatter(
        merged_demoDF, x=season_to_show, y=chosenCol, 
        # color_continuous_scale=px.colors.sequential.RdBu,
        color=chosenCol,
        hover_data=['Geoid', season_to_show, "Geography" ],     
        opacity=0.2,     
        width=widthPlot, height=600)
    fig.update_layout(
        title = "Number of Reports Per Census Tract ("+season_to_show+") vs "+chosenCol,
        xaxis_title = "Number of Gas Reports Per Census Tract ("+season_to_show+")",
        yaxis_title = chosenCol,
    )
    return fig

# ################################################################################################################################ CRIME DATA
# B1) PLOT 3:  Crime Pearson R Correlation Scatter Plot
def returnCrimeCorrFig(season_to_show): 
    fig_crimeCorr = px.scatter(
        corr_crimeDF, x="Crimes", y=season_to_show, 
        # color_continuous_scale=px.colors.sequential.RdBu,
        color=season_to_show, 
        width=widthPlot, height=heightPlot2)
    fig_crimeCorr.update_layout(
        title = '(Pearson r Correlation) Gas Reports of '+season_to_show+' VS Crimes Data',
        yaxis_title = "Gas Reports per Tract ("+season_to_show+") vs Crime Variables Correlation",
        xaxis_title = "Crime Variables",
    )
    return fig_crimeCorr

# B2) PLOT 4: A scatter plot function for any Crime variable vs NYFD gas reports of a choosen season
def returnCrimeScatterFig(chosenCol="TotalCrime", season_to_show="ALL_SEASONS"):     
    fig = px.scatter(
        merged_crimeDF, x=season_to_show, y=chosenCol, 
        # color_continuous_scale=px.colors.sequential.RdBu,
        color=chosenCol, 
        hover_data=['Geoid', season_to_show, "TotalCrime" ],
        opacity=0.2,
        width=widthPlot, height=600
        )
    fig.update_layout(
        title = "Number of Reports Per Census Tract ("+season_to_show+") vs "+chosenCol,
        xaxis_title = "Number of Gas Reports Per Census Tract ("+season_to_show+")",
        yaxis_title = chosenCol
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
        children = 
        [                                                             
            html.Div(
                style={                                                                                       # background fo graph to be white
                    'backgroundColor': colors['background'],
                    'margin': 0
                },   
                children = [
                    html.H1(children='GAS REPORT DASHBOARD'),                
                    html.Div(children="Pick the season you want to plot. Hover over a correlation dot to show the data for each census tract"),
                ]
            ),
            #_______________________________________________________________________________________________ ROW 1: drop down
            html.Div(
                style={                                                                                       # background fo graph to be white
                    'backgroundColor': colors['text'],
                    'marginBottom': 0, 'marginTop': 0
                },                         
                children = [ 
                    dcc.Dropdown(
                        id='dropdown',
                        options=[
                            {'label': 'All Seasons', 'value': "ALL_SEASONS"},
                            {'label': 'Summer', 'value': 'Summer'},
                            {'label': 'Spring', 'value': 'Spring'},
                            {'label': 'Winter', 'value': 'Winter'},
                            {'label': 'Fall', 'value': 'Autumn'}
                        ],
                        value = 'ALL_SEASONS'
                    ),
            ], className = "row"),

            #_______________________________________________________________________________________________ ROW 2: Plot 1 2
            html.Div(
                style={                                                                                       
                    'backgroundColor': colors['text'],
                    'marginBottom': 50, 'marginTop': 40,
                },  
                children = [                                             
                    html.Div([                                                      
                        dcc.Graph( id='Demo_ScatterPlot_Corr', figure = returnDemoCorrFig(season_to_show_deafult))
                    ], className="six columns"),                                    
                    html.Div([                                                      
                        dcc.Graph( id='Demo_ScatterPlot', figure = returnDemoScatterFig()#returnDemoCorrFig(season_to_show_deafult)   # will be replaced by fig from returnDemoScatterFig()
                        )
                    ],className="six columns"),                                   
            ], className = "row"),                                              
     
            #_______________________________________________________________________________________________ ROW 3: Plot 3 4
            html.Div(
                style={                                                                                       
                    'backgroundColor': colors['text'],
                    'marginBottom': 50, 'marginTop': 40,
                },                  
                children = [                                             
                    html.Div([                                                      
                        dcc.Graph( id='Crime_ScatterPlot_Corr', figure = returnCrimeCorrFig(season_to_show_deafult))
                    ], className="six columns"),                                    
                    
                    html.Div([                                                      
                        dcc.Graph( id='Crime_ScatterPlot', figure = returnCrimeScatterFig()#returnCrimeCorrFig(season_to_show_deafult) # will be replaced by fig from returnCrimeScatterFig()
                        )
                    ], className="six columns"),                                   
            ], className = "row"),                                              
            
            #_______________________________________________________________________________________________ ROW 4: Parallel

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



# dropdown
@app.callback(
        [   dash.dependencies.Output('Demo_ScatterPlot_Corr', 'figure'),
            dash.dependencies.Output('Crime_ScatterPlot_Corr', 'figure'),
        ],
        [dash.dependencies.Input('dropdown', 'value')]
    )    #getting the all seasons
def update_figure(hoverData):                              # hoverData is a json data
    season_to_show_deafult = hoverData
    return returnDemoCorrFig(hoverData), returnCrimeCorrFig(hoverData)#, returnDemoScatterFig(chosenCol_demo, hoverData)#,returnCrimeScatterFig(chosenCol_crime, hoverData)


@app.callback(
    dash.dependencies.Output('Demo_ScatterPlot', 'figure'),               # Output: graph id im targetting, the property of id im targetting 
    [dash.dependencies.Input('Demo_ScatterPlot_Corr', 'hoverData')])      # Input: when i hover of a dot in this graph, activate this fucntion. get the 'hoverdata' 
def update_figure2(hoverData):                              # hoverData = json data of each point. It holds the hover data i specified for each point
    if hoverData == None:
        return  returnDemoScatterFig()

    json_string = json.dumps(hoverData)
    jsonDict = json.loads(json_string)
    try:
        json_demoVar = jsonDict["points"][0]["x"]
        
        return returnDemoScatterFig(json_demoVar,season_to_show_deafult)      
    except:    
        return  returnDemoScatterFig()
    

@app.callback(
    dash.dependencies.Output('Crime_ScatterPlot', 'figure'),               # Output: graph id im targetting, the property of id im targetting 
    [dash.dependencies.Input('Crime_ScatterPlot_Corr', 'hoverData')])      # Input: when i hover of a dot in this graph, activate this fucntion. get the 'hoverdata' 
def update_figure3(hoverData):                              # hoverData = json data of each point. It holds the hover data i specified for each point
    if hoverData == None:
        return  returnCrimeScatterFig()
    json_string = json.dumps(hoverData)
    jsonDict = json.loads(json_string)
    try:
        json_crimeVar = jsonDict["points"][0]["x"]
        return returnCrimeScatterFig(json_crimeVar,season_to_show_deafult)      
    except:    
        return  returnCrimeScatterFig()
    


if __name__ == '__main__':
    app.run_server(port=8038,debug=True)








































