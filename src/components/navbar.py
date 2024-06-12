"""
module: navbar.py
author: Amandeep Singh
created on: 09-Jun-2024
last modified on: 09-Jun-2024

Module returns the layout for application navigation bar
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
import src.constants as app_configs

def app_navbar(app):
    """
    Creates and returns the navbar component for the application.

    Returns:
        navbar: The navigation component
    """

    navbar = dbc.NavbarSimple(
        children=[

            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavLink(
                "Dashboard", 
                id="btn-update-plot",
                href="/dashboard",
                n_clicks=0
            ),
            dbc.NavLink(
                "Insights", 
                id="btn-insights", 
                href="/insights",
                n_clicks=0
            ),
            dbc.NavItem(dbc.NavLink("Explore", id="btn-explore",  href="/explore")),
            dbc.Col([], style={"width": "10px"}),
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src=app.get_asset_url("images/logo.png"), 
                                style={"height": "30px", "margin-top": "5px"})
                            ),
                    ]
                )
            )
        ],
        brand="Customer Review Analytics",
        color=app_configs.NAVBAR_COLOR,
        dark=True,
        className="mb2"
    )

    return navbar
