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
from sqlalchemy import create_engine
import psycopg2

from app import app


#### Credentials for postgres ###############

host = 'team73test.c4xr0dadx0gz.us-east-2.rds.amazonaws.com'
port = 5432
user = 'postgres'
password = 'ds4a_t73'
database = 'postgres'
#connDB = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
#conn = connDB.raw_connection()
#cur = conn.cursor()
##########################




################ Loading the bitcarrier data
#temp_speed_hour = '''Select * from public.avg_speed_weekday_dash'''
avg_speed_weekday = pd.read_csv(r"data/avg_speed_weekday.csv")                         #pd.read_sql(temp_speed_hour, connDB)

avg_speed_weekday = avg_speed_weekday[avg_speed_weekday["name_from"] == "CL13"]
###################################


################ Loading the map speed data
#temp_df_map = '''Select * from public.df_map_speed_dash'''
#df_map_speed = pd.read_sql(temp_df_map, connDB)
df_map_speed = pd.read_csv(r"data/df_map_speed.csv")


df_map_speed_ew = df_map_speed[(df_map_speed["corridor"] == "cll13") & (df_map_speed["orientation"] == "east_west")]
df_map_speed_we = df_map_speed[(df_map_speed["corridor"] == "cll13") & (df_map_speed["orientation"] == "west_east")]


map_speed_ew = go.Figure()

for i in range(df_map_speed_ew.shape[0]):
    lat1 = df_map_speed_ew[['tramo_from_lat','tramo_to_lat']].iloc[i].to_numpy()
    long1 = df_map_speed_ew[['tramo_from_long','tramo_to_long']].iloc[i].to_numpy()
    line_color = df_map_speed_ew['color'].iloc[i]
    
    map_speed_ew.add_trace(go.Scattermapbox(
    mode = "markers+lines",
    lon = long1,
    lat = lat1,
    line=dict(width=10, color= line_color),
    marker=dict(
            size=4,
            showscale=True,
            colorscale='rdylgn',
            cmin=20,
            cmax=50)))#,
      #marker = {'size': 10}))

map_speed_ew.update_layout(
    title = "dsafsf",
    showlegend=False,
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'center': {'lon': -74.12, 'lat': 4.65},
        'style': "stamen-terrain",
        'zoom': 11.5})


map_speed_we = go.Figure()

for i in range(df_map_speed_we.shape[0]):
    lat1 = df_map_speed_we[['tramo_from_lat','tramo_to_lat']].iloc[i].to_numpy()
    long1 = df_map_speed_we[['tramo_from_long','tramo_to_long']].iloc[i].to_numpy()
    line_color = df_map_speed_we['color'].iloc[i]
    
    map_speed_we.add_trace(go.Scattermapbox(
    mode = "markers+lines",
    lon = long1,
    lat = lat1,
    line=dict(width=10, color= line_color),
    marker=dict(
            size=4,
            showscale=True,
            colorscale='rdylgn',
            cmin=20,
            cmax=50)))#,
      #marker = {'size': 10}))

map_speed_we.update_layout(showlegend=False,
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'center': {'lon': -74.12, 'lat': 4.65},
        'style': "stamen-terrain",
        'zoom': 11.5})

#################################




################ Loading the RNCD data 
#temp_orig_dest = '''Select * from public.origin_destin_dash'''
#origin_destin = pd.read_sql(temp_orig_dest, connDB)
df_product = pd.read_csv(r'data/product.csv', encoding = "latin-1")
df_product = df_product[df_product["corridor"] == "CALLE 13"]

df_product_setting = pd.read_csv(r'data/product_setting.csv')
df_product_setting = df_product_setting[df_product_setting["corridor"] == "CALLE 13"]

df_setting_grouped = pd.read_csv(r'data/setting_grouped.csv')
df_setting_grouped = df_setting_grouped[df_setting_grouped["corridor"] == "CALLE 13"]


# graph number of cargo vehicles by category of the product and direction of the traffic
fig_category_in_out = px.bar(df_product, 
             x="Commodity category", 
             y="Number of travels transported", 
             title = 'Number of travels transported by commodity',
             barmode='group',
             color="Bogotá",
             color_discrete_map = {' Out':'rgb(158,202,225)',
                                   ' In':'rgb(8,81,156)'})
fig_category_in_out.update_layout(font_family = 'Times New Roman',
                  title = {'x':0.5})



