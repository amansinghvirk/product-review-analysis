"""
module: app.py
author: Amandeep Singh
created on: 09-Jun-2024
last modified on: 09-Jun-2024

Application description: Dash based application which uses Large Language Model to generate insights
from customer or product reviews.

The module is main entry which loads the application
"""

import dash
from dash import Dash, Input, Output, ctx, html, dcc
from dash import html, dcc
import dash_bootstrap_components as dbc
import os
from dotenv import load_dotenv
from openai import OpenAI
from src.components import sidebar, navbar
from src.callbacks.app_callbacks import get_callbacks
import plotly.graph_objects as go
from src.utils import create_cache_if_not_exists

load_dotenv(".env")

# Create cache folder if not exists to store the llm executions
create_cache_if_not_exists()

app = Dash(
    __name__, 
    title="Review Insights", 
    external_stylesheets=[dbc.themes.SOLAR],
    use_pages=True,
    suppress_callback_exceptions = True,
    prevent_initial_callbacks = True
)

app_layout = dbc.Container([
    navbar.app_navbar(app),
    dbc.Row([
        sidebar.app_sidebar(),
        dbc.Col([
            html.Div([
                dash.page_container
            ], style={"width": "100%"})
    
        ], width=9)
    ])
])

app.layout = app_layout 

get_callbacks(app)

if __name__ == "__main__":
    app.run_server(port=8051, debug=True, host="0.0.0.0")