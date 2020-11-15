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

from apps import home_page, panel_links, cll_13, cll_80, model

server = app.server


colors = {'background': '#111111','text': '#E2E2E2'}
    



##### Menu Page

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])



                       

################ Update the pages (doing the links functionables)


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/calle-13':
        return cll_13.layout
    elif pathname == '/calle-80':
        return cll_80.layout
    elif pathname == '/model':
        return model.page_5_layout
    else:
        return home_page.index_page
    # You could also return a 404 "URL not found" page here



    
#Initiate the server where the app will work
if __name__ == "__main__":
    app.run_server(host='0.0.0.0',port='8050',debug=True, use_reloader=True)
    
