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
#
colors = {'background': '#111111','text': '#E2E2E2'}

panel_links = [
         dbc.Row(html.Img(src=app.get_asset_url('team_3.png'),
                  style={
                        "height": "160px",
                        "width": "auto", "margin-top": "15px", 'align-items': 'center',
                         }
                         ),
                 justify = "center"
                ),
    
        dbc.NavLink(
                    "home", 
                    href="/home",style={"margin-left": "20px"}, 
                    className='text-uppercase btn-link btn-link:hover font-weight-bold font-bold px-2'
                    ),
        
        dbc.NavLink(
                    "Calle 13", 
                    href="/calle-13",style={"margin-left": "30px"}, 
                    className='text-uppercase btn-link font-weight-bold font-bold px-2'
                    ),
        
    dbc.Col([
                dbc.NavLink("Average Speed", href="/calle-13#avg_speed", external_link=True, className='btn-link'),
                dbc.NavLink("Freigh Registry", href="#cargo", external_link=True, className='btn-link'),
                dbc.NavLink("Accident rate", href="#accident_rate", external_link=True, className='btn-link'),
            ],style={'color': colors['text'], "margin-left": "40px"}
            ),
    
        dbc.NavLink(
                    "Calle 80", 
                    href="/calle-80",style={ "margin-left": "30px"}, 
                    className='text-uppercase btn-link font-weight-bold font-bold px-2'
                    ),
    dbc.Col([
                dbc.NavLink("Average Speed", href="/calle-80#avg_speed_80", external_link=True, className='btn-link'),
                dbc.NavLink("Freigh Registry", href="/calle-80#cargo_80", external_link=True, className='btn-link'),
                dbc.NavLink("Accident rate", href="/calle-80#accident_80", external_link=True, className='btn-link'),
            ],style={'color': colors['text'], "margin-left": "40px"}
            ),
            
        dbc.NavLink(
                    "estimations", 
                    href="/model",style={ "margin-left": "30px"}, 
                    className='text-uppercase btn-link font-weight-bold font-bold px-2'
                    ), 
    
        
        
    
#        html.Img(src=app.get_asset_url('logo-sdm.png'),style={
#                                "height": "30px",
#                                "width": "auto", "margin-bottom": "5px", "margin-left": "5px"}),
    
#        html.Img(src=app.get_asset_url('mintic.png'),style={
#                                "height": "30px",
#                                "width": "auto", "margin-bottom": "5px", "margin-left": "8px"}),
    
]    