from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ALL
from dash import callback_context

import dash

import mango_ui.pages.export as eui
import mango_ui.pages.view as vui


def show_result_interactive(debug=False, no_start=False):
    external_scripts = [
        {
            "src": "//cdn.muicss.com/mui-0.10.3/js/mui.min.js",
        }
    ]

    # external CSS stylesheets
    external_stylesheets = [
        {
            "href": "//cdn.muicss.com/mui-0.10.3/css/mui.min.css",
            "rel": "stylesheet",
            "type": "text/css",
        }
    ]

    app = dash.Dash(
        __name__,
        suppress_callback_exceptions=True,
        external_scripts=external_scripts,
        external_stylesheets=external_stylesheets,
    )
    app.title = "mango UI"

    app.layout = html.Div(
        [
            html.Div(
                [
                    html.Img(
                        id="logo",
                        width=100,
                        height=50,
                        src=f"{app.get_asset_url('icons/mango-logo.png')}",
                    ),
                    html.Div(["mango UI"], id="head-title"),
                    html.Div(
                        [
                            dcc.Link("View", href="/view"),
                            dcc.Link("Export", id="export-link", href="/export"),
                        ],
                        className="nav",
                    ),
                ],
                className="head",
            ),
            dcc.Location(id="url", refresh=False),
            html.Div(id="page-content", className="content"),
            html.Div(id="panel-container", className="content"),
        ],
        id="page",
    )

    @app.callback(
        Output("page-content", "children"),
        Output("panel-container", "children"),
        Output("panel-container", "style"),
        Output("export-link", "href"),
        Input({"type": "new-scenario-button", "instance": ALL}, "n_clicks"),
        [Input("url", "pathname")],
    )
    def display_page(_, path):
        triggered_id = callback_context.triggered[0]["prop_id"]

        if "url" in triggered_id:
            if path == "/export":
                return (
                    dash.no_update,
                    eui.create_export_layout(),
                    {"display": "block"},
                    "/exportback",
                )
            elif path == "/exportback":
                return dash.no_update, [], {"display": "none"}, "/export"
            else:
                return (
                    vui.create_view_setup_layout(),
                    [],
                    {"display": "none"},
                    dash.no_update,
                )
        elif "new-scenario-button" in triggered_id:
            return vui.create_view_layout(app), [], {"display": "none"}, dash.no_update

    vui.create_page_callbacks(app)

    if not no_start:
        app.run_server(debug=debug)
    return app
