import dash
from dash import Dash, Input, Output, ctx, html, dcc
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.components import sidebar, navbar
from src.callbacks.app_callbacks import empty_element


dash.register_page(__name__, path='/insights')

def layout(**kwargs):
    layout = html.Div([
            dbc.Row(style={"height": "10px"}),
            dbc.Row([
                html.P("Insights for the topic", id="insights-header")]
                , className="app-insights-title"
            ),
            dbc.Row(style={"height": "10px"}),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                                html.Div([
                                    dbc.Spinner([
                                        html.Div([
                                            dbc.Row([
                                                html.Div(
                                                    children=empty_element(), 
                                                    id="pos-insights", 
                                                    style={"margin-left": "5px"}
                                                )
                                            ])
                                        ])
                                    ], color="info")
                                ], className="app-insights-positive")
                        ], width=6),
                        dbc.Col([
                            html.Div([
                                dbc.Spinner([
                                    html.Div([
                                        dbc.Row([
                                            html.Div(
                                                children=empty_element(),
                                                id="neg-insights", 
                                                style={"margin-left": "5px"}
                                            )
                                        ])
                                    ])
                                ], color="info")
                            ], className="app-insights-negative")

                        ], width=6),
                    ])

                ], width=11)
            ]),
            dbc.Row([], style={"height": "10px"}),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Spinner([
                            dbc.Col([
                                html.Div([
                                    dbc.Row([
                                        html.Div(children=empty_element(), id="suggestions")
                                    ])
                                ])
                            ], width=12)
                        ], color="info")
                    ])
                ], width=11)
            ], className="app-insights-suggestions"),
            dbc.Row([], style={"height": "10px"})
        ],
        className="glass-backdark",
        style={"height": "100%", "width": "100%"} 
    )

    return layout