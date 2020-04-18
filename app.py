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


app = dash.Dash()
#server = app.server



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
mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
)

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
                                    "Kenya Covid-19 Realtime Dashboard",
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

                        html.P(
                            "Data is sourced from Johns Hopkins CSSE .  "
                            "December 2019, a local outbreak of pneumonia was detected in Wuhan (Hubei, China), and was quickly determined to be caused by a novel coronavirus,1 namely COVID-19. The outbreak has since spread to mainland China as well as 185 other countries and regions, with more than 2million confirmed cases as of Feb 17, 2020.3 In response to this ongoing public health emergency, we developed an online interactive dashboard, hosted by the Center for Research and development at Africa Data School to visualise and track  Kenya reported cases of coronavirus disease in real-time.  ",
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

                        [dcc.Graph(id="three_graph")],
                      className="pretty_container seven columns",

                ),
                html.Div(
                    [dcc.Graph(id="aggregate_graph")],
                    className="pretty_container five columns",
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
    return Confirmedno

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
    return  revoverdno

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
    return  Deathsno












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
                'title': 'Confirmed'
            },
          title='Confirmed'

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
    app.run_server(debug=False)
