#!/usr/bin/env python
# coding: utf-8

from plotly.offline import init_notebook_mode, iplot
from wordcloud import WordCloud, STOPWORDS
from keras.preprocessing.text import text_to_word_sequence
from tensorflow.keras.preprocessing.text import Tokenizer
import dash
import dash_core_components as dcc
import pandas as pd
from plotly import graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import dash_html_components as html

# API Keys and datasets
mapbox_access_token = 'pk.eyJ1IjoiZ29sZGVkaXRpb24yMTIiLCJhIjoiY2tld3dvMGxmMGJsbjM1bXV5cXNjam84cSJ9.32Xt4hp12-2Fa3Rk2XFLgQ'
airbnb_data = pd.read_csv("AB_NYC_2019.csv")


tokenizer = Tokenizer()
airbnb_data.name = airbnb_data.name.astype(str)
tokenizer.fit_on_texts(airbnb_data.name)
airbnb_data.name = airbnb_data.name.apply(lambda x: text_to_word_sequence(x))

def plotly_wordcloud(text):
    wc = WordCloud(stopwords=set(STOPWORDS),
                   max_words=300,
                   max_font_size=50)
    wc.generate(text)

    word_list = []
    freq_list = []
    fontsize_list = []
    position_list = []
    orientation_list = []
    color_list = []

    for (word, freq), fontsize, position, orientation, color in wc.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)

    # get the positions
    x = []
    y = []
    for i in position_list:
        x.append(i[0])
        y.append(i[1])

    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i*100)
    new_freq_list

    trace = go.Scatter(x=x*20,
                       y=y*200,
                       textfont=dict(size=new_freq_list,
                                     color=color_list),
                       hoverinfo='text',
                       hovertext=['{0}{1}'.format(
                           w, f) for w, f in zip(word_list, freq_list)],
                       mode="text",
                       text=word_list
                       )

    layout = go.Layout(autosize=True,
                       xaxis=dict(showgrid=False,
                                  showticklabels=False,
                                  zeroline=False,
                                  automargin=True),
                       yaxis=dict(showgrid=False,
                                  showticklabels=False,
                                  zeroline=False,
                                  automargin=True),
                       margin=go.layout.Margin(pad=1000),
                       )

    fig = go.Figure(data=[trace], layout=layout)

    return fig


tab = []
airbnb_data.name = airbnb_data.name.apply(lambda x: " ".join(x))
airbnb_data.name.apply(lambda x: tab.append(x))

# print(tab[0])
text = " ".join(tab)
# print(text)



wordcloud_name = plotly_wordcloud(text)


# external CSS stylesheets

app = dash.Dash(__name__)

server = app.server


# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = airbnb_data
df = df[df['price'] < 1501]

#df = df.groupby(['name', 'neighbourhood_group', 'neighbourhood', 'room_type', 'latitude', 'longitude'])[['minimum_nights']].mean()
df.reset_index(inplace=True)
print(df[:5])
min_price = min(df['price'])
max_price = max(df['price'])
med_price = df['price'].median()

min_nb_R = min(df['number_of_reviews'])
max_nb_R = max(df['number_of_reviews'])
med_nb_R = df['number_of_reviews'].median()


# ------------------------------------------------------------------------------


