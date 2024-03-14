from dash import Dash, html, dcc
import dash
import plotly.express as px

px.defaults.template = "ggplot2"

app = Dash(__name__, title='Historical Analysis of Wildfires in the United States', pages_folder='pages', use_pages=True)
server = app.server

'''
    This is the main layout where the call starts.
    This holds the header chart and
    helps showing link for registered dashboard pages    
'''
app.layout = html.Div([
    html.Br(),
    html.Div([
        html.P('HISTORICAL ANALYSIS OF WILDFIRES IN THE UNITED STATES', className="heading-text")
    ], className="heading"),
    html.Div(children=[
        dcc.Link(
            page['name'],
            href=page["relative_path"],
            className="button-link m-2 fs-5",
            style={"margin-left": "18%" if page["relative_path"] == list(dash.page_registry.values())[0][
                "relative_path"] else "10px"}
        )
        for page in dash.page_registry.values()
    ]),
    dash.page_container
], className="layoutbackground")


if __name__ == '__main__':
    app.run_server()
