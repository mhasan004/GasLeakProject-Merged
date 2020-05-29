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

stateCount = 0                          # ************** since dash doesnt tell u what input triggered a callback, use this varibale to write to an invisible div, extracting the div var and see which input it was that called it
# For Demogrpahic Graph:
csvFile_demoMerged = "DataFiles/FDNY/Seasonal2017_2018_Demographics.csv"
merged_demoDF = pd.read_csv(csvFile_demoMerged)
csvFile_demoCorr = "DataFiles/FDNY/Seasonal2017_2018_Demographic_Correlation.csv"
corr_demoDF = pd.read_csv(csvFile_demoCorr)

# For Crime Graphs:
csvFile_crimeMerged  = "DataFiles/Crime and Demographics/Crime/ACS_10_5YR_S0101_With_Census_Data_FILTERED_Merged.csv"
merged_crimeDF = pd.read_csv(csvFile_crimeMerged)
csvFile_crimeCorr     = "DataFiles/Crime and Demographics/Crime/ACS_10_5YR_S0101_With_Census_Data_FILTERED_Corr.csv"
corr_crimeDF = pd.read_csv(csvFile_crimeCorr)

# For Parallel graph:
NYFD_Crime2_CSV_For_Parallel= "DataFiles/Crime and Demographics/Crime/NYPD_Complaint_Data_Historic_WITH_CENSUS_DATA_Filtered_Merged_FilteredMore.csv"
parallelDF = pd.read_csv(NYFD_Crime2_CSV_For_Parallel)
colorCol = "BoroughColors"
countyColorOrder = ["Richmond County", "Queens County", "Bronx County","Kings County","New York County"]
filteredCol = [
    'Geoid',
    'TotalCrime',
    'Spring',
    'Summer',
    'Autumn',
    'Winter',
    'ALL_SEASONS',
    'CountyName',
    'CountyName',
    'CensusTract_2010_NAME',
    'BoroughColors'
]

# For correlation crime and demo headers so less compact:
demoHeaders = list(corr_demoDF.columns) + list(merged_demoDF.columns) 
crimeHeaders = list(corr_crimeDF.columns) + list(merged_crimeDF.columns) 

widthPlot  = 700
heightPlot = 900

heightPlot2 = 1200    # for the crime data to have space at bottom to show labels
season_to_show_deafult = "ALL_SEASONS"

######################################################################################################### NYFD DEMOGRAPHIC DATA
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

# ################################################################################################################################ NYFD CRIME DATA
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
# ################################################################################################################################ NYFD CRIME DATA Parallel
def geoid_ticks_to_plot(pick = "ALL_SEASONS"):
    # 1) What geoids should be plotted in the parallel graph?
    if pick == "ALL_SEASONS":
        tick_tickIds = list(range(0,len(parallelDF)))                                   # [0...2024] - tickvals, values. parallelDF row ids for all stuff im printign
        tick_geoidTickVals = list(parallelDF["Geoid"])                                  # will be tickvals and values
        tick_geoidTickVals_str = [ str(x) for x in tick_geoidTickVals ]                 # turnign geoidList to geoidList where the string geoid and ints
        return [tick_tickIds, tick_geoidTickVals_str]
    tick_tickIds = parallelDF.index[parallelDF['Geoid'] ==int(pick)].tolist()           # the parallelDF row id for that geoid
    tick_geoidTickVals_str = [str(tick_tickIds)]
    return [tick_tickIds, tick_geoidTickVals_str]

def making_dimension_list_for_parallel( GEOID_to_plot):
    global parallelDF
    parallelDF = parallelDF[filteredCol]                                                # doing this so the parallel plot dont get so squished
    # 2) Making an array of dictionaries. Each dict is holds the attributes of each bar of the parallel graph
    dimList = list()
    dimList.append(
        dict(
            range    = [0, len(parallelDF)],                                            # 1) tick0, tick1, etc....
            tickvals = list(range(0,len(parallelDF), 100)),  # (1) numbering ticks to be named 
            values   = geoid_ticks_to_plot(GEOID_to_plot)[0],                           # (2) which rows to shows? selects the tickids
            label    = 'Geoid',                                                         # (3) label the bar
            ticktext = geoid_ticks_to_plot(GEOID_to_plot)[1],                           # (4) name of each tick?
        ))     
    for col in parallelDF:
        if col == "Geoid" or col == "CountyName" or col == "CensusTract_2010_NAME" or col == "BoroughColors":
            continue
        parallelBarForCol = dict(
            range = [parallelDF[col].min(), parallelDF[col].max()],
            label = col, 
            values = parallelDF[col]
        )
        dimList.append(parallelBarForCol)
    return dimList

