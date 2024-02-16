import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  


app = Dash(__name__)

df = pd.read_csv("output.csv",low_memory=False)
fire_data_grped = df.groupby(['STATE', 'FIRE_YEAR'])['FIRE_SIZE'].sum().reset_index()


app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2000", "value": 2000},
                     {"label": "2001", "value": 2001},
                     {"label": "2002", "value": 2002},
                     {"label": "2003", "value": 2003},
                     {"label": "2004", "value": 2004},
                     {"label": "2005", "value": 2005},
                     {"label": "2006", "value": 2006},
                     {"label": "2007", "value": 2007},
                     {"label": "2008", "value": 2008},
                     {"label": "2009", "value": 2009}
                 ],
                 multi=False,
                 value=2015,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='us_map', figure={})

])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='us_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    container = "The year chosen by user was: {}".format(option_slctd)
    dff = fire_data_grped.copy()
    dff = dff[dff["FIRE_YEAR"] == option_slctd]

    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='STATE',
        scope="usa",
        color='FIRE_SIZE',
        hover_data=['STATE', 'FIRE_SIZE'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        template='plotly_dark'
    )
    return container, fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)