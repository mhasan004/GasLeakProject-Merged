import dash
import dash_core_components as dcc   # has a component for every HTML tag (html.H1() puts the string in a h1 html tag for ex)
import dash_html_components as html  # 
import plotly.graph_objects as go
import pandas as pd

crimeCSVFILE = "NYPD_Complaint_Data_Historic_WITH_CENSUS_DATA_Filtered_Merged.csv"
df = pd.read_csv(crimeCSVFILE)
df = df[0:4]

geoidList = list(df["Geoid"]) # will be tickvals and values
geoidStrList = [ str(x) for x in geoidList ] #turnign geoidList to geoidList where the string geoid and ints

# 1) Making an array of dictionaries. Each dict is holds the attributes of each bar 
dimList = list()
dimList.append(
    dict(
        range    = [df["Geoid"].min(), df["Geoid"].max()],  # 1) range of bar
        tickvals = geoidList, #2) all the ticks that can be selected
        values   = geoidList, #3) ticks that are selected
        label    = 'Geoid',   #4) label the bar
        ticktext = geoidStrList #5) label each tick

    ))              
for col in df:
    if col == "Geoid" or col == "CountyName" or col == "CensusTract_2010_NAME":
        continue
    parallelBarForCol = dict(
        range = [df[col].min(), df[col].max()],
        label = col, 
        values = df[col]
    )
    dimList.append(parallelBarForCol)

# Chnage Col order:
cols = list(df.columns)
cols.remove("TotalCrime")
cols.insert(6,"TotalCrime")
df = df[cols]

# 2) Plot:
colorCol = "TotalCrime"
figParallel = go.Figure(
    data = go.Parcoords(
        # LINE COLOR DEF: 
        line = dict( 
           color = df[colorCol], #each lines' color val
           colorscale = "Electric",
           showscale = True, #show the scale 
           cmin = df[colorCol].min(),
           cmax = df[colorCol].max()
        ),
        dimensions = dimList
    )
)


figParallel.update_layout(
    autosize=False,
    width=9000,
    height=500,    
)
figParallel.update_yaxes(
    tickangle=45,
    #  tickfont=dict(family='Rockwell', color='crimson', size=14)
)

# figParallel.update_yaxes(automargin=True)







#####################################
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
            html.Div(children="dahs app"),

            ############## ROW 1
            html.Div([                                                          # 3. ROW 1 DIV START
                # html.Div([                                                      # 4. ROW 1 - half START
                dcc.Graph(
                    id='parallelGraph',                                                  # id of the graph
                    figure = figParallel
                )
                # ], className="twelve columns"),                                    # 4. ROW 1 - half END
            ], className = "row"),                                              # 3. ROW 1 DIV END
            ############ END
        ],                                                                      # 1. GLOBAL CHILDREN DIV END
        className='ten columns offset-by-one'
    )                                                                           # 2. GLOBAL DIV END
)


if __name__ == '__main__':
    app.run_server(port=8008,debug=True)
