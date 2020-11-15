import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import math


import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import joblib

from app import app


################ Loading the models

modelocalle13_In = joblib.load('data/modelocalle13_In.pkl')
modelocalle13_Out = joblib.load('data/modelocalle13_Out.pkl')
modelocalle13_Out = joblib.load('data/modelocalle13_Out.pkl')
modelocalle80_Out = joblib.load('data/modelocalle80_Out.pkl')

################ Loading avg speed for plot

df_avg_vel_model = pd.read_csv('data/avg_speed_modelplot.csv')


################ Loading setting percentage for estimation
setting_pctg = pd.read_csv('data/df_pctge_promedio_camiones_hora_dia_calle_tramo.csv')

###################################
###################################

colors = {'background': '#111111','text': '#E2E2E2'}


### import the panel links

from apps import panel_links

######### Page 5: Model

page_5_layout = html.Div(className="content",
                
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
                html.H1('ESTIMATIONS',style={'textAlign': 'center'},),
                html.H2('Number of freight vehicles by setting',style={'textAlign': 'center'},),
                ]),
        html.Div(className="content",children=[
                html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Filter by average speed (km/h)",
                            className="control_label",
                        ),
                        dcc.Slider(
                            id="speed_slider",
                            step = 1,
                            value = 20,
                            className="dcc_control",
                        ),
                        html.Br(),
                        html.P("Select corridor:", className="control_label"),
                        
                        dcc.RadioItems(
                            id="slct_corridor",
                            options=[
                                {"label": "Calle 13", "value": "CL13"},
                                {"label": "Calle 80", "value": "CL80"},
                                ],
                            value="CL13",
                            labelStyle={"display": "inline-block", "padding-left":"10px"},
                            className="dcc_control",
                        ),
                        
                        html.Br(),
                        html.P("Select traffic orientation:", className="control_label"),
                        dcc.RadioItems(
                            id="slct_direction",
                            options=[
                                {"label": " West to East (In) ", "value": "In"},
                                {"label": " East to West (Out) ", "value": "Out"},
                                ],
                            value="In",
                            labelStyle={"display": "inline-block", "padding-left":"10px"},
                            className="dcc_control",
                        ),
                        html.Br(),
                        dbc.Row([
                            dbc.Col(html.P("Month"), width = 3),
                            dbc.Col(dcc.Dropdown(
                                id="month",
                                options=[
                                    {"label": "January", "value": "1"},
                                    {"label": "February", "value": "2"},
                                    {"label": "March", "value": "3"},
                                    {"label": "April", "value": "4"},
                                    {"label": "May", "value": "5"},
                                    {"label": "June", "value": "6"},
                                    {"label": "July", "value": "7"},
                                    {"label": "August", "value": "8"},
                                    {"label": "September", "value": "9"},
                                    {"label": "October", "value": "10"},
                                    {"label": "November", "value": "11"},
                                    {"label": "December", "value": "12"},
                                ],
                                multi=False,
                                value="1",
                                className="dcc_control"
                                        ))
                            ]),
                        dbc.Row([
                            dbc.Col(html.P("Weekday"), width = 3),
                            dbc.Col(dcc.Dropdown(
                            id="weekday",
                            options=[
                                {"label": "Monday", "value": "Monday"},
                                {"label": "Tuesday", "value": "Tuesday"},
                                {"label": "Wednesday", "value": "Wednesday"},
                                {"label": "Thursday", "value": "Thursday"},
                                {"label": "Friday", "value": "Friday"},
                                {"label": "Saturday", "value": "Saturday"},
                                {"label": "Sunday", "value": "Sunday"},
                            ],
                            multi=False,
                            value="Monday",
                            className="dcc_control",
                                    ))
                            ]),
                        dbc.Row([
                            dbc.Col(html.P("Hour"), width = 3),
                            dbc.Col(dcc.Dropdown(
                            id="hour",
                            options=[
                                {"label": "00-01", "value": "0"},
                                {"label": "01-02", "value": "1"},
                                {"label": "02-03", "value": "2"},
                                {"label": "03-04", "value": "3"},
                                {"label": "04-05", "value": "4"},
                                {"label": "05-06", "value": "5"},
                                {"label": "06-07", "value": "6"},
                                {"label": "07-08", "value": "7"},
                                {"label": "08-09", "value": "8"},
                                {"label": "09-10", "value": "9"},
                                {"label": "10-11", "value": "10"},
                                {"label": "11-12", "value": "11"},
                                {"label": "12-13", "value": "12"},
                                {"label": "13-14", "value": "13"},
                                {"label": "14-15", "value": "14"},
                                {"label": "15-16", "value": "15"},
                                {"label": "16-17", "value": "16"},
                                {"label": "17-18", "value": "17"},
                                {"label": "18-19", "value": "18"},
                                {"label": "19-20", "value": "19"},
                                {"label": "20-21", "value": "20"},
                                {"label": "21-22", "value": "21"},
                                {"label": "22-23", "value": "22"},
                                {"label": "23-24", "value": "23"},
                            ],
                            multi=False,
                            value="7",
                            className="dcc_control",
                             ))
                            ]),
                        html.Br(),
                        
                        html.Br(),
                        html.Button('RUN', id='run-val', n_clicks=0, className = "button button-two", style = {"justify":"center"}),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options", style= {"margin-left":"15px"}
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H1(id="equivalent_text", style={"textAlign": "center"}), html.P("Equivalent Vehicles", style={"textAlign": "center"})],
                                    id="equivalent",
                                    className="mini_container", style={'width': '22%', 'display': 'none'}
                                ),
                                html.Div(
                                    [html.H1(id="c2gText", style={"textAlign": "center"} ), html.P("C2G Vehicles", style={"textAlign": "center"})],
                                    id="c2g",
                                    className="mini_container",style={'width': '30.5%', 'display': 'inline-block'}
                                ),
                                html.Div(
                                    [html.H1(id="c2pText", style={"textAlign": "center"}), html.P("C2P Vehicles", style={"textAlign": "center"})],
                                    id="c2p",
                                    className="mini_container",style={'width': '30.5%', 'display': 'inline-block'}
                                ),
                                html.Div(
                                    [html.H1(id="TrucksText", style={"textAlign": "center"}), html.P("Trucks", style={"textAlign": "center"})],
                                    id="trucks",
                                    className="mini_container",style={'width': '30.5%', 'display': 'inline-block'}
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                            style = {"justify":"center"}
                        ),
                        html.Div(
                            [dcc.Graph(id="model_graph", figure={})],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        )], style = {"margin-left": "35px",  # style of the container of the two squares
                    "width":"100%", 
                    "margin-top": "15px", 
                    "margin-bottom": "15px", 
                    "background": "rgba(0, 0, 0, 0)"} )
    ])    
])



