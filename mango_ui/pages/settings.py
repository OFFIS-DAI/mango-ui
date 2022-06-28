import dash_html_components as html
import dash_core_components as dcc


def create_setup_layout():
    return [
        html.Div([
            dcc.Input(
                id='scenario-name',
                type="text"
            ),
            html.Label('Name of the current scenario.'),
        ], className="mui-textfield mui-textfield--float-label"),
        html.Div([
            html.Button("SAVE",id="save", className='mui-btn mui-btn--primary mui-btn--raised')
        ])
    ]