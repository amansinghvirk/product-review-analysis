"""
module: home.py
author: Amandeep Singh
created on: 09-Jun-2024
last modified on: 09-Jun-2024

Application home page layout
"""


import dash
from dash import Dash, Input, Output, ctx, html, dcc
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.components import sidebar, navbar
from src.app_plots import topics_sentiment_plot
from src.components.buttons import app_buttons


dash.register_page(__name__, path='/')


layout = html.Div([

    ],
    className="glass-backdark",
    style={"height": "500px", "width": "100%"} 
)
