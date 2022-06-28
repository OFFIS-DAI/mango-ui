
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq

import dash

import mango_ui.pages.settings as uis

def show_result_interactive(debug=False):
    external_scripts = [
        {
            'src': '//cdn.muicss.com/mui-0.10.3/js/mui.min.js',
        }
    ]

    # external CSS stylesheets
    external_stylesheets = [
        {
            'href': '//cdn.muicss.com/mui-0.10.3/css/mui.min.css',
            'rel': 'stylesheet',
            'type': 'text/css'
        }
    ]

    app = dash.Dash(__name__, suppress_callback_exceptions=True,
        external_scripts=external_scripts,
        external_stylesheets=external_stylesheets)
    app.title = 'mango UI'

    # graph + detail time series
    app.layout = html.Div([
        html.Div([html.Img(id="logo", width=100, height=50, src=f"{app.get_asset_url('icons/mango-logo.png')}"),
            html.Div(["mango UI"], id='head-title'), 
            html.Div([
                dcc.Link("View", href='/view'), 
                dcc.Link("Settings", href='/settings')
            ], className='nav')
        ], className='head'), 
        dcc.Location(id="url", refresh=False),
        html.Div(id='page-content',  className='content'), 
        html.Div(id='settings-container',  className='content'), 
    ], id='page')

    @app.callback(Output("settings-container", "children"), 
                  Output("settings-container", "style"), 
                  [Input("url", "pathname")])  
    def display_page(path):
        if path == '/view':
            return [], {"display": "none"}
        elif path == '/settings':
            return uis.create_setup_layout(), {"display": "flex"}

    app.run_server(debug=debug)

