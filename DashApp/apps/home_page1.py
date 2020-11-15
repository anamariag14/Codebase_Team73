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
from apps import panel_links

colors = {'background': '#111111','text': '#E2E2E2'}

index_page = html.Div(className="content",children=[
	html.Div(className="left_menu", children = panel_links.panel_links),    #### links in the the left panel
	html.Div(className="right_content",children=[
		html.Div(className="top_metrics",children=[
			html.H1(children='Traffic impact of freight vehicles',style={'textAlign': 'center','color': "#73879c"}),
			html.H3(children='Bogotá - Main corridors',style={'textAlign': 'center','color': "#73879c"})
		]),
		html.Div(className = 'container', children=[
			dbc.Row([dbc.Col([html.Br(),html.Br(),html.Button('Average speed', id='btn-nclicks-2', n_clicks=0), html.Br(),html.Br(), html.H5( "The Bitcarrier database contains information about the velocity from the majority of corredors in Bogota City")])]),
			dbc.Row([dbc.Col([html.Br(),html.Br(),html.Button('National registry', id='btn-nclicks-2', n_clicks=0), html.Br(),html.Br(), html.H5( "The National Registry of Road Freight Dispatches receives, validates and transmits the information generated at the operations fom public services of freight transport in highways")])]),
			dbc.Row([dbc.Col([html.Br(),html.Br(),html.Button('Accident rate', id='btn-nclicks-2', n_clicks=0), html.Br(),html.Br(), html.H5( "Accidents, their causes, types and type vehicles involved")])]),
		])
	])
])