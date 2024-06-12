"""
module: app_functions.py
author: Amandeep Singh
created on: 09-Jun-2024
last modified on: 09-Jun-2024

Module contains all the functions which are called by the callbacks. This module works as route
to the llm calls and llm processing functions. 

"""


import os
import pandas as pd

from src.insights import get_insights, get_suggestions, get_summary
from src.chroma_embeddings import query_vector_store
from src.utils import (
    create_cache_if_not_exists, 
    create_project_cache_if_not_exists,
    create_cache_topic_if_not_exists, 
    get_insights_cache_file_name,
    get_insight_reviews_cache_file_name,
    get_insight_summary_cache_file_name
)

LLM_MODEL = "gpt-4-turbo-preview"

def get_projects_list() -> list:
    """Returns the list of the projects available"""

    data_dir = "data"
    if not os.path.exists(data_dir):
        return None

    projects = [
        project for project in os.listdir(data_dir) 
        if os.path.isdir(os.path.join(data_dir, project))
    ]

    return projects

def load_data(project: str, data_dir: str="data") -> pd.DataFrame:
    """Loads the project data
    
    Args:
        project (str): Name of the project
        data_dir (str) default="data": path of the project data
    
    Returns
        Pandas dataframe

    """

    review_file = os.path.join(data_dir, project, "reviews.csv")
    predicted_sentiments_file = os.path.join(data_dir, project, "predicted_sentiments.csv")
    predicted_topics_file = os.path.join(data_dir, project, "predicted_topics.csv")

    reviews_df = pd.read_csv(review_file)
    sentiments_df = pd.read_csv(predicted_sentiments_file)
    topics_df = pd.read_csv(predicted_topics_file)

    analysis_df = pd.merge(
        left=reviews_df,
        right=sentiments_df.loc[:, ["id", "sentiment", "sentiment_score"]],
        on=["id"],
        how="inner"
    )

    analysis_df = pd.merge(
        left=topics_df,
        right=analysis_df,
        on=["id"],
        how="inner"
    )

    return analysis_df

def get_topics(project: str) -> list:
    """Loads the data of the project and return list of the topics,
    available in the project

    Args:
        project (str): Name of the project to load the data for that project

    Returns:
        list of the topics in the project
    
    """

    df = load_data(project)

    topics = list(df.loc[df.predicted.isna() == False, :].predicted.unique())

    topics = [topic for topic in topics if topic != "null"]

    return topics



def get_reviews_to_generate_insights(
    project: str, 
    sentiment: str, 
    topic: str, 
    n_reviews=10
) -> pd.DataFrame:
    """Returns the sample set of reviews for the topic and based on sentiment

    Args:
        - project (str): Name of the project
        - sentiment (str): type of the sentiment (negative/positive/neutral)
        - topic (str): topic name to get the reviews for that topic
        - n_reviews (int) default=10: Number of reviews to be returned

    Return:
        list: list of review text selected based on parameters
    """

    df = load_data(project)

    reviews = (
        df.loc[(
            (df.predicted == topic) 
            & (df.sentiment == sentiment))
        , :]
        .sort_values("sentiment_score", ascending=False)
        .head(n_reviews)
        .text
        .tolist()
    )

    return reviews

def review_insights(
    project: str, 
    topic: str, 
    llm_model: str, 
    sentiment="negative"
):

    create_project_cache_if_not_exists(project)
    create_cache_topic_if_not_exists(project, topic)
    cache_file = os.path.join(".cache", project, topic, f"{sentiment}.txt")

    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            insights = f.readlines()

    else:
        data = load_data(project)
        reviews = get_reviews_to_generate_insights(project, sentiment, topic, 20)

        insights = get_insights(
            topic=topic, 
            reviews=reviews, 
            sentiment=sentiment, 
            llm_model=llm_model, 
            n_points=5
        )

        with open(cache_file, "w") as f:
            for insight in insights:
                f.write(str(insight) + "\n")

    return insights


def review_suggestions(project, topic, llm_model):

    create_project_cache_if_not_exists(project)
    create_cache_topic_if_not_exists(project, topic)
    cache_file = os.path.join(".cache", project, topic, "suggestions.txt")

    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            suggestions = f.readlines()

    else:
        data = load_data(project)
        reviews = []
        reviews.append(get_reviews_to_generate_insights(project, "positive", topic, 10))
        reviews.append(get_reviews_to_generate_insights(project, "negative", topic, 10))
        reviews.append(get_reviews_to_generate_insights(project, "neutral", topic, 10))

        suggestions = get_suggestions(
            topic=topic, 
            reviews=reviews,  
            llm_model=llm_model, 
            n_points=5
        )

        with open(cache_file, "w") as f:
            for insight in suggestions:
                f.write(str(insight) + "\n")

    return suggestions

def review_summary(project, topic, reviews, llm_model):

    create_project_cache_if_not_exists(project)
    create_cache_topic_if_not_exists(project, topic)
    cache_file = os.path.join(".cache", project, topic, "suggestions.txt")

    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            summary = f.readlines()
    summary = get_summary(
        topic=topic, 
        reviews=reviews,  
        llm_model=llm_model
    )

    return summary

def get_topic_insights_for_exploration(project: str, topic: str, insights_type: str) -> list:


    cache_file = get_insights_cache_file_name(insights_type, project, topic)

    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            suggestions = f.readlines()
        return suggestions
    else:
        return None

def get_relevant_reviews(query, collection_name):
    docs = result = query_vector_store(query, collection_name)
    reviews = []

    for doc in docs: 
        reviews.append(doc.page_content)

    return reviews

def get_relevant_reviews_and_llm_summary(
    project: str, 
    topic: str, 
    insights_type: str, 
    insight: str
):

    reviews_cache_file = get_insight_reviews_cache_file_name(project, topic, insight)
    summary_cache_file = get_insight_summary_cache_file_name(project, topic, insight)

    if not os.path.exists(reviews_cache_file):
        reviews = get_relevant_reviews(insight, project)
        with open(reviews_cache_file, "w") as f:
            for review in reviews:
                f.write(str(review) + "\n")
    else:
        with open(reviews_cache_file, "r") as f:
            reviews = f.readlines()

    if not os.path.exists(summary_cache_file):
        summary = review_summary(project, topic, reviews)
        with open(summary_cache_file, "w") as f:
            for point in summary:
                f.write(str(point) + "\n")
    else:
        with open(summary_cache_file, "r") as f:
            summary = f.readlines()

    return reviews, summary

    
