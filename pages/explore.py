import dash
from dash import Dash, Input, Output, ctx, html, dcc
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.components import sidebar, navbar
from src.components.buttons import app_buttons
from src.callbacks.app_callbacks import empty_element


dash.register_page(__name__, path='/explore')

def layout(**kwargs):


    layout = html.Div([
            dbc.Row(style={"height": "10px"}),
            dbc.Row([
                html.P("Explore insights")]
                , className="app-insights-title"
            ),
            dbc.Row(style={"height": "10px"}),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dcc.Dropdown(
                            id="cmb-insights-type",
                            options=["Negative Insights", "Positive Insights", "Suggestions"],
                            className="app-dropdown"
                        )
                    ]),
                    dbc.Row(style={"height": "10px"}),
                    dbc.Row([
                        dcc.Dropdown(
                            id="cmb-insights",
                            options=[],
                            className="app-dropdown"
                        )
                    ])
                ],width=9),
                dbc.Col([
                    dbc.Row(style={"height": "30px"}),
                    dbc.Row([
                        app_buttons(
                            "btn-get-reviews",
                            "Fetch relevant reviews",
                            style={"width": "150px"},
                        )
                    ])
                ], width=3)

            ], style={"margin-left": "2px"}),
            dbc.Row(style={"height": "10px"}),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Spinner([
                            dbc.Col([
                                html.Div([
                                    dbc.Row([
                                        html.Div(id="relevant-reviews-summary")
                                    ])
                                ])
                            ], width=12)
                        ], color="info")
                    ])
                ], width=11)
            ], className="app-insights-suggestions"),
            dbc.Row(style={"height": "10px"}),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Spinner([
                            dbc.Col([
                                html.Div([
                                    dbc.Row([
                                        html.Div(id="relevant-reviews")
                                    ])
                                ])
                            ], width=12)
                        ], color="info")
                    ])
                ], width=11)
            ], className="app-insights-suggestions"),
            dbc.Row(style={"height": "10px"})
        ],
        className="glass-backdark",
        style={"height": "100%", "width": "100%"} 
    )

    return layout