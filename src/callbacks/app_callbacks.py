"""
module: app_callbacks.py
author: Amandeep Singh
created on: 09-Jun-2024
last modified on: 09-Jun-2024

Module returns the application callbacks

"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from src.app_functions import (
    get_projects_list,
    get_topics,
    review_insights, 
    review_suggestions, 
    get_topic_insights_for_exploration,
    get_relevant_reviews_and_llm_summary
)
from src.app_plots import topics_sentiment_plot

def empty_element():
    return html.P([""], style={"height": "40px"})

def get_callbacks(app):
    """
    Returns the callbacks for the given app.

    Parameters:
    - app: The Dash app object.

    Returns:
    - A list of callbacks.

    """

    # @app.callback(
    #     Output("add-modal-card", "is_open"),
    #     Output("cmb-projects", "options"),
    #     [Input("btn-open-project", "n_clicks")],
    #     Input("add-modal-card", "is_open")],
    # )
    # def toggle_modal(n1, is_open):
    #     projects_list = get_projects_list()
    #     if n1:
    #         return not is_open, projects_list
    #     return is_open, projects_list

    @app.callback(
        Output("cmb-topics", "options"),
        Input("cmb-projects", "value")
    )
    def update_topic_list(project):
        if project:
            if (project != ""):
                topics = get_topics(project)
                return topics
        return []

    @app.callback(
        Output("div-sentiment-plot", "children"),
        Input("btn-update-plot", "n_clicks"),
        State("cmb-projects", "value")
    )
    def update_plot(n_click, project):
        if n_click:
            if project:
                if (project != ""):
                    sentiment_plot = topics_sentiment_plot(project)
                    plt = dcc.Graph(
                        id="graph-sentiment", 
                        figure=sentiment_plot, 
                        style={"height": "100%"}
                    )
                    return plt
        return ""


    @app.callback(
        Output("neg-insights", "children"),
        Output("pos-insights", "children"),
        Output("suggestions", "children"),
        Output("insights-header", "children"),
        [Input("btn-run-agent", "n_clicks"),
        Input("btn-insights", "n_clicks")],
        State("cmb-projects", "value"),
        State("cmb-topics", "value")
    )
    def update_insights(
        n_click, n_click_insight, project, topic
    ):
        title = f"Insights for the topic: {topic}"

        if n_click or n_click_insight:
            try:

                # Insights for negative reviews
                negative_insights = review_insights(project, topic, sentiment="negative")
                app_negative_insights = [html.H6("Insights from negative reviews:\n\n")]
                idx = 0
                for insight in negative_insights:
                    idx = idx + 1
                    app_negative_insights.append(html.P(f"{idx}. {insight}\n"))

                # Insights for positive reviews
                positive_insights = review_insights(project, topic, sentiment="positive")
                app_positive_insights = [html.H6("Insights from positive reviews:\n\n")]
                idx = 0
                for insight in positive_insights:
                    idx = idx + 1
                    app_positive_insights.append(html.P(f"{idx}. {insight}\n"))

                # Insights for suggestions
                suggestions = review_suggestions(project, topic)
                app_suggestions = [html.H6("Suggestions:\n\n")]
                idx = 0
                for insight in suggestions:
                    idx = idx + 1
                    app_suggestions.append(html.P(f"{idx}. {insight}\n"))

                return app_negative_insights, app_positive_insights, app_suggestions, title
            except Exception as e:
                print(e)
                return empty_element(), empty_element(), empty_element(), ""
        return empty_element(), empty_element(), empty_element(), ""

    @app.callback(
        Output("cmb-insights", "options"),
        Input("cmb-insights-type", "value"),
        State("cmb-projects", "value"),
        State("cmb-topics", "value")
    )
    def get_insights_list(insights_type, project, topic):
        if ((topic is not None) 
            & (insights_type is not None)):
            insights = get_topic_insights_for_exploration(project, topic, insights_type)

            if insights:
                return insights
            else:
                return []
        return []   

    @app.callback(
        Output("relevant-reviews", "children"),
        Output("relevant-reviews-summary", "children"),
        Input("btn-get-reviews", "n_clicks"),
        State("cmb-insights-type", "value"),
        State("cmb-insights", "value"),
        State("cmb-projects", "value"),
        State("cmb-topics", "value")
    )
    def get_insights_list(n_click, insights_type, insight, project, topic):
        if n_click:
            if (insight is not None):
                reviews, summary = get_relevant_reviews_and_llm_summary(project, topic, insights_type, insight)
                reviews_list = [html.H6("Relevant Reviews:\n\n")]
                idx = 0
                for review in reviews:
                    idx = idx + 1
                    reviews_list.append(html.P(f"{idx}. {review}\n"))
                return reviews_list, [html.H6("Summary:\n"), html.P(summary)]
        return [], empty_element()          


 