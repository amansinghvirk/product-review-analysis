import os
import re
import json
from json import JSONDecodeError

def parse_json_output(response):

    try:
        json_response = response.replace("```json", "").replace("```", "")
        return json.loads(json_response)
    except JSONDecodeError:
        print("Error parasing json")
        return None

def create_cache_if_not_exists():
    if not os.path.exists(".cache"):
        os.mkdir(".cache")

def create_project_cache_if_not_exists(project):
    if not os.path.exists(os.path.join(".cache", project)):
        os.mkdir(os.path.join(".cache", project))

def create_cache_topic_if_not_exists(project: str, topic: str) -> bool:
    create_cache_if_not_exists()

    topic_cache_path = os.path.join(".cache", project, topic)

    try:
        if not os.path.exists(topic_cache_path):
            os.mkdir(topic_cache_path)
        return True
    except Exception as e:
        print(e)
        return False

def get_insights_cache_file_name(insights_type, project, topic):
    if insights_type == "Negative Insights":
        label = "negative.txt"
    elif insights_type == "Positive Insights":
        label = "positive.txt"
    elif insights_type == "Suggestions":
        label = "suggestions.txt"
    else:
        return None

    return os.path.join(".cache", project, topic, label)

def get_insight_reviews_cache_file_name(project, topic, insight):

    pattern = re.compile(r'[^a-zA-Z0-9\s]+')
    insight =  pattern.sub("", insight)
    insight = insight.replace(" ", "")

    label = insight[:12] + insight[-12:]
    filename = os.path.join(".cache", project, topic, label.strip()) + "reviews.txt"

    return filename

def get_insight_summary_cache_file_name(project, topic, insight):

    pattern = re.compile(r'[^a-zA-Z0-9\s]+')
    insight =  pattern.sub("", insight)
    insight = insight.replace(" ", "")

    label = insight[:12] + insight[-12:]
    filename = os.path.join(".cache", project, topic, label.strip() + "summary.txt") 

    return filename
    


    
