import dash
from dash import Dash, Input, Output, ctx, html, dcc
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.components import sidebar, navbar
from src.app_plots import topics_sentiment_plot



dash.register_page(__name__, path='/dashboard')

def layout(**kwargs):
    layout = html.Div([
            dbc.Row(style={"height": "10px"}),
            dbc.Row([
            html.P("Distribution of sentiments by topic")]
                , className="app-insights-title"
            ),
            dbc.Row(style={"height": "10px"}),
            dbc.Row([
                    html.Div(id="div-sentiment-plot")
                ]
            , className="app-plots")
        ],
        className="glass-backdark",
        style={"height": "500px", "width": "100%"} 
    )

    return layout