########## Callback speed slider values and graph of average speed


@app.callback(
    [Output(component_id='model_graph', component_property='figure'),
    Output('speed_slider', 'min'),
    Output('speed_slider', 'max'),
    Output('speed_slider', 'marks'),],
    
    [Input(component_id='slct_corridor', component_property='value'),
     Input(component_id='slct_direction', component_property='value'),
     Input(component_id='hour', component_property='value'),]
    )

def avg_speed_plot(corridor,direction,hour):
  if direction == 'In':
    direction = 'west_east'
  else:
    direction = 'east_west'
  hour = int(hour)
  df_plot = df_avg_vel_model[(df_avg_vel_model['name_from'] == corridor) & (df_avg_vel_model['orientation'] == direction)].drop(['name_from','orientation'],axis = 1)
  df_plot = df_plot.groupby(['month','hour']).mean().reset_index()
  df_plot['color'] = 0
  df_plot['color'] = df_plot['color'].where(df_plot['hour'] == hour,1)
  df_plot['size'] = 2
  df_vel = df_plot.groupby(['month','hour']).mean().reset_index()
  vel_min = math.floor(df_vel[df_vel['hour'] == hour]['average_speed'].min())
  vel_max = math.ceil(df_vel[df_vel['hour'] == hour]['average_speed'].max())
  
  mark_points = {x: str(x) for x in range(vel_min,vel_max+1,1)}
  
  fig_model = px.scatter(df_plot, x="hour",
                   y="average_speed",
                   size = 'size',
                   size_max = 4,
                   color = 'color',
                   color_continuous_scale=px.colors.sequential.Bluered_r,
                   title = 'Average speed by hour',
                   labels = { 'average_speed': 'Average speed [km/h]',
                       'hour': 'Hour'},
                   )
  fig_model.update_layout(font_family = 'Times New Roman',
                  title = {'x':0.5},xaxis = dict(tickmode = 'linear',
                               tick0 = 0,
                               dtick = 1))
  fig_model.update_layout({
  'plot_bgcolor': 'rgba(0, 0, 2, 0)',
  'paper_bgcolor': 'rgba(0, 0, 2, 0)',
  })
  fig_model.update(layout_coloraxis_showscale=False)
  fig_model.update_xaxes(showgrid=False, zeroline=False)
  fig_model.update_yaxes(showgrid=False)
  return fig_model,vel_min,vel_max,mark_points



