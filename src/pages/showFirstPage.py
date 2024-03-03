from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import dash
from dash import html, dcc, dash_table, Input, Output
import plotly.express as px

dash.register_page(__name__, path='/', name="Overview on WildFire")

# Load data
df = pd.read_csv("../data/processed/output.csv", low_memory=False)
fire_data_grped = df.groupby(['STATE', 'FIRE_YEAR', 'FIRE_SIZE_CLASS'])['FIRE_SIZE'].sum().reset_index()

# Options for filters
states = sorted([{'label': state, 'value': state} for state in fire_data_grped['STATE'].unique()],
                key=lambda x: x['label'])
fireSize = sorted([{'label': size, 'value': size} for size in fire_data_grped['FIRE_SIZE_CLASS'].unique()],
                  key=lambda x: x['label'])
default_state = 'AK'
default_fire_size = 'A'

# Define layout
layout = html.Div([
    # Filters sidebar
    html.Div([
        html.Label('Fire Year', className="filter-label"),
        dcc.RangeSlider(
            id='year-slider',
            min=fire_data_grped['FIRE_YEAR'].min(),
            max=fire_data_grped['FIRE_YEAR'].max(),
            step=1,
            value=[fire_data_grped['FIRE_YEAR'].min(), fire_data_grped['FIRE_YEAR'].max()],
            marks={fire_data_grped['FIRE_YEAR'].min(): str(fire_data_grped['FIRE_YEAR'].min()),
                   fire_data_grped['FIRE_YEAR'].max(): str(fire_data_grped['FIRE_YEAR'].max())}
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
            html.Label('Information on Fire Size', className="sub-heading"),
            html.Div([
                html.P('A = 0 - 0.25 acres'),
                html.P('B = 0.26-9.9 acres'),
                html.P('C = 10.0-99.9 acres'),
                html.P('D = 100-299 acres'),
                html.P('E = 300 to 999 acres'),
                html.P('F = 1000 to 4999 acres'),
                html.P('G = 5000+ acres')
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
                html.Label('Total Area Damaged',className="count-label"),
            ], className="countLabel"),
            html.Div([
                html.Div(id='total-wildfire-incidents',className="count"),
                html.Label('Total Wildfire Incidents',className="count-label"),
            ], className="countLabel")
        ],className="Container"),
            dcc.Graph(id='bar_plot',figure={},style={'height':'65%','margin-left':'10px'})
            ])
        ,
    ], className="Container"),  #, 'justify-content': 'space-between','margin-top': '20px', 'margin-left': '20px'
 # Charts section
    html.Div([
        html.Br(),
        dcc.Graph(id='count-chart', className="chart_1"),
        dcc.Graph(id='area-chart', className="chart_2")
    ], className="Container")
])


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
    min_year, max_year = year_range
    slider_output = dcc.Markdown(f'Selected years: {min_year} - {max_year}')
    dff = fire_data_grped.copy()
    dff = dff[
        (dff['FIRE_YEAR'] >= year_range[0]) & (dff['FIRE_YEAR'] <= year_range[1]) &
        (dff['STATE'].isin(selected_states)) &
        (dff['FIRE_SIZE_CLASS'].isin(selected_sizes))]

    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='STATE',
        scope="usa",
        color='FIRE_SIZE',
        hover_data=['STATE', 'FIRE_SIZE'],
        color_continuous_scale=px.colors.sequential.YlOrRd
    )
    count_chart = px.histogram(dff, x='FIRE_YEAR', color='STATE', title='Count of Fires by Year and State')
    area_chart = px.scatter(dff, x='FIRE_YEAR', y='FIRE_SIZE', color='STATE',
                            title='Total Area Burned by Year and State')
    total_area = round(dff['FIRE_SIZE'].sum(),3)
    total_count = dff['FIRE_SIZE'].count()

    top10_grouped = dff.groupby('STATE')['FIRE_SIZE'].sum().reset_index()
    top10 = top10_grouped.head(10)
    barPlot = px.bar(top10, y='STATE', x='FIRE_SIZE')
    return slider_output, fig, count_chart, area_chart,total_area,total_count,barPlot
