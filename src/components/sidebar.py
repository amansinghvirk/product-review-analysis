"""
module: sidebar.py
author: Amandeep Singh
created on: 09-Jun-2024
last modified on: 09-Jun-2024

Module returns the layout for the sidebar
"""

from dash import html, dcc, page_registry
import dash_bootstrap_components as dbc
from src.components.buttons import app_buttons, app_inputs
from src.app_functions import get_topics, get_projects_list

def app_sidebar():
    """
    Generate the sidebar component for the application.

    Returns:
        sidebar: The generated sidebar component.
    """
    sidebar = dbc.Col(
        [
            dbc.Row([], style={"height": "30px"}),
            dbc.Row([
                dcc.Dropdown(
                    id="cmb-projects",
                    options=get_projects_list(),
                    className="app-dropdown",
                    style={"margin-left": "4px"}
                )
            ]),
            dbc.Row([], style={"height": "10px"}),
            dbc.Row([
                dcc.Dropdown(
                    id="cmb-topics",
                    options=[],
                    className="app-dropdown",
                    style={"margin-left": "4px"}
                )
            ]),
            dbc.Row([], style={"height": "10px"}),
            dbc.Row([
                app_buttons(
                    "btn-run-agent",
                    "Update Insights",
                    style={"width": "9rem"},
                ),
            ]),
            dbc.Row([], style={"height": "10px"})
        ],
        width=2,
        className="glass-backdark-sidebar",
        style={"height": "500px"},
    )

    return sidebar
