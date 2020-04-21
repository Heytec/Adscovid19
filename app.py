import pandas as pd
import dash
import requests
import pandas as pd
import json
from pandas.io.json import json_normalize
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash
import plotly.graph_objects as gos
import plotly.express as px
from bs4 import BeautifulSoup
import dash_table

# Multi-dropdown options


# get relative data folder

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TK8Q9SS');</script>
<!-- End Google Tag Manager -->
        <title>ADS Research Center</title>
        
        {%favicon%}
        {%css%}
          {%metas%}
    </head>
    <body>
    <!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TK8Q9SS"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
          <h><cite> 2020 ADS R&D Center  </cite></h>
          <h>&nbsp;<cite> Contact us: africadataschool@gmail.com </cite></h>
         
        </footer>
    </body>
</html>"""



server = app.server



well_type_options = [
    {"label": 'kenya', "value":'kenya'}

]


# Load data
#function read json to dataframe
def readjsontodataframe(url):
    response = requests.get(url)
    json_object=json.loads(response.content)
    df= json_normalize(json_object[:])
    return df


# web scrapping for coronavirus
def GetDataWordMetric(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    data = []
    table = soup.find('table', id="main_table_countries_today")
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)  # Get rid of empty values
    return data


# make a dataframe and kenya dataonly

def kenyadataframe(data):
    colnames = ['Country',
                'Total cases',
                'New cases',
                'Total deaths',
                'New deaths',
                'Total recovered',
                'Active cases',
                'Serious_critical cases',
                'Total cases/1M pop',
                'Deaths/1M pop',
                'Total Tests',
                'Test/1M pop',
                'Continent']

    df = pd.DataFrame(data=data, columns=colnames)
    kenya = df[df.Country == 'Kenya']
    return kenya



def alldataframe(data):
    colnames = ['Country',
                'Total cases',
                'New cases',
                'Total deaths',
                'New deaths',
                'Total recovered',
                'Active cases',
                'Serious_critical cases',
                'Total cases/1M pop',
                'Deaths/1M pop',
                'Total Tests',
                'Test/1M pop',
                'Continent']

    df = pd.DataFrame(data=data, columns=colnames)
    df=df.head(14)

    return df

data1=GetDataWordMetric('https://www.worldometers.info/coronavirus/')
df=alldataframe(data1)


# Create global chart template


# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Kenya Covid-19 Tracker",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "ADS Research Center", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Africa Data School", id="learn-more-button"),
                            href="https://africadataschool.com/",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [


                        dcc.Dropdown(
                            id="kenya",
                            options=well_type_options,
                            value='kenya',

                            #value=list(WELL_TYPES.keys()),
                            className="dcc_control",
                        ),

                        html.P(id="worldupdate",
                            className="control_label",
                        ),

                        html.P(
                            "Data is sourced from WHO,Johns Hopkins CSSE,Ministry of Health Kenya,Worldometer,Daily Nation and Ushahidi.  ",
                            className="control_label",
                        ),
                        html.P(
                            "December 2019, a local outbreak  was detected in Wuhan (Hubei, China) . The outbreak has since spread to mainland China as well as 185 other countries and regions, with more than 2 million confirmed cases as of April 17, 2020.4. In response to this ongoing public health emergency, we developed an online interactive dashboard, hosted by the Center for Research and Development at Africa Data School to visualise and track  Kenya daily reported cases of coronavirus disease.",
                            className="control_label",

                        ),

                        html.P(
                            "Credits : Africa Data School Team,Johns Hopkins,Covid19API-Kyle Redelinghuys and Ushahidi",
                            className="control_label",

                        ),


                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [

                                html.Div(

                                    [html.H6(id="confirmed"), html.P("Confirmed")],
                                    id="wells",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="recovered"), html.P("Recovered")],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="death"), html.P("Death")],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="active"), html.P("Active")],
                                    id="water",
                                    className="mini_container",
                                ),





                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="bar_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),

html.Div([
        html.Div(
            [
            html.Div(

                [html.H6(id="tested"), html.P("Tested")],
                id="wells0O",
                className="mini_container",
            ),
            html.Div(
                     [html.H6(id="new_cases"), html.P("New Cases ")],
                      id="gas0",
                      className="mini_container",
                        ),

            html.Div(
                            [html.H6(id="new_deaths"), html.P("New Deaths ")],
                            id="oilO",
                            className="mini_container",
                        ),
            html.Div(
                            [html.H6(id="tot_cas_pop"), html.P("Total Cases/1M pop")],
                            id="waterO",
                            className="mini_container",
                        ),


        ], className="row container-display", ),

],),




        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="individual_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(

                        [ html.Label("3D Representation of cases"),
                            dcc.Graph(id="three_graph")],
                      className="pretty_container seven columns",

                ),
                html.Div(
                    [dcc.Graph(id="aggregate_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),

        html.Div(
            [
                html.Div(

                    [  html.Label("Daily Nation • Last Update"),
                        html.Iframe(src='https://public.flourish.studio/visualisation/1603849/embed?auto=1',width=300,height=400,style={
                            "border":"0",
                            "framebolder":'0'

                        })],
                    className="pretty_container three columns",
                ),
                html.Div(
                    [ html.Label("The map shows the county of residence of persons that have tested positive"),
                        html.Iframe(src='https://public.flourish.studio/visualisation/1603839/embed?auto=1',width=300,height=400,style={
                            "border":"0",
                            "framebolder":'0'

                        })],
                    className="pretty_container four columns",
                ),

                html.Div(
                    [
                     html.Iframe(src='https://kenyacovid19.ushahidi.io/views/data', width=300,
                                 height=400,style={
                            "border":"0",
                            "framebolder":'0'

                        })],
                    className="pretty_container four columns",
                ),

                html.Div(
                    [   html.Label("East Africa"),
                        html.Iframe(src='https://public.flourish.studio/visualisation/1603846/embed?auto=1', width=400,
                                    height=400,style={
                            "border":"0",
                            "framebolder":'0'

                        })],
                    className="pretty_container four columns",
                ),

            ],
            className="row flex-display",
        ),



        html.Div(
                    [
                        html.Div([

                            dash_table.DataTable(
                                id='table',
                                columns=[{"name": i, "id": i} for i in df.columns],
                                data=df.to_dict('records'), style_table={'overflowX': 'scroll'},
                                style_data_conditional=[{
                                        "if": {"row_index": 7},
                                        "backgroundColor": "#3D9970",
                                        'color': 'white'
                                    }]




                            ),

                        ],
                            className="pretty_container twelve columns",

                        ),

                    ],
                    className="row flex-display",
                ),





 ],
    #id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},


)











#confirmed ......................................
@app.callback(
    Output("confirmed", "children"), [
        Input("kenya", "value"),

    ],)
def update_well_text(well_statuses):
    #url = 'https://api.covid19api.com/total/dayone/country/kenya/status/confirmed'
    #url = 'https://api.covid19api.com/country/kenya'

    #url = 'https://api.covid19api.com/country/kenya'
    #df = readjsontodataframe(url)
    # confirmed last no
    #Confirmedlastrow = df.tail(1)
    #Confirmedno = Confirmedlastrow['Confirmed'].values[0]

    data = GetDataWordMetric('https://www.worldometers.info/coronavirus/')
    kenya = kenyadataframe(data)
    Total_cases = kenya['Total cases'].values[0]
    Total_cases=int(Total_cases)


    return Total_cases

#recoverd cases ......................................................

@app.callback(
    Output("recovered", "children"), [
        Input("kenya", "value"),

    ],)
def update_well_text(well_statuses):
    #url = 'https://api.covid19api.com/total/dayone/country/kenya/status/confirmed'
    url = 'https://api.covid19api.com/country/kenya'

    #url = 'https://api.covid19api.com/country/kenya'
    df = readjsontodataframe(url)
    # confirmed last no
    recoverdlastrow = df.tail(1)
    revoverdno = recoverdlastrow['Recovered'].values[0]
    revoverdno


    #world meter
    data = GetDataWordMetric('https://www.worldometers.info/coronavirus/')
    kenya = kenyadataframe(data)
    Total_recovered = kenya['Total recovered'].values[0]
    Total_recovered=int(Total_recovered)
    return  Total_recovered

#death.......................................................................


@app.callback(
    Output("death", "children"), [
        Input("kenya", "value"),

    ],)
def update_well_text(well_statuses):
    #url = 'https://api.covid19api.com/total/dayone/country/kenya/status/confirmed'
    url = 'https://api.covid19api.com/country/kenya'

    #url = 'https://api.covid19api.com/country/kenya'
    df = readjsontodataframe(url)
    # confirmed last no
    # confirmed last no
    Deathslastrow = df.tail(1)
    Deathsno = Deathslastrow['Deaths'].values[0]
    Deathsno

    data = GetDataWordMetric('https://www.worldometers.info/coronavirus/')
    kenya = kenyadataframe(data)
    Total_deaths = kenya['Total deaths'].values[0]

    return  int(Total_deaths)


#  active cases in kenya
@app.callback(
    Output("active", "children"), [
        Input("kenya", "value"),

    ],)
def update_well_text(well_statuses):
    data = GetDataWordMetric('https://www.worldometers.info/coronavirus/')
    kenya = kenyadataframe(data)
    Active_cases = kenya['Active cases'].values[0]
    int(Active_cases)


    return  int(Active_cases)




#  active cases in kenya
@app.callback(
    Output("worldupdate", "children"), [
        Input("kenya", "value"),

    ],)

# world updatev
def update_well_text(well_statuses):
    page = requests.get('https://www.worldometers.info/coronavirus/')
    soup = BeautifulSoup(page.text, 'html.parser')
    titletest = soup.title.text


    return  titletest


#  total tested  cases in kenya
@app.callback(
    Output("tested", "children"), [
        Input("kenya", "value"),

    ],)
def update_well_text(well_statuses):
    data = GetDataWordMetric('https://www.worldometers.info/coronavirus/')
    kenya = kenyadataframe(data)
    # total test
    Total_test = kenya['Total Tests'].values[0]
    Total_test


    return  Total_test


#  new cases  cases in kenya
@app.callback(
    Output("new_cases", "children"), [
        Input("kenya", "value"),

    ],)
def update_well_text(well_statuses):
    data = GetDataWordMetric('https://www.worldometers.info/coronavirus/')
    kenya = kenyadataframe(data)
    # total test
    # new cases
    New_cases = kenya['New cases'].values[0]
    New_cases


    return New_cases


# new deaths
@app.callback(
    Output("new_deaths", "children"), [
        Input("kenya", "value"),

    ],)
def update_well_text(well_statuses):
    data = GetDataWordMetric('https://www.worldometers.info/coronavirus/')
    kenya = kenyadataframe(data)
    # total test
    # new cases
    # new death
    New_deaths = kenya['New deaths'].values[0]
    New_deaths


    return New_deaths


# total cases per 1 milliom
@app.callback(
    Output("tot_cas_pop", "children"), [
        Input("kenya", "value"),

    ],)
def update_well_text(well_statuses):
    data = GetDataWordMetric('https://www.worldometers.info/coronavirus/')
    kenya = kenyadataframe(data)
    # total test
    # new cases
    # new death
    Total_cases_pop = kenya['Total cases/1M pop'].values[0]
    Total_cases_pop


    return Total_cases_pop









#bar chart at the top of things
@app.callback(Output('bar_graph', 'figure'),
              [Input('kenya', 'value')])
def update_figure(kenya):
    #url = 'https://api.covid19api.com/country/kenya'
    url = 'https://api.covid19api.com/total/dayone/country/kenya/status/confirmed'

    df = readjsontodataframe(url)
    traces = []

    traces.append(go.Bar(
            x=df.Date,
            y=df.Cases,

        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': 'Date'
            },
            yaxis={
                'title': 'Confirmed'
            },
          title='Confirmed'
        )
    }

# confrinmed cases
@app.callback(Output('main_graph', 'figure'),
              [Input('kenya', 'value')])
def update_figure(well_statuses):
    #url = 'https://api.covid19api.com/country/kenya'
    url = 'https://api.covid19api.com/total/dayone/country/kenya/status/confirmed'

    df = readjsontodataframe(url)
    traces = []

    traces.append(go.Scatter(
            x=df.Date,
            y=df.Cases,
            mode='markers+lines',
            marker=dict(
                color='#ffff5a',
                size=10,
                line=dict(
                    color='MediumPurple',
                    width=2
                )
            ),
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': 'Date'
            },
            yaxis={
                'title': 'Confirmed '
            },
          title='Confirmed Curve'

        )
    }



@app.callback(Output('individual_graph', 'figure'),
              [Input('kenya', 'value')])
def update_figure(well_statuses):
    url = 'https://api.covid19api.com/country/kenya'

    df = readjsontodataframe(url)
    traces = []

    traces.append(go.Scatter(
            x=df.Date,
            y=df.Recovered,
            mode='markers+lines',
            marker=dict(
            color='#60ad5e',
            size=10,
            line=dict(
                color='MediumPurple',
                width=2
            )
        ),



            #opacity=0.7,
            #marker={'size': 15},
            #name=continent_name
        ))

    return {
        'data': traces,
        'layout': go.Layout(


            xaxis={
                'title': 'Date'

            },
            yaxis={
                'title': 'Recovered'

            },
          title='Recovered'

        )
    }





# deaths ..............
@app.callback(Output('aggregate_graph', 'figure'),
              [Input('kenya', 'value')])
def update_figure(well_statuses):
    url = 'https://api.covid19api.com/country/kenya'

    df = readjsontodataframe(url)
    traces = []

    traces.append(go.Scatter(
            x=df.Date,
            y=df.Deaths	,
            mode='markers+lines',
            #marker_color=df['Death'],
            marker=dict(
            color='#9b0000',
            size=10,
            line=dict(
                color='MediumPurple',
                width=2
            )
           ),


            #opacity=0.7,
            #marker={'size': 15},
            #name=continent_name
        ))

    return {
        'data': traces,
        'layout': go.Layout(


            xaxis={
                'title': 'Date'

            },
            yaxis={
                'title': 'Deaths'

            },
          title='Deaths'

        )
    }


# 3d graph ..............
@app.callback(Output('three_graph', 'figure'),
              [Input('kenya', 'value')])
def update_figure(well_statuses):
    url = 'https://api.covid19api.com/country/kenya'

    df = readjsontodataframe(url)
    traces = []

    traces = go.Figure(data=[go.Scatter3d(
        x=df.Date,
        y=df.Confirmed,
        z=df.Deaths,
        mode='markers',
        marker=dict(
            size=12,
            color=df.Deaths,  # set color to an array/list of desired values
            colorscale='Viridis',  # choose a colorscale
            opacity=0.8
        )
    )])

    layout = go.Layout(
        title='Confirmed Cases'
    )

    fig = go.Figure(data=traces, layout=layout)
    return  fig


#map
@app.callback(Output('map_graph', 'figure'),
              [Input('kenya', 'value')])
def update_figure(well_statuses):
    mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"

    df = pd.read_csv("kenya_county.csv")
    df = pd.DataFrame(df)
    mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"
    px.set_mapbox_access_token(mapbox_access_token)
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", color="corona_cases", size="corona_cases",
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=5, hover_name='county',
                            center=dict(lat=-0.02,
                                        lon=37.91))

    #fig.show()

    return  #fig






# Add the server clause:
if __name__ == '__main__':
    app.run_server()


