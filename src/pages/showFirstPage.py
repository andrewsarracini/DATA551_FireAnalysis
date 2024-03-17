from dash import Dash, html, Input, Output, callback
import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

'''
Helps to register the page
'''
dash.register_page(__name__, path='/', name="WildFire Overview")

'''
Helps to get the data. 
Then, filters and groups the data according to the requirement 
'''
#df = pd.read_csv("https://raw.githubusercontent.com/andrewsarracini/DATA551_FireAnalysis/main/data/processed/output.csv", low_memory=False)
df = pd.read_csv("https://raw.githubusercontent.com/Naye013/Fires/main/data/processed/output.csv", low_memory=False)

fire_data_grped = df.groupby(['state_descriptions','STATE', 'FIRE_YEAR', 'FIRE_SIZE_CLASS'])['FIRE_SIZE'].agg(['sum', 'count']).reset_index()
fire_data_grped.rename(columns={'sum': 'FIRE_SIZE', 'count': 'TotalFireCount'}, inplace=True)

'''
Collects the values for the filter. Sorts it so that user can easily scroll through it.
Adds an 'All' button, so that the user can see the over view of wildfire on all states and of all sizes.
'''
states = sorted([
    {'label': state_label, 'value': state_value}
    for state_value, state_label in zip(fire_data_grped['STATE'].unique(), fire_data_grped['state_descriptions'].unique())
], key=lambda x: x['label'])
fireSize = sorted([{'label': size, 'value': size} for size in fire_data_grped['FIRE_SIZE_CLASS'].unique()],
                  key=lambda x: x['label'])

all_dict = {"label": "All", "value": "All"}
states.insert(0, all_dict)
fireSize.insert(0, all_dict)

default_state = 'All'
default_fire_size = 'All'

'''
Helps to design the layout.
The layout has 2 main component, the filter components and the main page component.
Those page components are further divided to fit filters and charts.
It takes it's design form the css file in assets.
Component description:
Filter Division:
    1. year-slider : responsible for showing year filter
    2. slider-output-container-map : shows the user selected year range
    3. state-dropdown : a multiselect combo box that shows all the states
    4. size-class-dropdown : A multiselect combo box that shows all the Categorized fire sizes
    5. Fire Size Description : A scrollable text bar that shows description about the fire sizes
Main Division:
    1. us_maps: helps to visualize how wild wife is spread acroos different staes in US
    2. fire size countLabel: helps to give exact figure of total area damaged
    3. fire occurance countLabel: helps to give exact figure of total wildfire incident 
    4. top 10 bar plot chart : shows the top 10 area damaged by the wild fire.
    5. count line chart : helps to visualize the total wildfire incident over the time
    6. count area chart : helps to visualize the area burned by wildfire over the time
'''
# Define layout
layout = html.Div([
    # Filters sidebar
    html.Div([
        html.Label('Fire Year', className="filter-label"),
        dcc.RangeSlider(
            id='year-slider',
            min=int(fire_data_grped['FIRE_YEAR'].min()),
            max=int(fire_data_grped['FIRE_YEAR'].max()),
            step=1,
            value=[fire_data_grped['FIRE_YEAR'].min(), fire_data_grped['FIRE_YEAR'].max()],
            marks={int(fire_data_grped['FIRE_YEAR'].min()): str(fire_data_grped['FIRE_YEAR'].min()),
                   int(fire_data_grped['FIRE_YEAR'].max()): str(fire_data_grped['FIRE_YEAR'].max())}
        ),
        html.Div(id='slider-output-container-map', className="slider-output"),
        html.Label('State', className="filter-label"),
        dcc.Dropdown(
            id='state-dropdown',
            options=states,
            multi=True,
            value=[default_state],
            className="shadow-style"
        ),
        html.Br(),
        html.Label('Fire Size', className="filter-label"),
        dcc.Dropdown(
            id='size-class-dropdown',
            options=fireSize,
            multi=True,
            value=[default_fire_size],
            className="shadow-style"
        ),
        html.Br(),
        html.Div([
            html.Label('Fire Size Description', className="filter-label"),
            html.Div([
                html.P('A = 0 - 0.25 acres (minimal)'),
                html.P('B = 0.26-9.9 acres (minor)'),
                html.P('C = 10.0-99.9 acres (low-moderate)'),
                html.P('D = 100-299 acres (moderate)'),
                html.P('E = 300 to 999 acres (high-moderate)'),
                html.P('F = 1000 to 4999 acres (major)'),
                html.P('G = 5000+ acres (extreme)')
            ], className='fire-size-info')
        ]),
    ], className="sidebar"),
    # Maps section
    html.Div([
        dcc.Graph(id='us_maps', figure={}, className="mapStyle"),
        html.Div([
            html.Div([
                html.Div([
                    html.Div(id='total-area-damaged', className="count"),
                    html.Label('Total Area Damaged', className="count-label"),
                ], className="countLabel"),
                html.Div([
                    html.Div(id='total-wildfire-incidents', className="count"),
                    html.Label('Total Wildfire Incidents', className="count-label"),
                ], className="countLabel")
            ], className="Container"),
            dcc.Graph(id='bar_plot', figure={}, style={'height': '65%', 'margin-left': '10px'})
        ])
        ,
    ], className="Container"),  # , 'justify-content': 'space-between','margin-top': '20px', 'margin-left': '20px'
    # Charts section
    html.Div([
        html.Br(),
        dcc.Graph(id='count-chart', className="chart_1"),
        dcc.Graph(id='area-chart', className="chart_2")
    ], className="Container")
])