def return_parallel_plot_fig( GEOID_to_plot = "ALL_SEASONS", height = 800):
    # 3) Plot:
    fig = go.Figure(
        data = go.Parcoords(
            # LINE COLOR DEF: 
            line = dict( 
               color = parallelDF[colorCol],                                        # each lines' color val
               colorscale = ["purple", "lightcoral", "red", "firebrick","maroon"],  # [counties0->4]
               colorbar = dict(
                   tickvals = [0,1,2,3,4],                                          # [counties0->4]
                   ticktext = countyColorOrder,                                     # [counties0->4]
                   title = {'text': "NYC Counties"},
                   x = -0.5,                                                        # ******delete this to turn the colorscale bar to normal position
                   ticks = "outside",
               ),
               showscale = True,                                                    # show the scale 
               cmin = parallelDF[colorCol].min(),
               cmax = parallelDF[colorCol].max(),
            ),
            dimensions = making_dimension_list_for_parallel(GEOID_to_plot),
            labelangle = -45,
        )
    )

    fig.update_layout(
        title = "Focused look on Season Gas Leak Reports and Total Crime of all GEOID in NYC",
        autosize=False,
        width  = widthPlot,#1000,
        height = height,#700,
        margin=dict(
            l=10,
            r=100,
            b=10,
            t=200,
            pad=4
        ),
    )
    return fig
# parallel_plot("ALL_SEASONS").show()

