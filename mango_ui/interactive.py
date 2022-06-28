
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

import dash

def show_result_interactive(debug=False):

    app = dash.Dash(__name__, suppress_callback_exceptions=True)
    app.title = 'mango UI'

    # graph + detail time series
    app.layout = html.Div([
        html.Div([html.Img(id="logo", width=100, height=50, src=f"{app.get_asset_url('icons/mango-logo.png')}"),
            html.Div(["mango UI"], id='head-title'), 
            html.Div([
                dcc.Link("View", href='/view'), 
                dcc.Link("Setup", href='/setup')
            ], className='nav')
        ], className='head'), 
        dcc.Location(id="url", refresh=False),
        html.Div(id='page-content',  className='content'), 
    ], id='page')

    app.run_server(debug=debug)