# App layout
app.layout = html.Div([

    html.Div([
        html.Div([
            html.H1("Airbnb Dashboard", style={'textAlign': 'center'}),
            html.Br(),

            html.Div([
                html.Div([

                    html.H4('Choose layout of the page'),
                    dcc.RadioItems(id='slct_web_mode',
                                   options=[
                                       {'label': 'dark mode', 'value': 'dark'},
                                       {'label': 'light mode', 'value': 'light'},
                                   ],
                                   value='light'
                                   ),

                    html.Br(),

                    html.H4('Choose Room Type:'),
                    dcc.Dropdown(id="slct_room_type",
                                 options=[
                                     {'label': str(item), 'value': str(item)} for item in df['room_type'].unique()],
                                 multi=True,
                                 value=list(set(df['room_type'])),
                     style={'backgroundColor': '#999999',
                         'height': 'fit-content', 'color': 'black'},
                        placeholder="Select a room type"
                    ),

                    html.Div([
                        html.H4('Enter the number of nights you want to stay :'),

                        dcc.Input(id='minimum_night',
                                  style={'backgroundColor': '#999999'},
                                  placeholder='minimum night you want to stay...',
                                  type='text',
                                  value='2'
                                  ),
                    ], style={}),

                    html.Div([
                        html.H4('Enter a key word :'),

                        dcc.Input(id='keyword',
                                  style={'backgroundColor': '#999999'},
                                  placeholder='key word...',
                                  type='text',
                                  value=' '
                                  ),
                    ], style={}),

                ]),

                html.Div([
                    html.H4('Choose Borough:'),
                    dcc.Checklist(id='slct_region',
                                  options=[
                                      {'label': str(item), 'value': str(item)} for item in df['neighbourhood_group'].unique()],
                                  # value=list(set(df['neighbourhood_group'])),
                                  value=[
                                      item for item in df['neighbourhood_group'].unique()],
                                  labelStyle={'display': 'inline-block'}
                                  ),
                    html.Br(),

                    html.H4('Choose the coloration of dots:'),
                    dcc.Dropdown(id='slct_color',
                                 options=[
                                     {'label': 'collor by room type',
                                         'value': 'room_type'},
                                     {'label': 'collor by neighboorhoud',
                                         'value': 'neighbourhood'}

                                 ],
                                 value='room_type',
                                 style={'backgroundColor': '#999999'},
                                 placeholder="Select a room type"
                                 ),

                    html.H4('Choose the map view:'),
                    dcc.Dropdown(id='slct_view_map',
                                 options=[
                                     {'label': 'basic view', 'value': 'basic'},
                                     {'label': 'steets view', 'value': 'streets'},
                                     {'label': 'outdoors view',
                                         'value': 'outdoors'},
                                     {'label': 'light view', 'value': 'light'},
                                     {'label': 'dark view', 'value': 'dark'},
                                     {'label': 'satellite view',
                                         'value': 'satellite'},
                                     {'label': 'satellite-streets view',
                                         'value': 'satellite-streets'}

                                 ],
                                 value='dark',
                                 style={'backgroundColor': '#999999'},
                                 placeholder="Select a map view"
                                 ),

                ]),

            ], style={'display': 'flex'}),


            html.Br(),
            html.Div(id='output_container', children=[]),
            html.Br(),
        ]),

        html.Div([
            html.H3('New york airbnb map'),

            html.Div([
                html.H4('Choose Price:'),
                dcc.RangeSlider(id='range-slider-price',
                                min=min_price,
                                max=max_price,
                                step=1,
                                vertical=True,
                                value=[0, 1500],
                                marks={
                                    0: {'label': str(min_price), 'style': {'color': '#00DA3C'}},
                                    105: {'label': str(med_price), 'style': {'color': '#c8c904'}},
                                    1500: {'label': str(max_price), 'style': {'color': '#ff0d00'}},
                                },
                                updatemode='mouseup',
                                allowCross=False
                                ),

                html.H4('Choose number of reviews:'),
                dcc.RangeSlider(id='range-slider-reviews',
                                min=min_nb_R,
                                max=max_nb_R,
                                step=1,
                                vertical=True,
                                value=[0, 629],
                                marks={
                                    0: {'label': str(min_nb_R), 'style': {'color': '#ff0d00'}},
                                    5: {'label': str(med_nb_R), 'style': {'color': '#c8c904'}},
                                    629: {'label': str(max_nb_R), 'style': {'color': '#00DA3C'}},
                                },
                                updatemode='mouseup',
                                allowCross=False
                                ),

                dcc.Graph(id='airbnb_map', figure={}),





            ], style={'display': 'flex', 'margin': 'auto', 'textAligne': 'center',
                      'borderStyle': 'groove', 'borderColor': 'aliceblue', 'backgroundColor': 'rgb(0,0,0,0)'}),

        ], style={'display': 'column'}),

    ], style={'display': 'flex', 'margin': 'auto', 'borderStyle': 'groove', 'borderColor': 'aliceblue'}),

    html.Div([
        html.Div([

            dcc.Graph(id='reviews', figure={}, style={
                      'borderStyle': 'groove', 'borderColor': 'aliceblue'}),

        ], style={'width': '60%'}),


        html.Div([

            dcc.Graph(id='room_type_pie', figure={}, style={
                      'borderStyle': 'groove', 'borderColor': 'aliceblue'}),
        ], style={'width': '40%'}),

    ], style={'display': 'flex', 'borderStyle': 'groove', 'borderColor': 'aliceblue', 'margin': 'auto'}),



    html.Div([
        dcc.Graph(id='box_price', figure={}, style={
                  'borderStyle': 'groove', 'borderColor': 'aliceblue', 'width': '50%'}),
        dcc.Graph(id='minimum_nights', figure={}, style={
                  'borderStyle': 'groove', 'borderColor': 'aliceblue', 'width': '50%'}),
    ], style={'display': 'flex', 'borderStyle': 'groove', 'borderColor': 'aliceblue'}),
    html.Div([dcc.Graph(id='word', figure={})], style={'width': '100%'})



], id='global',)


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='airbnb_map', component_property='figure'),
     Output(component_id='reviews', component_property='figure'),
     Output(component_id='room_type_pie', component_property='figure'),
     Output(component_id='box_price', component_property='figure'),
     Output(component_id='minimum_nights', component_property='figure'),
     Output(component_id='word', component_property='figure')

     ],

    [Input(component_id='slct_room_type', component_property='value'),
     Input(component_id='slct_region', component_property='value'),
     Input(component_id='range-slider-price', component_property='value'),
     Input(component_id='minimum_night', component_property='value'),
     Input(component_id='range-slider-reviews', component_property='value'),
     Input(component_id='slct_color', component_property='value'),
     Input(component_id='slct_view_map', component_property='value'),
     Input(component_id='slct_web_mode', component_property='value'),
     Input(component_id='keyword', component_property='value')]
)

