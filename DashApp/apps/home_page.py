import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

from app import app
from apps import panel_links


colors = {'background': '#111111','text': '#E2E2E2'}


desc_1 = "Cities face challenges to guarantee citizens’ quality of life, economic development, efficient public transport, and a sustainable environment. In this scenario, the Freight transportation impact on cities mobility and is a topic of major concern for both policy makers and private companies."

desc_2 = "In the city of Bogotá, freight transport generates around 44% of the total emissions of the city – the Latin American capital city with the worst air quality according to IQAir (2020)–, and represents between 17% and 25% of the city vehicle flows."

desc_3 = "The aim of the project is to estimate the number of freight vehicles that flow in a specific road based on the available data that SDM has and the inference as well as machine learning models that will forecast future flows. This input will help SDM to evaluate traffic policies, environmental impacts and save public budget spent on fieldworks for vehicle counting."

#### Graph home

dpto_transport = pd.read_csv(r'data/dpto_transport.csv')


fig_home = px.scatter_mapbox(dpto_transport, 
                        lat="lat", lon="lon",
                        animation_frame = 'Department', 
                        animation_group = 'City', 
                        color="Department", size="size_dot",
                        size_max=50, 
                        hover_data = ['City','Department','lat','lon'],
                        opacity=0.5,
                        category_orders=dict(Department=['ANTQ.', 'CHOCO', 'BOLV.', 'CALDAS', 'CESAR','ATLN.', 'CORD.', 'RISAR.', 'CUND.', 'GUAJ.','MAGD.', 'SUCRE','ALL' ])
                        )
fig_home.update_layout(showlegend=True,
                  margin ={'l':0,'t':0,'b':0,'r':0},
                  mapbox = {
                      'center': {'lon': -74.12, 'lat': 8.3},
                      'style': "carto-positron",
                      'zoom': 4.9}
                        )




index_page = html.Div(className="content",
            children=[

html.Div(
    className="left_menu",
    style={
            'background-image': 'url("/assets/left_panel.jpg")',
            'background-repeat': 'no-repeat',
            'background-position': 'top',
            },
    children = panel_links.panel_links    #### links in the the left panel
    
),
    
    
html.Div(
    className="right_content",
    children=[
        html.Div(

            className="top_metrics",
            children=[
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.H1(children='SmartFlow',
                        style={
                                'textAlign': 'center',
                               }
           ),
                
    html.H3(
        children='Urban Freight transport',
                style={
                        'textAlign': 'center',
                        
                        }
            ),
                       ]
                ),

            html.Br(),
            html.Br(),
            html.Br(),        
            dbc.Row([
                    dbc.Col(html.P(desc_1 + desc_2 + desc_3,style={"margin-left": "15px",'color':'#7F90AC'},
                           ), width = 4
                           ),
                    dbc.Col(dcc.Graph(id='map_home', figure=fig_home),width = 8),

                    ]),
            html.Br(),
            html.Br(),         
            dbc.Row([html.Img(src='assets/logos.png')],style={'textAlign': 'center'}),
        
                ])
  
])