@app.callback(
    Output(component_id='equivalent_text', component_property='children'),
    
    [Input(component_id='run-val', component_property='n_clicks'),
    Input(component_id='speed_slider', component_property='value'),
     Input(component_id='slct_corridor', component_property='value'),
     Input(component_id='slct_direction', component_property='value'),
     Input(component_id='month', component_property='value'),
     Input(component_id='hour', component_property='value'),
     Input(component_id='weekday', component_property='value'),
     ]
)

def estimate(n,speed,corridor,direction,month,hour,weekday):
  
  changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
  
  if "run-val" in changed_id:
      if direction == 'In':
        direction1 = 'west_east'
      else:
        direction1 = 'east_west'
      hour1 = int(hour)
      if corridor == 'CL13':
        corridor = 'CL13'
      else:
        corridor = 'CL80'

      df_avg_vel = df_avg_vel_model[(df_avg_vel_model['name_from'] == corridor) & (df_avg_vel_model['orientation'] == direction1)].drop(['name_from','orientation'],axis = 1)
      df_avg_vel = df_avg_vel.groupby(['month','hour']).mean().reset_index()

      vel_mean = df_avg_vel[df_avg_vel['hour'] == hour1]['average_speed'].mean()
      vel_std = df_avg_vel[df_avg_vel['hour'] == hour1]['average_speed'].std()

      if corridor == 'CL13':
        corridor = 'calle13'
      else:
        corridor = 'calle80'
      
      
      
      
      modelname = 'data/modelo' + corridor + '_'  + direction + '.pkl'
      model = joblib.load(modelname)

      names = model.get_booster().feature_names
      input = np.zeros([len(names)])
      zip_iterator = zip(names, input)
      dict_2predict = dict(zip_iterator)

      dict_2predict['average_speed_total'] = abs(speed - vel_mean) / vel_std
      dict_2predict['average_speed_tramo'] = abs(speed - vel_mean) / vel_std
      hour_ = 'hour_' + hour 
      dict_2predict[hour_] = 1

      month_ = 'month_' + month 
      dict_2predict[month_] = 1

      weekday_ = 'weekday_' + weekday 
      dict_2predict[weekday_] = 1

      estimation = pd.DataFrame(dict_2predict, index =  ['value'])
      estimated = (model.predict(estimation[names].iloc[[-1]]))[0]
      estimated = int(estimated.round())
      
  else:
      estimated = "0"
    
  return str(estimated)


@app.callback(
    Output(component_id='c2gText', component_property='children'),
    Output(component_id='c2pText', component_property='children'),
    Output(component_id='TrucksText', component_property='children'),
    
    [Input('equivalent_text', 'children'),
     Input(component_id='slct_corridor', component_property='value'),
     Input(component_id='slct_direction', component_property='value'),
     Input(component_id='month', component_property='value'),
     Input(component_id='hour', component_property='value'),
     Input(component_id='weekday', component_property='value'),]
)

def setting_estimation(estimated,corridor,direction,month,hour,weekday):
  estimated = int(estimated)
  if estimated is None:
        estimated = 10
  if corridor == 'CLL13':
    corridor = 'CL13'
  else:
    corridor = 'CL80'
  if direction == 'In':
    direction = 0
  else:
    direction = 1
  hour = int(hour)
  month = int(month)
  setting_corr_dir = setting_pctg[(setting_pctg['corridor'] == corridor) & (setting_pctg['direction'] == direction)]
  setting_date = setting_corr_dir[(setting_corr_dir['month'] == month) & (setting_corr_dir['weekday'] == weekday) & (setting_corr_dir['hour'] == hour)]
  setting_estimation = (setting_date[['pctge_c2g_mean','pctge_c2p_mean','pctge_tractocamiones_mean']] * estimated / 100).T
  setting_estimation.columns = ['percentage']
  camiones = setting_estimation['percentage'].tolist()
  camiones = [round(num) for num in camiones]
  c2g = camiones[0]
  c2p = camiones[1]
  tracto = camiones[2]
  return c2g,c2p,tracto


#@app.callback(
#    Output(component_id='c2gText', component_property='style'),
    
#    Input('run-val', 'n_clicks'))