def update_graph(option_slctd_1, option_slctd_2, option_slctd_3, option_slctd_4, option_slctd_5, option_slctd_6, option_slctd_7, option_slctd_8, option_slctd_9):
    tabkey=[]
    def keytest(var):
        if type(var) == str :
            if option_slctd_9 in var:
                tabkey.append(True)
            else:
                tabkey.append(False)
            
        else:
            tabkey.append(False)



    df.name.apply(lambda x : keytest(x))

    container = ["You're looking for a(n) {} ".format(option_slctd_1),
                 "near {} ".format(option_slctd_2),
                 "for the price of ${}".format(option_slctd_3),
                 " with a minimum night of {}".format(option_slctd_4),
                 " for a number of reviews between ${}".format(option_slctd_5)
                 ]

    dff = df.copy()

    df_sub = dff[tabkey]

    df_sub = df_sub[
        (dff["room_type"].isin(option_slctd_1)) &
        (dff["neighbourhood_group"].isin(option_slctd_2)) &
        (dff["price"].isin(np.arange(option_slctd_3[0], option_slctd_3[1]))) &
        (dff["minimum_nights"].isin(np.arange(1, int(option_slctd_4)))) &
        (dff["number_of_reviews"].isin(np.arange(option_slctd_5[0], option_slctd_5[1]))) 
        
    ]
    

    # Plotly Express
    fig = px.scatter_mapbox(df_sub, lat=df_sub["latitude"], lon=df_sub["longitude"], hover_name=df_sub["name"], hover_data=["neighbourhood_group", "neighbourhood", "room_type", "price", "minimum_nights", "number_of_reviews"],
                            color=df_sub[f'{option_slctd_6}'], zoom=8, height=450, width=825, title='New york airbnb map')
    fig.update_layout(mapbox_style="light",
                      mapbox_accesstoken=mapbox_access_token)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    ###########################################################################################

    fig7 = px.bar(airbnb_data[airbnb_data['neighbourhood_group'] == f'{option_slctd_2[0]}'],
                  x="number_of_reviews", y="neighbourhood", color="neighbourhood", log_x=True, title="Number of reviews by neighbourhood")

    ###########################################################################################

    roomdf = airbnb_data.groupby('room_type').size(
    )/airbnb_data['room_type'].count()*100
    labels = roomdf.index

    one = 0.0
    two = 0.0
    three = 0.0

    if('Entire home/apt' in option_slctd_1):
        one = 0.2
    else:
        one = 0.0

    if('Private room' in option_slctd_1):
        two = 0.2
    else:
        two = 0.0

    if('Shaaliceblue room' in option_slctd_1):
        three = 0.2
    else:
        three = 0.0

    fig9 = go.Figure(data=[go.Pie(labels=labels, values=airbnb_data.groupby('room_type').size(
    ), pull=[one, two, three], textinfo='percent+label', title='Room type repartition')])

    ###########################################################################################

    wordcloud_graph = plotly_wordcloud(text)

    ###########################################################################################

    fig10 = px.box(airbnb_data, x='neighbourhood_group', y='price', log_y=True,
                   color="room_type", title='Price repartition by neighbourhood group')

    ###########################################################################################

    fig6 = px.histogram(airbnb_data, x="minimum_nights", color="room_type", log_y=True,
                        log_x=True, title='Repartition of minimum night acceptency airbnb by room type')

    ###########################################################################################

    if(option_slctd_8 == 'dark'):

        fig.update_layout(legend_bgcolor="#202020", paper_bgcolor="#202020",
                          plot_bgcolor="#202020", font_color='#21a1bb')
        fig7.update_layout(legend_bgcolor="#202020", paper_bgcolor="#202020",
                           plot_bgcolor="#202020", font_color='#21a1bb')
        fig10.update_layout(legend_bgcolor="#202020", paper_bgcolor="#202020",
                            plot_bgcolor="#202020", font_color='#21a1bb')
        fig9.update_layout(legend_bgcolor="#202020", paper_bgcolor="#202020",
                           plot_bgcolor="#202020", font_color='#21a1bb')
        fig6.update_layout(legend_bgcolor="#202020", paper_bgcolor="#202020",
                           plot_bgcolor="#202020", font_color='#21a1bb')
        wordcloud_graph.update_layout(
            legend_bgcolor="#202020", paper_bgcolor="#202020", plot_bgcolor="#202020", font_color='#21a1bb')

    if(option_slctd_8 == 'light'):

        fig.update_layout(legend_bgcolor="#f8f8f0", paper_bgcolor="#f8f8f0",
                          plot_bgcolor="#f8f8f0", font_color='#041417')
        fig7.update_layout(legend_bgcolor="#f8f8f0", paper_bgcolor="#f8f8f0",
                           plot_bgcolor="#f8f8f0", font_color='#041417')
        fig10.update_layout(legend_bgcolor="#f8f8f0", paper_bgcolor="#f8f8f0",
                            plot_bgcolor="#f8f8f0", font_color='#041417')
        fig9.update_layout(legend_bgcolor="#f8f8f0", paper_bgcolor="#f8f8f0",
                           plot_bgcolor="#f8f8f0", font_color='#041417')
        fig6.update_layout(legend_bgcolor="#f8f8f0", paper_bgcolor="#f8f8f0",
                           plot_bgcolor="#f8f8f0", font_color='#041417')
        wordcloud_graph.update_layout(
            legend_bgcolor="#f8f8f0", paper_bgcolor="#f8f8f0", plot_bgcolor="#f8f8f0", font_color='#041417')

    ###########################################################################################

    fig.update_layout(
        uirevision='foo',  # preserves state of figure/map after callback activated
        clickmode='event+select',
        hovermode='closest',
        hoverdistance=2,  # hover box
        title=dict(text="Where to Stay?", font=dict(size=50, color='green')),
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style=f'{option_slctd_7}',
            # "basic", "streets", "outdoors", "light", "dark", "satellite", or "satellite-streets"
            center=dict(
                lat=40.64899,
                lon=-74.0125,
            ),
            pitch=40,
            zoom=9.7

        ))

    return container, fig, fig7, fig9, fig10, fig6, wordcloud_graph


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
