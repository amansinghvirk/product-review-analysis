"""
module: buttons.py
author: Amandeep Singh
created on: 09-Jun-2024
last modified on: 09-Jun-2024

Module contains functions to create buttons and input components. 
Objective is to keep the standard layout of all the components

Functions:
    - app_buttons: return the button layout of the application
    - app_inputs: return the input layout of the application

"""


from dash import html, dcc
import dash_bootstrap_components as dbc


def app_buttons(
    btn_id: str, 
    btn_text: str, 
    class_name: str="app-button", 
    style:dict ={}
):
    """Creates the button layout for application buttons

    Args:
        btn_id (str): uniuqe id of each button 
        btn_text (str): Text to be displayed on the application
        class_name (str): css class name for the button styling
        style (str): css styles this will override the style in css class

    Returns:
        dbc.Button: dash button component
    """

    buttons = dbc.Button(
        btn_text, id=btn_id, n_clicks=0, className=class_name, style=style
    )

    return buttons


def app_inputs(
    input_id, input_placeholder, input_type="text", class_name="app-input", style={}
):
    """
    Create an input component for the application.

    Parameters:
    - input_id (str): The ID of the input component.
    - input_placeholder (str): The placeholder text for the input component.
    - input_type (str, optional): The type of the input component. Defaults to "text".
    - class_name (str, optional): The CSS class name for the input component. Defaults to "app-input".
    - style (dict, optional): The CSS styles for the input component. Defaults to an empty dictionary.

    Returns:
    - dcc.Input: The input component.

    """
    input = dcc.Input(
        id=input_id,
        type=input_type,
        placeholder=input_placeholder,
        debounce=True,
        className=class_name,
        style=style,
    )

    return input