# graph number of cargo vehicles by category of the product and type of vehicle

fig_product_setting = px.bar(df_product_setting, 
             x="Commodity category", 
             y="Number of travels transported", 
             title = 'Number of travels transported by commodity',
             barmode='group',
             color="Setting",
             color_discrete_map = {'C2P':'rgb(158,202,225)',
                                   'C2G':'rgb(8,81,156)',
                                   'TRACTOCAMIONES':'rgb(66,146,198)'})
fig_product_setting.update_layout(font_family = 'Times New Roman',
                  title = {'x':0.5})


# graph number of cargo vehicles by setting

fig_setting_grouped = px.bar(df_setting_grouped, 
             x="Setting", 
             y="Number of travels", 
             title = 'Number of travels by setting of the freigh vehicle',
             color_discrete_sequence= ['rgb(158,202,225)'],
             text = 'Number of travels'
)
fig_setting_grouped.update_traces(texttemplate = '%{text:,}',
     textposition = 'outside')
fig_setting_grouped.update_layout(font_family = 'Times New Roman',
                  title = {'x':0.5})
fig_setting_grouped.update_yaxes(range=[0, 5e5])
fig_setting_grouped.show()



################ Loading Accidents data 


# Loading accidents data from postgres

#td_acc_sql = '''Select * from public.accidentes_13_80'''
#db_acc = pd.read_sql(td_acc_sql, connDB)
db_acc = pd.read_csv(r'data/db_acc.csv', encoding = "latin-1")

db_acc = db_acc[db_acc["corredor"] == "Calle 13"]
###################################



colors = {'background': '#111111','text': '#E2E2E2'}


### import the panel links

from apps import panel_links















#### Layout #######
########## Page 1: Speed average - Bitcarrier info                       

