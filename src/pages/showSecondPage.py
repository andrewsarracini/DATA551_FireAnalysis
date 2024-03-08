import pandas as pd
import altair as alt
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_vega_components as dvc

alt.data_transformers.enable("vegafusion")
dash.register_page(__name__, path='/showSecondPage.py', name="Causes of WildFire")
# Load data
df = pd.read_csv("../data/processed/output.csv", low_memory=False)
alt.themes.enable('dark')
wildfires_causes = df.groupby(['FIRE_YEAR', 'state_descriptions', 'FIRE_SIZE_CLASS', 'STAT_CAUSE_DESCR']).size().reset_index(name='COUNT')
fireSize = sorted([{'label': size, 'value': size} for size in wildfires_causes['FIRE_SIZE_CLASS'].unique()],
                  key=lambda x: x['label'])
all_dict = {"label": "All", "value": "All"}
fireSize.insert(0, all_dict)
default_fire_size = 'All'

# Function to create Altair chart
def create_altair_chart(data):
    title = alt.TitleParams(
    text='Understanding Wildfires: Causes and Estimated Fire Size Classes',
    subtitle='The fire size classes range from A (small) to G (large)')
    chart = alt.Chart(data, title=title).mark_square().encode(
        alt.X('FIRE_SIZE_CLASS:N', title=None, axis=alt.Axis(labelAngle=0, ticks=False)),
        alt.Y('STAT_CAUSE_DESCR:N', title=None, sort='color', axis=alt.Axis(ticks=False, labels=True)),
        alt.Color('count(FIRE_SIZE_CLASS)', title= 'Number of wildfires', scale=alt.Scale(scheme='darkred')),
        size='count(FIRE_SIZE_CLASS)',
        tooltip=[
        alt.Tooltip('FIRE_SIZE_CLASS:N', title='Class'),
        alt.Tooltip('STAT_CAUSE_DESCR:N', title='Cause'),
        alt.Tooltip('count(FIRE_SIZE_CLASS)', title='Fires')
        ]
    ).properties(width=300, height=300).configure_view(stroke='transparent')
    return chart.to_dict(format="vega")
## -- Plot 2: "altair-chart-2" --
causes_grouped = df[df['CAUSES'].isin(['Human', 'Lightning'])].groupby(['FIRE_YEAR', 'state_descriptions', 'geographic_areas_desc', 'CAUSES']).size().reset_index(name='COUNT')
def create_altair_chart2(data):
    title2 = alt.TitleParams(
        text='Proportion of Fires',
        subtitle='By Geographic Area and Cause')
    chart2 = alt.Chart(data, title=title2).mark_bar().encode(
        alt.X('sum(COUNT)', stack='normalize', title=''),
        alt.Y('geographic_areas_desc:O', sort='y', title=""),
        alt.Color('CAUSES', title="", scale=alt.Scale(scheme='darkred'), legend=alt.Legend(orient='none',
            legendX=90, legendY=-20,
            direction='horizontal',
            titleAnchor='middle')),
        tooltip=[
            alt.Tooltip('sum(COUNT)', title='Fires', format=',d'),
            alt.Tooltip('geographic_areas_desc:O', title='Area'),
            alt.Tooltip('CAUSES', title='Cause')
        ]
    ).properties(width=300, height=300)
    return chart2.to_dict(format="vega")
## -- Plot 3: "altair-chart-3" --
# Group by FIRE_YEAR, STATE, and MONTH, calculate the count, and reset the index
grouped_df = df[df['CAUSES'].isin(['Human', 'Lightning'])].groupby(['FIRE_YEAR', 'state_descriptions', 'CAUSES', 'MONTH']).size().reset_index(name='COUNT')
# Define the sort order
sort_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# Sorting dataframe by the desired order
grouped_df['MONTH'] = pd.Categorical(grouped_df['MONTH'], categories=sort_order, ordered=True)
grouped_df = grouped_df.sort_values(by='MONTH')
def create_altair_chart3(data):
    title3 = alt.TitleParams(
                text='Average number of fires',
                subtitle='By Month and Cause')
    chart3 = (alt.Chart(data, title=title3).mark_line().encode(
    alt.X('MONTH:O', title=None, sort=sort_order, axis=alt.Axis(labelAngle=0)),
    alt.Y('average(COUNT)', title=None),
    alt.Color('CAUSES:O', title= '', scale=alt.Scale(scheme='darkred'), legend=alt.Legend(orient='none',
    legendX=120, legendY=-20, direction='horizontal', titleAnchor='middle'))
    ).properties(width=355, height=270,
    ) + alt.Chart(data).mark_point().encode(
    alt.X('MONTH:O', title=None, sort=sort_order),
    alt.Y('average(COUNT)'),
    alt.Color('CAUSES:O', title='', scale=alt.Scale(scheme='darkred')),
    tooltip=[
    alt.Tooltip('MONTH:O', title='Month'),
    alt.Tooltip('average(COUNT):Q', title='Mean', format='.2f'),
    alt.Tooltip('CAUSES:O', title='Cause')]
    ))
    return chart3.to_dict(format="vega")
## -- Plot 4: "altair-chart-4" --
# Total acres burned
causes_grouped2 = df[df['CAUSES'].isin(['Human', 'Lightning'])].groupby(['FIRE_YEAR', 'state_descriptions', 'geographic_areas_desc', 'CAUSES'])['FIRE_SIZE'].sum().reset_index(name='SUM')
def create_altair_chart4(data):
    title4 = alt.TitleParams(
        text='Proportion of Acres Burned',
        subtitle='By Geographic Area and Cause')
    chart4 = alt.Chart(data, title=title4).mark_bar().encode(
        alt.X('sum(SUM)', stack='normalize', title=''),
        alt.Y('geographic_areas_desc:O', sort='y', title=""),
        alt.Color('CAUSES', title="", scale=alt.Scale(scheme='darkred'), legend=alt.Legend(orient='none',
            legendX=90, legendY=-20,
            direction='horizontal',
            titleAnchor='middle')),
        tooltip=[
            alt.Tooltip('sum(SUM)', title='Acres', format=',d'),
            alt.Tooltip('geographic_areas_desc:O', title='Area'),
            alt.Tooltip('CAUSES', title='Cause')
        ]
    ).properties(width=300, height=300)
    return chart4.to_dict(format="vega")
