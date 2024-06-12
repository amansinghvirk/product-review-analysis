"""
module: app_plots.py
author: Amandeep Singh
created on: 09-Jun-2024
last modified on: 09-Jun-2024

Module contains all the app visualization functions 

"""

import plotly.graph_objects as go
from src.app_functions import load_data


def topics_sentiment_plot(project: str) -> go.Figure:
    """
    Returns the horizontal stacked bar chart visualizing the sentiment distribution
    of all the topics in a project

    Args:
        - project (str): Name of the project, this will be used to load the data for the project
    
    """

    analysis_df = load_data(project)
    topics_sentiment_df = analysis_df.groupby(
        ["predicted", "sentiment"]
    ).size().reset_index(name="count")
    topics_sentiment_df.columns = ["topic", "sentiment", "count"]
    topics_sentiment_df["topic_count"] = (
        topics_sentiment_df.groupby("topic")["count"].transform("sum")
    )
    topics_sentiment_df["sentiment_pct"] = round(
        (topics_sentiment_df["count"] / topics_sentiment_df["topic_count"]) * 100
    , 1)
    topics_sentiment_df.topic = topics_sentiment_df.topic.apply(lambda x: x + " ")
    fig = go.Figure()

    sentiment_colors = {
        "positive": '#0af244', 
        "neutral": '#d1e09d',
        "negative": '#e8371c'
    }

    # Iterate over each topic
    for sentiment in topics_sentiment_df['sentiment'].unique():
        # Filter the DataFrame for the current topic
        topic_df = topics_sentiment_df[topics_sentiment_df['sentiment'] == sentiment]

        
        # Create a stacked bar trace for each sentiment
        fig.add_trace(go.Bar(
            x=topic_df['sentiment_pct'],
            y=topic_df['topic'],
            name=sentiment,
            textposition='auto',
            hovertemplate='Sentiment: ' + sentiment + '<br>' +
                        'Percentage of topics: %{x}%<br>' +
                        'Topic: %{y}',
            marker=dict(
                color=sentiment_colors[sentiment],
                line=dict(color=sentiment_colors[sentiment], width=1)),
            orientation='h',
            opacity=0.8
        ))

    # Set the layout of the figure
    fig.update_layout(
        yaxis=None,
        xaxis=None,
        barmode='stack',
        showlegend=True,
        legend=dict(title='Sentiment'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#f9e1c7",
        margin=go.layout.Margin(
            l=0, #left margin
            r=0, #right margin
            b=0, #bottom margin
            t=0  #top margin
        )
    )

    return fig


    