layout = html.Div(className="content",
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
                    html.Div(className="top_metrics",
                                    children=[
                                            html.Br([]),
                                            html.H1(children='CALLE 13 AVENUE',
                                                            style={
                                                                   'textAlign': 'center',
                                                                    }
                                                   ),
 
                                            html.H2(children='2019',
                                                            style={
                                                                'textAlign': 'center',
                                                                   }
                                                    ),
                                                ]
                               ),
        
            
        
        html.Div(
            
        ),
        
        html.Div(className="content",children=[                       
               
        html.H3('Average speed of the corridor', id = "avg_speed"),
        html.P("This avenue has 13 speed sensors throughout its 7.5 km of distance. The sensors allow to estimate the speed for the 13 segments that componse the corridor. Its important to notice that each direction of the avenue has an independent behavior of the other. The following maps illustrate the average speed of the year for each segment.", style={'color':'#7F90AC'}),
        
        html.Br(),
        dbc.Row([
                dbc.Col([html.P('Speed average west to east direction', style = {"textAlign": "center"}),
                         dcc.Graph(id='speed_we_cll13', figure=map_speed_we)]),

                dbc.Col([html.P('Speed average east to west direction', style = {"textAlign": "center"}),
                         dcc.Graph(id='speed_ew_cll13', figure=map_speed_ew),]),       
                ]),
        
        html.Br(),
        html.Br(),

        dbc.Row([
                dbc.Col(dcc.Dropdown(id="slct_direction",
                                     options=[
                                         {"label": "East to west", "value": "east_west"},
                                         {"label": "West to east", "value": "west_east"}],
                                     multi=False,
                                     value="east_west",
                                     #style={'width': "40%"}
                                         ), 
                        width = 2),
        
                dbc.Col(dcc.Dropdown(id="slct_section",
                                     options=[],
                                     multi=False,
                                     value=[],
                                     #style={'width': "50%"}
                                     ),
                        width = 4),
                ], justify = "center"
                ),
        
            
            
        html.Br(),
        html.Br(),
            
            
            
        dbc.Row([
        dbc.Col([dcc.Graph(id='speed_day', figure={})],width = 8),

        dbc.Col(html.P(
                       "The behavior of the average speed of the corridor has a small variability over the day of the week. It is possible to notice that for every month of the year the speed is higher on Sundays. Regarding to every hour, there is a pattern for every month in which the average speed decreases in the day and increases at night. There are restrictions for freight vehicles that have more than 20 years of antiquity. The schedules for this restriction is between 5:30 am and 8:00 am, and between 4:30 pm and  7:00 pm.",style={'color':'#7F90AC'}), width = 3),       
                ]),  
            
         html.Br(),
         html.Br(),
            
            
         dbc.Row([
         dbc.Col([dcc.Graph(id='speed_hour', figure={})]),     
                ]),  
            
            
            
            
        html.Br(),
        html.Br(),
            
            
            
        
        html.H3('Detailed Freigh Registry', id="cargo"),
        
        html.Br(),
        html.Br(),
            
        dbc.Row([
            dbc.Col(html.P("It is important to identify which departments in the country send and received freight from Bogotá since this information will let to identify which corridors are used and could be impacted by the freight vehicles. The following maps could be filtered by month of the year and by type of freight to show the number of cargo vehicles that circulate entering and leaving the city",style={'color':'#7F90AC'},
                           ), width = 4
                   ),
            dbc.Col([dcc.Graph(id='destination_rncd_cl13', figure = fig_category_in_out),
                    ],width = 7
                   ),       
                ]),
        dbc.Row([
                    dbc.Col([dcc.Graph(id='origin_rncd_cl13', figure = fig_product_setting),], width = 7),
                    dbc.Col([dcc.Graph(id='destination_rncd_cl13', figure = fig_setting_grouped),], width = 5),       
                ]),

            
            
        html.Br(),    
        html.Br(),
        html.H3('Accident rate', id = "accident_rate"),
        html.P(["Different elements affect the mobility of the city, the accident rate is one the most important because of the immediate impact of the speed in the corridor. In the prediction section, there is a model that evaluates whether an accident has more impact on mobility or not, when freight vehicles are involved. Also, it is important to notice the historical of the number of accidents in the corridor, which has approximately a decreasing behavior. Finally, the behavior of accidents per hour seems to be inverse of the behavior of the average speed, which is expected for the vehicle density over the day."], style={'color':'#7F90AC'} ),
        
        dbc.Row([
                dbc.Col(dcc.Dropdown(id="slct_clas",
                                     options=[{'label':x, 'value':x} for x in db_acc['clase'].unique().tolist()],
                                     multi=False,
                                     value=db_acc['clase'].unique().tolist()[0],
                                     #style={'width': "60%"}
                                     ),
                        width = 2
                        ),

                dbc.Col(dcc.Dropdown(id="freight_s_n",
                                     options=[{'label':"Cargo vehicle involved", 'value':1},
                                              {'label':"Other vehicles", 'value':0}
                                             ],
                                     multi = False,
                                     value = 0,
                                     #style = {'width': "60%"}
                                     ),
                        width = 2
                        ),
                     ],
                justify="center",
               ), 
            
            
        dbc.Row([
        dbc.Col([dcc.Graph(id='graph_1A', figure={}),]),
        dbc.Col([dcc.Graph(id='graph_2B', figure={}),]),
                ]),
        
                    
            
        ], style = {"margin-left": "15px",  # style of the container of the all graphs
                    "width":"97%", 
                    "margin-top": "15px", 
                    "margin-bottom": "15px", 
                    "background": "rgba(0, 0, 0, 0)"} )
    ])    
  
])



####### Callback dropdow orientation affecting road section dropdown
@app.callback(
    [Output(component_id='slct_section', component_property='options'),
    Output(component_id='slct_section', component_property='value')],
    
    Input(component_id='slct_direction', component_property='value')
              )

def dropdown_section(option_direction):
    
    road_df = avg_speed_weekday[avg_speed_weekday["orientation"] == option_direction]
    
    road_options = [{'label':x, 'value':x} for x in road_df['name_to'].unique().tolist()]
    first_value=road_df['name_to'].unique().tolist()[0]
    
    return road_options, first_value



########## Callback dropdown road section and direction of the traffic

color1 = ['#3798BE', '#3798BE', '#3798BE', '#3798BE', '#3798BE', '#3798BE',
       '#F6E20E', '#F6E20E', '#3798BE', '#3798BE', '#3798BE', '#3798BE',
       '#3798BE', '#3798BE', '#3798BE', '#3798BE', '#3798BE', '#F6E20E',
       '#F6E20E', '#F6E20E', '#767C7F', '#3798BE', '#3798BE', '#3798BE',
       '#3798BE', '#3798BE']