## -- End of plots --
# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# Options for filters (New version)
states = sorted([{'label': state, 'value': state} for state in df['state_descriptions'].unique()], key=lambda x: x['label'])
all_dict = {"label": "All", "value": "All"}
states.insert(0, all_dict)
default_state = 'All'


# Define layout
layout = html.Div([
    # Main container for the entire layout
    html.Div([
        # Filters sidebar (dbc.Col with width=3)
        dbc.Col([
            html.Label('Fire Year', className="filter-label"),
            dcc.RangeSlider(
                id='year-slider',
                min=int(df['FIRE_YEAR'].min()),
                max=int(df['FIRE_YEAR'].max()),
                step=1,
                value=[df['FIRE_YEAR'].min(), df['FIRE_YEAR'].max()],
                marks={int(df['FIRE_YEAR'].min()): str(df['FIRE_YEAR'].min()),
                       int(df['FIRE_YEAR'].max()): str(df['FIRE_YEAR'].max())}
            ),
            html.Div(id='slider-output-container', className="slider-output"),
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
                html.P('A = 0 - 0.25 acres'),
                html.P('B = 0.26-9.9 acres'),
                html.P('C = 10.0-99.9 acres'),
                html.P('D = 100-299 acres'),
                html.P('E = 300 to 999 acres'),
                html.P('F = 1000 to 4999 acres'),
                html.P('G = 5000+ acres')
            ], className='fire-size-info')
        ]),
            #html.Button("SELECT ALL", id="select-all", n_clicks=0, style={'margin-top': '10px'}),
            html.Br()
        ], width=3, className="sidebar"),  # End of Filters sidebar
        html.Br(),
        # First column of plots (dbc.Col with width=6)
        dbc.Col([
            html.Br(),
            dvc.Vega(
                id="altair-chart-1",
                opt={"renderer": "svg", "actions": False},
                spec=create_altair_chart(wildfires_causes),
            ),
            html.Br(),
            dvc.Vega(
                id="altair-chart-2",
                opt={"renderer": "svg", "actions": False},
                spec=create_altair_chart2(causes_grouped),
            ),
        ], width=3),  # End of first column
        # Second column of plots (dbc.Col with width=6)
        dbc.Col([
            html.Br(),
            dvc.Vega(
                id="altair-chart-3",
                opt={"renderer": "svg", "actions": False},
                spec=create_altair_chart3(grouped_df),
            ),
            html.Br(),
            dvc.Vega(
                id="altair-chart-4",
                opt={"renderer": "svg", "actions": False},
                spec=create_altair_chart4(causes_grouped2),
            ),
        ],width=5)  # End of second column
    ], className="Container")  # End of Main container
])
@callback(
    [Output('slider-output-container', 'children'),
    Output('altair-chart-1', 'spec'),
     Output('altair-chart-2', 'spec'),
     Output('altair-chart-3', 'spec'),
     Output('altair-chart-4', 'spec')],
    [Input('year-slider', 'value'),
     Input('state-dropdown', 'value'),
     Input('size-class-dropdown', 'value')]
)
def update_altair_chart(year_range, selected_states, selected_sizes):
    dff = wildfires_causes.copy()
    dff2 = causes_grouped.copy()
    dff3 = grouped_df.copy()
    dff4 = causes_grouped2.copy()

    dff = wildfires_causes[(wildfires_causes['FIRE_YEAR'] >= year_range[0]) & (wildfires_causes['FIRE_YEAR'] <= year_range[1])]
    dff2 = causes_grouped[(causes_grouped['FIRE_YEAR'] >= year_range[0]) & (causes_grouped['FIRE_YEAR'] <= year_range[1])]
    dff3 = grouped_df[(grouped_df['FIRE_YEAR'] >= year_range[0]) & (grouped_df['FIRE_YEAR'] <= year_range[1])]
    dff4 = causes_grouped2[(causes_grouped2['FIRE_YEAR'] >= year_range[0]) & (causes_grouped2['FIRE_YEAR'] <= year_range[1])]

    if 'All' not in selected_states:
        dff = dff[dff['state_descriptions'].isin(selected_states)]
        dff2 = dff2[dff2['state_descriptions'].isin(selected_states)]
        dff3 = dff3[dff3['state_descriptions'].isin(selected_states)]
        dff4 = dff4[dff4['state_descriptions'].isin(selected_states)]

    if 'All' not in selected_sizes:
        dff = dff[dff['FIRE_SIZE_CLASS'].isin(selected_states)]
        dff2 = dff2[dff2['FIRE_SIZE_CLASS'].isin(selected_states)]
        dff3 = dff3[dff3['FIRE_SIZE_CLASS'].isin(selected_states)]
        dff4 = dff4[dff4['FIRE_SIZE_CLASS'].isin(selected_states)]

    updated_chart1 = create_altair_chart(dff)
    updated_chart2 = create_altair_chart2(dff2)
    updated_chart3 = create_altair_chart3(dff3)
    updated_chart4 = create_altair_chart4(dff4)
    slider_output = dcc.Markdown(f'Selected years: {year_range[0]} - {year_range[1]}')
    return slider_output, updated_chart1, updated_chart2, updated_chart3, updated_chart4