# ################################################################################################################################ 


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']               # external cssCSS file for Bootstraps
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)                # initialize app with the external CSS file
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
            html.Div(id='storeVal_demo', style={'display': 'none'}),
            html.Div(id='storeVal_crime', style={'display': 'none'}),

            html.Div(
                style={                                                                                       # background fo graph to be white
                    'backgroundColor': colors['background'],
                    # 'marginTop': 10,
                    # 'marginBottom': 10,
                    # 'position': "absolute",
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
                    'marginBottom': 0, 'marginTop': 0,
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
            ],className = "row"),

            #_______________________________________________________________________________________________ ROW 2: Plot 1 2
            html.Div(
                style={                                                                                       
                    'backgroundColor': colors['text'],
                    'marginBottom': 50, 'marginTop': 40,
                },  
                children = [                                             
                    html.Div([                                                      
                        dcc.Graph( id='Demo_ScatterPlot_Corr', figure = returnDemoCorrFig(season_to_show_deafult))
                    ],  className="four columns"),                                    
                    html.Div([                                                      
                        dcc.Graph( id='Demo_ScatterPlot', figure = returnDemoScatterFig()                   # returnDemoCorrFig(season_to_show_deafult)   # will be replaced by fig from returnDemoScatterFig()
                        )
                    ],className="four columns"),

                    html.Div([       
                        dcc.Graph( id='Crime_ParallelPlot', figure = return_parallel_plot_fig("ALL_SEASONS"))
                    ], className="four columns"),     

            ], 
            className = "row"
            ),                                              
     
            #_______________________________________________________________________________________________ ROW 3: Plot 3 4
            html.Div(
                style={                                                                                       
                    'backgroundColor': colors['text'],
                    'marginBottom': 0, 'marginTop': 10,
                },                  
                children = [                                             
                    html.Div([                                                      
                        dcc.Graph( id='Crime_ScatterPlot_Corr', figure = returnCrimeCorrFig(season_to_show_deafult))
                    ], className="four columns"),                                    
                    
                    html.Div([                                                      
                        dcc.Graph( id='Crime_ScatterPlot', figure = returnCrimeScatterFig()#returnCrimeCorrFig(season_to_show_deafult) # will be replaced by fig from returnCrimeScatterFig()
                        )
                    ], className="four columns"),                                   
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
            
            #_______________________________________________________________________________________________ ROW 4: Parallel
            # html.Div(
            #     style={                                                                                       
            #         'backgroundColor': colors['text'],
            #         'marginBottom': 500, 'marginTop': 0,
            #     },                 
            #     children = [                                             
            #         html.Div([       
            #             dcc.Graph( id='Crime_ParallelPlot', figure = return_parallel_plot_fig("ALL_SEASONS"))
            #         ], className="twelve columns"),                                  
            # ], className = "row"),   

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
def update_figure1(hoverData):                                             # hoverData is a json data
    season_to_show_deafult = hoverData
    return returnDemoCorrFig(hoverData), returnCrimeCorrFig(hoverData)

@app.callback(
    dash.dependencies.Output('Demo_ScatterPlot', 'figure'),               # Output: graph id im targetting, the property of id im targetting 
    [dash.dependencies.Input('Demo_ScatterPlot_Corr', 'hoverData')])      # Input: when i hover of a dot in this graph, activate this fucntion. get the 'hoverdata' 
def update_figure2(hoverData):                                            # hoverData = json data of each point. It holds the hover data i specified for each point
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
        dash.dependencies.Output('Crime_ScatterPlot', 'figure'),               
        [dash.dependencies.Input('Crime_ScatterPlot_Corr', 'hoverData')]
    )      
def update_figure3(hoverData):                              
    if hoverData == None:
        return  returnCrimeScatterFig()
    json_string = json.dumps(hoverData)
    jsonDict = json.loads(json_string)
    try:
        json_crimeVar = jsonDict["points"][0]["x"]
        return returnCrimeScatterFig(json_crimeVar,season_to_show_deafult)      
    except:    
        return  returnCrimeScatterFig()
    





# @app.callback(
#         dash.dependencies.Output('Crime_ParallelPlot', 'figure'),             
#         [   
#             dash.dependencies.Input('Demo_ScatterPlot', 'hoverData'),
#             dash.dependencies.Input('Crime_ScatterPlot', 'hoverData')
#         ]
#     )
# def update_figure3(hoverData1, hoverData2):   
#     print("                  started")                           
#     if hoverData1 == None and hoverData2 == None:
#         return  return_parallel_plot_fig("ALL_SEASONS")
    
#     hoverData = None
#     if (hoverData1 != None) and :
#         hoverData = hoverData1
#     elif hoverData2 != None:
#         hoverData = hoverData2
    
#     print(hoverData)

#     print()

    # json_string = json.dumps(hoverData)
    # jsonDict = json.loads(json_string)
    # try:
    #     json_dot_geoid = jsonDict["points"][0]["customdata"][0]
    #     print("doing: "+str(json_dot_geoid))
    #     return  return_parallel_plot_fig(json_dot_geoid)
    # except:
    #     return  return_parallel_plot_fig("ALL_SEASONS")




# @app.callback(
#         dash.dependencies.Output('storeVal_demo', 'children'),             
#         [   dash.dependencies.Input('Demo_ScatterPlot', 'hoverData') ]
#     )
# def update_figure_P1(hoverData): 
#     global stateCount
#     stateCount += 1  
#     if hoverData == None:
#         return  [return_parallel_plot_fig("ALL_SEASONS"), stateCount]
#     json_string = json.dumps(hoverData)
#     jsonDict = json.loads(json_string)
#     try:
#         json_dot_geoid = jsonDict["points"][0]["customdata"][0]
#         return  [return_parallel_plot_fig(json_dot_geoid), stateCount]
#     except:
#         return  [return_parallel_plot_fig("ALL_SEASONS"), stateCount]


# @app.callback(
#         dash.dependencies.Output('storeVal_crime', 'children'),             
#         [   dash.dependencies.Input('Crime_ScatterPlot', 'hoverData') ]
#     )
# def update_figure_P2(hoverData):   
#     global stateCount
#     stateCount += 1  
#     if hoverData == None:
#         return  [return_parallel_plot_fig("ALL_SEASONS"), stateCount]
#     json_string = json.dumps(hoverData)
#     jsonDict = json.loads(json_string)
#     try:
#         json_dot_geoid = jsonDict["points"][0]["customdata"][0]
#         return  [return_parallel_plot_fig(json_dot_geoid), stateCount]
#     except:
#         return  [return_parallel_plot_fig("ALL_SEASONS"), stateCount]

# @app.callback(
#         dash.dependencies.Output('Crime_ParallelPlot', 'figure'),             
#         [   
#             dash.dependencies.Input('storeVal_crime', 'children'),
#             dash.dependencies.Input('storeVal_demo', 'children'),
#         ]
#     )
# def update_figure_P3(geoidToPlotFig1, geoidToPlotFig2): 
#     print("crime: "+str(geoidToPlotFig1[1]))
#     print("demog: "+str(geoidToPlotFig2[1]))

#     print("-----------------------")
#     # return geoidToPlotFig




@app.callback(
        dash.dependencies.Output('storeVal_demo', 'children'),             
        [   dash.dependencies.Input('Demo_ScatterPlot', 'hoverData') ]
    )
def update_figure_P1(hoverData): 
    global stateCount
    stateCount += 1  
    return stateCount

@app.callback(
        dash.dependencies.Output('storeVal_crime', 'children'),             
        [   dash.dependencies.Input('Crime_ScatterPlot', 'hoverData') ]
    )
def update_figure_P2(hoverData):   
    global stateCount
    stateCount += 1  
    return stateCount


@app.callback(
        dash.dependencies.Output('Crime_ParallelPlot', 'figure'),             
        [   
            dash.dependencies.Input('storeVal_demo', 'children'),
            dash.dependencies.Input('storeVal_crime', 'children'),
            dash.dependencies.Input('Demo_ScatterPlot', 'hoverData'),
            dash.dependencies.Input('Crime_ScatterPlot', 'hoverData')
        ]
    )
def update_figure_P3(state1, state2, demoHover, crimeHover): 
    if (state1 == None and state2 ==None) or (state1==state2):
        return  return_parallel_plot_fig("ALL_SEASONS")
    json_string = ""
    if state1 > state2:
        json_string = json.dumps(demoHover)
    if state2 > state1:
        json_string = json.dumps(crimeHover)
    jsonDict = json.loads(json_string)
    try:
        json_dot_geoid = jsonDict["points"][0]["customdata"][0]
        return  return_parallel_plot_fig(json_dot_geoid,400)
    except:
        return  return_parallel_plot_fig("ALL_SEASONS")

if __name__ == '__main__':
    app.run_server(port=8129,debug=True)








































