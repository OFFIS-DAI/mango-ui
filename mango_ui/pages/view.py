from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ALL
from dash import callback_context

import dash_cytoscape as cyto


def create_default_style(app):
    return [
        {
            "selector": "node",
            "style": {
                "content": "data(label)",
                "color": "black",
                "text-wrap": "wrap",
                "font-size": "11px",
            },
        },
        {
            "selector": ".agent-node",
            "style": {
                "background-fit": "cover",
                "background-image": f'url({app.get_asset_url("icons/agent-icon.png")})',
            },
        },
        {
            "selector": ".agent-node:selected",
            "style": {
                "background-fit": "cover",
                "background-image": f'url({app.get_asset_url("icons/agent-selected-icon.png")})',
            },
        },
    ]


def create_view_setup_layout():
    return [
        html.Div(
            [
                html.Div(
                    [
                        html.H1("Load scenario file"),
                        html.Div("Upload agent scenario"),
                        html.Br(),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Upload(
                                            id="upload-scenario",
                                            children=html.Div(
                                                [
                                                    "Drag and Drop or ",
                                                    html.A("Select Scenario File"),
                                                ]
                                            ),
                                            className="dcc-upload",
                                            multiple=False,
                                        )
                                    ]
                                ),
                                html.Button(
                                    "LOAD",
                                    id={
                                        "type": "load-button",
                                        "instance": "central",
                                    },
                                    className="mui-btn mui-btn--raised mui-btn--accent",
                                ),
                            ],
                            className="setup-tab-content",
                        ),
                    ],
                    className="mui-panel setup-container-part",
                ),
                html.Div(
                    [
                        html.H1("Create new scenario"),
                        html.Button(
                            "NEW",
                            id={
                                "type": "new-scenario-button",
                                "instance": "central",
                            },
                            className="mui-btn mui-btn--raised mui-btn--accent",
                        ),
                    ],
                    className="mui-panel setup-container-part",
                ),
                html.Br(),
                html.Br(),
                dcc.Loading(
                    id="loading-view-setup",
                    type="default",
                    children=html.Div(
                        style={"height": "100px"},
                        id="loading-view-setup-view",
                    ),
                ),
            ],
            className="flex-row-layout-ontainer",
        )
    ]


def create_view_layout(app):
    cyto_elements = [
        {
            "data": {"id": "agent1", "label": "agent1"},
            "classes": "agent-node",
        }
    ]

    return [
        html.Div(
            [
                html.Div(
                    [
                        html.Button(
                            "ADD AGENT",
                            id={
                                "type": "add-agent-button",
                                "instance": "central",
                            },
                            className="mui-btn mui-btn--flat mui-btn--accent no-margin full-width medium-font-size double-element-height",
                        ),
                        html.Button(
                            "ADD CONTAINER",
                            id={
                                "type": "add-container-button",
                                "instance": "central",
                            },
                            className="mui-btn mui-btn--flat mui-btn--accent no-margin full-width medium-font-size double-element-height",
                        ),
                        html.Button(
                            "REMOVE",
                            id={
                                "type": "remove-agent-button",
                                "instance": "central",
                            },
                            className="mui-btn mui-btn--flat mui-btn--accent no-margin full-width medium-font-size double-element-height",
                        ),
                    ],
                    className="left-panel",
                ),
                cyto.Cytoscape(
                    id="cytoscape-agent-view-central",
                    className="cytoscape-agent-view",
                    elements=cyto_elements,
                    layout={
                        "name": "circle",
                        "padding": 100,
                        "animate": True,
                        "spacingFactor": 0.5,
                    },
                    stylesheet=create_default_style(app),
                ),
                html.Div(id="cyto-overlay-container", className="content"),
            ],
            id="view-content",
            className="full-width",
        ),
        dcc.Store(id="agent-id-counter", data=0),
        dcc.Store(id="container-id-counter", data=0),
    ]


def create_agent_view_layout(nodeData):
    return html.Div(
        [
            html.Div(
                [
                    html.H1(nodeData["label"]),
                    html.Button(
                        "x",
                        id={
                            "type": "close-agent-details",
                            "instance": nodeData["id"],
                        },
                        className="mui-btn mui-btn--flat mui-btn--accent no-margin medium-font-size double-element-height",
                    ),
                ],
                className="header-flex",
            )
        ],
        className="mui-panel full-width overlay-centered border-box-style",
    )


def create_page_callbacks(app):
    @app.callback(
        Output("cytoscape-agent-view-central", "elements"),
        Output("agent-id-counter", "data"),
        Output("container-id-counter", "data"),
        State("agent-id-counter", "data"),
        State("container-id-counter", "data"),
        State("cytoscape-agent-view-central", "elements"),
        Input(
            {
                "type": "add-agent-button",
                "instance": ALL,
            },
            "n_clicks",
        ),
        Input(
            {
                "type": "add-container-button",
                "instance": ALL,
            },
            "n_clicks",
        ),
        State("cytoscape-agent-view-central", "selectedNodeData"),
        Input(
            {
                "type": "remove-agent-button",
                "instance": ALL,
            },
            "n_clicks",
        ),
    )
    def change_cyto_scene(
        agent_id_counter, container_id_counter, elements, _, __, nodeData, ___
    ):
        triggered_id = callback_context.triggered[0]["prop_id"]

        if "add-agent-button" in triggered_id:
            aid = f"agent{agent_id_counter}"
            agent_id_counter += 1
            elements += [
                {
                    "data": {"id": aid, "label": aid},
                    "classes": "agent-node",
                }
            ]
        elif "add-container-button" in triggered_id:
            cid = f"container{container_id_counter}"
            container_id_counter += 1
            elements += [
                {
                    "data": {"id": cid, "label": cid},
                    "classes": "container-node",
                }
            ]
        elif "remove-agent-button" in triggered_id:
            elements = [el for el in elements if el["data"]["id"] != nodeData[0]["id"]]

        return elements, agent_id_counter, container_id_counter

    @app.callback(
        Output("cyto-overlay-container", "children"),
        Input("cytoscape-agent-view-central", "tapNodeData"),
        Input(
            {
                "type": "close-agent-details",
                "instance": ALL,
            },
            "n_clicks",
        ),
        Input("cytoscape-agent-view-central", "tapNode"),
    )
    def show_agent_view(nodeData, _, __):
        triggered_id = callback_context.triggered[0]["prop_id"]

        if "close-agent-details" in triggered_id:
            return []
        if nodeData:
            return create_agent_view_layout(nodeData)
