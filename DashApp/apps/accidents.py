import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import requests
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
from app import app
from sqlalchemy import create_engine
import psycopg2

host = 'team73test.c4xr0dadx0gz.us-east-2.rds.amazonaws.com'
port = 5432
user = 'postgres'
password = 'ds4a_t73'
database = 'postgres'
connDB = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
conn = connDB.raw_connection()
cur = conn.cursor()

################ Loading accidents data from postgres

td_acc_sql = '''Select * from public.accidentes_13_80'''
db_acc = pd.read_sql(td_acc_sql, connDB)

###################################
###################################

colors = {'background': '#111111','text': '#E2E2E2'}


### import the panel links

from apps import panel_links

########## Page 3: Accident rate

page_3_layout = html.Div(className="content",
            children=[

html.Div(
    className="left_menu",
    
    children = panel_links.panel_links    #### links in the the left panel
),
    
    
html.Div(
    className="right_content",
    children=[
        html.Div(
            className="top_metrics",
            children=[
                html.H1(children='Accident rate',
                        style={
            'textAlign': 'center',
            'color': "#73879c"}
           ),
                
    html.H2(
        children='Main corridors',
        style={
            'textAlign': 'center',
            'color': "#1abb9c"
        }
    ),
                dcc.Dropdown(id="slct_corr",
                 options=[
                     {"label": "Calle 13", "value": "Calle 13"},
                     {"label": "Calle 80", "value": "Calle 80"}],
                 multi=False,
                 value="Calle 13",
                 style={'width': "40%"}
                 ),
            ]
        ),
        dcc.Dropdown(id="slct_clas",
                 options=[{'label':x, 'value':x} for x in db_acc['clase'].unique().tolist()],
                 multi=False,
                 value=db_acc['clase'].unique().tolist()[0],
                 style={'width': "40%"}
                 ),
            
        
        html.Div(
            
        ),
        dbc.Row([
        dbc.Col([dcc.Graph(id='graph_1A', figure={}),]),
        dbc.Col([dcc.Graph(id='graph_2B', figure={}),]),       
    ]),
    ])    
  
])

########## Callback dropdown corridor and direction of the traffic
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='graph_1A', component_property='figure'),
    Output(component_id='graph_2B', component_property='figure')],
    [Input(component_id='slct_corr', component_property='value'),
    Input(component_id='slct_clas', component_property='value')]
)
def update_graph(option_slctd, option_direction):
    
    dff1 = db_acc.copy()
    dff1 = dff1[dff1["corredor"] == option_slctd]
    dff1 = dff1[dff1["clase"] == option_direction]
    

    # Plotly Express
    per_sin = dff1[['year','month','codigo_siniestro']].groupby(['year','month']).count().reset_index()
    fig = px.bar(per_sin, x="year", y="codigo_siniestro", animation_frame="month", animation_group="year",color="codigo_siniestro",color_continuous_scale=px.colors.sequential.Darkmint,title='Accidents per Year')
    

    per_sin_hour = dff1[['month','hour','codigo_siniestro']].groupby(['month','hour']).count().reset_index()
    fig2 = px.bar(per_sin_hour, x="hour", y="codigo_siniestro", animation_frame="month", animation_group="hour",color="codigo_siniestro",color_continuous_scale=px.colors.sequential.Emrld,title='Accidents per Hour')
    
    
    return fig, fig2