'''
Helps to update the charts based on filter
Input:
 1. selected years from year slider
 2. selected state from state-dropdown
 3. selected fire size from size-class-dropdown
Output:
 1. us_maps
 2. fire size countLabel
 3. fire occurance countLabel
 4. top 10 bar plot chart 
 5. count line chart 
 6. count area chart 
'''
@callback(
    [Output('slider-output-container-map', 'children'),
     Output(component_id='us_maps', component_property='figure'),
     Output('count-chart', 'figure'),
     Output('area-chart', 'figure'),
     Output('total-area-damaged', 'children'),
     Output('total-wildfire-incidents', 'children'),
     Output('bar_plot', 'figure')],
    [Input('year-slider', 'value'),
     Input('state-dropdown', 'value'),
     Input('size-class-dropdown', 'value')]
)
def update_graph(year_range, selected_states, selected_sizes):
    '''
    Helsp to update teh chart based on the input fdat

    :param year_range: list of selected years
    :param selected_states: selected state
    :param selected_sizes: selected fire size
    :return: updated chart
    '''
    min_year, max_year = year_range
    slider_output = dcc.Markdown(f'Selected years: {min_year} - {max_year}')
    dff = fire_data_grped.copy()
    dff = dff[(dff['FIRE_YEAR'] >= year_range[0]) & (dff['FIRE_YEAR'] <= year_range[1])]
    if 'All' not in selected_states:
        dff = dff[dff['STATE'].isin(selected_states)]
    if 'All' not in selected_sizes:
        dff = dff[dff['FIRE_SIZE_CLASS'].isin(selected_sizes)]

    mapdata = dff.groupby(['STATE'])['FIRE_SIZE'].sum().reset_index()

    count_area_data = dff[['FIRE_YEAR', 'FIRE_SIZE_CLASS', 'FIRE_SIZE','TotalFireCount']]
    count_area_data = count_area_data.groupby(['FIRE_YEAR', 'FIRE_SIZE_CLASS']).agg({'FIRE_SIZE': 'sum', 'TotalFireCount': 'sum'}).reset_index()
    count_area_data.rename(columns={'sum': 'TotalFireSize', 'count': 'TotalFireCount'}, inplace=True)

    fig = px.choropleth(
        data_frame=mapdata,
        locationmode='USA-states',
        locations='STATE',
        scope="usa",
        color='FIRE_SIZE',
        hover_data=['STATE', 'FIRE_SIZE'],
        color_continuous_scale= px.colors.sequential.YlOrRd,
        template='plotly_dark',
        labels={'FIRE_SIZE': 'Fire Size Class', 'STATE': 'State'}
    )
    color_scale = px.colors.sequential.YlOrRd
    '''
    Helps to get and update  
    '''
    count_chart = px.area(count_area_data, x='FIRE_YEAR', y='TotalFireCount', line_shape='linear',
                          color='FIRE_SIZE_CLASS',
                          color_discrete_sequence=color_scale, title='Annual Count of Wildfires',
                          template='plotly_dark')
    count_chart.update_layout(
        xaxis_title='',
        yaxis_title='Count of Wildfires',
        legend_title_text="Fire Size Class"
    )
    '''
    Helps to get and update area chart
    '''
    area_chart = px.area(count_area_data, x='FIRE_YEAR', y='FIRE_SIZE', line_shape='linear', color='FIRE_SIZE_CLASS',
                         color_discrete_sequence=color_scale, title='Annual Area Damaged by Wildfires',
                         template='plotly_dark')
    area_chart.update_layout(
        xaxis_title='',
        yaxis_title='Area Damaged (Acres)',
        legend_title_text="Fire Size Class"
    )

    total_area = f"{round(dff['FIRE_SIZE'].sum(), 1):,}"
    total_count = f"{round(dff['TotalFireCount'].sum(), 1):,}"

    top10_grouped = dff.groupby('STATE')['FIRE_SIZE'].sum().reset_index()
    top10 = top10_grouped.head(10)

    top10_sorted = top10.sort_values(by='FIRE_SIZE', ascending=False)

    color_scale = px.colors.sequential.YlOrRd
    '''
    Helps to add and update bar plot 
    '''
    barPlot = px.bar(
        top10_sorted,
        y='STATE',
        x='FIRE_SIZE',
        color='FIRE_SIZE',
        color_continuous_scale=color_scale,
        labels={'FIRE_SIZE': 'Total Area Damaged (Acres)'},
        template='plotly_dark'
    )
    barPlot.update_layout(
        yaxis=dict(title=None),
        title="Top 10 Wildfire Damage States"
    )
    barPlot.update_layout(
        showlegend=False,
        coloraxis_showscale=False
    )
    return slider_output, fig, count_chart, area_chart, total_area, total_count, barPlot