@app.callback(
    [Output(component_id='speed_day', component_property='figure'),
    Output(component_id='speed_hour', component_property='figure')],
    
    [Input(component_id='slct_direction', component_property='value'),
    Input(component_id='slct_section', component_property='value')]
)
def speed_graph(option_direction, option_section):
    
    dff = avg_speed_weekday.copy()
    dff = dff[dff["orientation"] == option_direction]
    dff = dff[dff["name_to"] == option_section]
    
    days_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    

    # Figure avg speed by day of the week
    avg_weekday = dff[['month','average_speed','weekday']].groupby(['month','weekday']).mean().reset_index()
    fig = px.bar(avg_weekday, 
             x="weekday", 
             y="average_speed", 
             animation_frame="month", 
             animation_group="weekday",
             color_discrete_sequence= ['rgb(158,202,225)'],
             text = 'average_speed',
             category_orders=dict(weekday=days_order),
             title = 'Average speed by weekday',
             labels = { 'average_speed': 'Average speed [km/h]',
                       'weekday': 'Weekday'})
    fig.update_traces(texttemplate = '%{text:.1f} km/h', 
                      textposition = 'outside')
    fig.update_layout(font_family = 'Times New Roman',
                      title = {'x':0.5})
    fig['layout'].pop("updatemenus")
    fig.update_yaxes(range=[0, 45])

    
    
    # Figure avg speed by hour of the day
    avg_speed_hour = dff.groupby(['month','hour','orientation','Restriction']).mean().reset_index()
    
    fig2 = px.bar(avg_speed_hour, 
             x="hour", y="average_speed", 
             animation_frame="month", 
             animation_group="hour", 
             title = 'Average speed by hour',
             color = 'Restriction', 
             color_discrete_map = {' No':'rgb(158,202,225)',
                                   ' Yes':'rgb(8,48,107)'},
             text = 'average_speed',
             labels = {'average_speed': 'Average speed [km/h]',
                       'hour': 'Hour'})      
    fig2["layout"].pop("updatemenus") # optional, drop animation buttons
    fig2.update_layout(font_family = 'Times New Roman',
                      title = {'x':0.5})
    fig2.update_traces(texttemplate = '%{text:.1f}', 
                      textposition = 'outside')
    fig2.update_yaxes(range=[0, 60])
    fig2.update_layout(xaxis = dict(tickmode = 'linear',
                               tick0 = 0,
                               dtick = 1))
    
    
    return fig, fig2



                
########## Callback accident rate

@app.callback(
    [Output(component_id='graph_1A', component_property='figure'),
    Output(component_id='graph_2B', component_property='figure')],
    
    [Input(component_id='slct_clas', component_property='value'),
     Input(component_id='freight_s_n', component_property='value'),]
    

)
def update_graph(class_slctd, freight_involved):

    
    dff3 = db_acc.copy()
    dff3 = dff3[dff3["clase"] == class_slctd]
    dff3 = dff3[dff3["carga_S/N"] == freight_involved]
    tem_acc = dff3[dff3["year"] == 2019]

    

    # Plotly Express
    per_sin = dff3[['year','codigo_siniestro']].groupby('year').count().reset_index()
    fig5 = px.bar(per_sin, x="year", y="codigo_siniestro",
             color_discrete_sequence= ['rgb(158,202,225)'] ,
             text = 'codigo_siniestro',
             labels = { 'codigo_siniestro': 'Number of accidents',
                       'year': 'Year'})
    fig5.update_traces( textposition = 'outside')
    fig5.update_layout(font_family = 'Times New Roman',
                  title = {'text':'Number of reported accidents per year',
                           'x':0.5})
    
    

    per_sin_hour = tem_acc[['hour','codigo_siniestro']].groupby('hour').count().reset_index()
    fig6 = px.bar(per_sin_hour, 
              x="hour", 
              y="codigo_siniestro", 
              text = 'codigo_siniestro',
              labels = { 'codigo_siniestro': 'Number of accidents',
                       'hour': 'Hora del día'},
              color_discrete_sequence= ['rgb(158,202,225)'] )
    fig6.update_traces( textposition = 'outside')
    fig6.update_layout(font_family = 'Times New Roman',
                  title = {'text':'Number of accidents per hour - 2019',
                           'x':0.5})
    fig6.update_layout(xaxis = dict(tickmode = 'linear',
                               tick0 = 0,
                               dtick = 1))
    
    return fig5, fig6

