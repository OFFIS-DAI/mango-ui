from dash import dcc
from dash import html


def create_export_layout():
    return [
        html.Div(
            [
                html.Div(
                    [
                        dcc.Input(id="scenario-name", type="text"),
                        html.Label("Name of the current scenario."),
                    ],
                    className="mui-textfield mui-textfield--float-label",
                ),
                html.Div(
                    [
                        html.Button(
                            "EXPORT",
                            id="save",
                            className="mui-btn mui-btn--primary mui-btn--raised",
                        )
                    ]
                ),
            ],
            className="flex-container mui-panel ",
        )
    ]
