from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash import callback_context
import dash

import dash_cytoscape as cyto
import mango_ui.example_agents as example_agents

from mango_ui.simulation import execute_simulation_with_ui_data


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
        html.Div(
            [],
            id="scenario-overall-container-output-container",
        ),
        html.Div(
            [dcc.Store(id={"type": "agent-container-data", "instance": "agent1"})],
            id="scenario-overall-agent-output-container",
        ),
        html.Button(
            "SIM",
            id="start-simulation",
            n_clicks=0,
            className="mui-btn mui-btn--fab mui-btn--primary primary-action-button",
        ),
        dcc.Store(id="simulation-store"),
    ]


def create_container_view_layout(nodeData):
    return html.Div(
        [
            html.Div(
                [
                    html.H1(nodeData["label"]),
                    html.Button(
                        "x",
                        id={
                            "type": "close-node-details",
                            "instance": nodeData["id"],
                        },
                        className="mui-btn mui-btn--flat mui-btn--accent no-margin medium-font-size double-element-height",
                    ),
                ],
                className="header-flex",
            ),
            dcc.Dropdown(
                [str(acls) for acls in example_agents.ALL_CONT],
                str(example_agents.ALL_CONT[0]),
                id={"type": "choose-container-cls", "instance": nodeData["id"]},
            ),
            html.Div(
                [],
                id={"type": "param-container-content", "instance": nodeData["id"]},
                className="content-column",
            ),
        ],
        className="mui-panel full-width overlay-centered border-box-style",
    )


def create_agent_view_layout(nodeData):
    return html.Div(
        [
            html.Div(
                [
                    html.H1(nodeData["label"]),
                    html.Button(
                        "x",
                        id={
                            "type": "close-node-details",
                            "instance": nodeData["id"],
                        },
                        className="mui-btn mui-btn--flat mui-btn--accent no-margin medium-font-size double-element-height",
                    ),
                ],
                className="header-flex",
            ),
            dcc.Dropdown(
                [str(acls) for acls in example_agents.ALL_AGENTS],
                str(example_agents.ALL_AGENTS[0]),
                id={"type": "choose-agent-cls", "instance": nodeData["id"]},
            ),
            html.Div(
                [],
                id={"type": "param-agent-content", "instance": nodeData["id"]},
                className="content-column",
            ),
        ],
        className="mui-panel full-width overlay-centered border-box-style",
    )


def create_page_callbacks(app):
    @app.callback(
        Output("simulation-store", "data"),
        Input("start-simulation", "n_clicks"),
        State("scenario-overall-agent-output-container", "children"),
        State("scenario-overall-container-output-container", "children"),
    )
    def start_simulation(_, scenario_data_agent, scenario_data_container):
        if scenario_data_agent and scenario_data_container:
            data_entries_agent = [
                scenario_data_store["props"]["data"]
                for scenario_data_store in scenario_data_agent
            ]
            data_entries_container = [
                scenario_data_store["props"]["data"]
                for scenario_data_store in scenario_data_container
            ]
            execute_simulation_with_ui_data(data_entries_container, data_entries_agent)

        return dash.no_update

    @app.callback(
        Output({"type": "param-agent-content", "instance": MATCH}, "children"),
        Input({"type": "choose-agent-cls", "instance": MATCH}, "value"),
        State({"type": "choose-agent-cls", "instance": MATCH}, "id"),
    )
    def choose_agent_cls(new_value, id):
        if new_value:
            actual_agent = None
            for agent in example_agents.ALL_AGENTS:
                if str(agent) == new_value:
                    actual_agent = agent
            parameters_for_agent = actual_agent.__ui_parameters__
            inputs = [
                html.Div(
                    [
                        dcc.Input(
                            id={
                                "type": "single-param-agent",
                                "instance": id["instance"],
                                "param-id": param_name,
                            },
                            type="text",
                        ),
                        html.Label(f"{param_name} ({str(desc[0])})"),
                    ],
                    className="mui-textfield mui-textfield--float-label full-width",
                )
                for param_name, desc in parameters_for_agent.items()
            ]
            return inputs
        return dash.no_update

    @app.callback(
        Output("cytoscape-agent-view-central", "elements"),
        Output("agent-id-counter", "data"),
        Output("container-id-counter", "data"),
        Output("scenario-overall-agent-output-container", "children"),
        Output("scenario-overall-container-output-container", "children"),
        State("scenario-overall-agent-output-container", "children"),
        State("scenario-overall-container-output-container", "children"),
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
        output_agent_state,
        output_cont_state,
        agent_id_counter,
        container_id_counter,
        elements,
        _,
        __,
        nodeData,
        ___,
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
            output_agent_state.append(
                dcc.Store(id={"type": "agent-container-data", "instance": aid})
            )
        elif "add-container-button" in triggered_id:
            cid = f"container{container_id_counter}"
            container_id_counter += 1
            elements += [
                {
                    "data": {"id": cid, "label": cid},
                    "classes": "container-node",
                }
            ]
            output_cont_state.append(
                dcc.Store(id={"type": "container-container-data", "instance": cid})
            )
        elif "remove-agent-button" in triggered_id:
            elements = [el for el in elements if el["data"]["id"] != nodeData[0]["id"]]

        return (
            elements,
            agent_id_counter,
            container_id_counter,
            output_agent_state,
            output_cont_state,
        )

    @app.callback(
        Output({"type": "agent-container-data", "instance": MATCH}, "data"),
        Input(
            {
                "type": "close-node-details",
                "instance": MATCH,
            },
            "n_clicks",
        ),
        State(
            {"type": "single-param-agent", "instance": MATCH, "param-id": ALL},
            "value",
        ),
        State(
            {"type": "single-param-agent", "instance": MATCH, "param-id": ALL},
            "id",
        ),
        State({"type": "choose-agent-cls", "instance": MATCH}, "value"),
    )
    def store_agent_data(_, agent_state, ids, agent_cls):
        triggered_id = callback_context.triggered[0]["prop_id"]

        if "close-node-details" in triggered_id and agent_state:
            agent_data = {}
            param_ids = [id["param-id"] for id in ids]
            for i, param_id in enumerate(param_ids):
                agent_data[param_id] = agent_state[i]
            return [agent_cls, agent_data]
        return dash.no_update

    @app.callback(
        Output({"type": "container-container-data", "instance": MATCH}, "data"),
        Input(
            {
                "type": "close-node-details",
                "instance": MATCH,
            },
            "n_clicks",
        ),
        State({"type": "choose-container-cls", "instance": MATCH}, "value"),
    )
    def store_container_data(_, container_cls):
        triggered_id = callback_context.triggered[0]["prop_id"]

        if "close-node-details" in triggered_id and container_cls:
            return [container_cls, {}]
        return dash.no_update

    @app.callback(
        Output("cyto-overlay-container", "children"),
        Input("cytoscape-agent-view-central", "tapNodeData"),
        Input(
            {
                "type": "close-node-details",
                "instance": ALL,
            },
            "n_clicks",
        ),
        Input("cytoscape-agent-view-central", "tapNode"),
    )
    def show_agent_view(nodeData, _, __):
        triggered_id = callback_context.triggered[0]["prop_id"]

        if "close-node-details" in triggered_id:
            return []
        if nodeData:
            if "agent" in nodeData["id"]:
                return create_agent_view_layout(nodeData)
            else:
                return create_container_view_layout(nodeData)
