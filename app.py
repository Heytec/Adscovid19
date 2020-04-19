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
         <h><cite>Credits : Africa Data School Team,Johns Hopkins,Covid19API-Kyle Redelinghuys,Daily Nation and Ushahidi</cite></h>
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


                        html.Div(

                            [
                             html.Iframe(src='https://public.flourish.studio/visualisation/1603849/embed?auto=1',
                                         width=300, height=400,style={
                            "border":"0",
                            "framebolder":'0'

                        })],

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

                    [  html.Label("Ministry of Health Kenya • Last Updated"),
                        html.Iframe(src='https://public.flourish.studio/visualisation/1603849/embed?auto=1',width=300,height=400,style={
                            "border":"0",
                            "framebolder":'0'

                        })],
                    className="pretty_container three columns",
                ),
                html.Div(
                    [ html.Label("The map shows the county of residence of persons that have tested positive"),
                        html.Iframe(src='https://public.flourish.studio/visualisation/1603839/embed?auto=1',width=400,height=400,style={
                            "border":"0",
                            "framebolder":'0'

                        })],
                    className="pretty_container four columns",
                ),

                html.Div(
                    [
                     html.Iframe(src='https://kenyacovid19.ushahidi.io/views/data', width=400,
                                 height=400,style={
                            "border":"0",
                            "framebolder":'0'

                        })],
                    className="pretty_container four columns",
                ),

                html.Div(
                    [   html.Label("East Africa  ( Via Daily Nation)"),
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




    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)





# active days ..........................................
"""
@app.callback(
    Output("active", "children"), [
        Input("kenya", "value"),

    ],)
def update_well_text(well_statuses):
    url = 'https://api.covid19api.com/total/dayone/country/kenya/status/confirmed'

    #url = 'https://api.covid19api.com/country/kenya'
    df = readjsontodataframe(url)

    return df.shape[0]
"""

#confirmed ......................................
@app.callback(
    Output("confirmed", "children"), [
        Input("kenya", "value"),

    ],)
def update_well_text(well_statuses):
    #url = 'https://api.covid19api.com/total/dayone/country/kenya/status/confirmed'
    url = 'https://api.covid19api.com/country/kenya'

    #url = 'https://api.covid19api.com/country/kenya'
    df = readjsontodataframe(url)
    # confirmed last no
    Confirmedlastrow = df.tail(1)
    Confirmedno = Confirmedlastrow['Confirmed'].values[0]
    return #Confirmedno

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
    return  #revoverdno

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
    return  #Deathsno












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







# Add the server clause:
if __name__ == '__main__':
    app.run_server()


