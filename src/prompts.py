
"""
module: prompts.py
author: Amandeep Singh
created on: 09-Jun-2024
last modified on: 09-Jun-2024

Module contains functions which serves as prompt templates. 

"""

def prompt_template_for_insights(topic: str, reviews: list, sentiment: str, n_points: int) -> dict:

    template = f"""Detect {n_points} key points from the reviews related to {topic} topic:
    ### INSTRUCTIONS: ###
        - Reviews are listed in REVIEWS section and enclosed by triple quotes
        - Analyze the reviews for their {sentiment} sentiments.
        - Detect {n_points} key points mentioned by customers with relevance to the {sentiment} sentiment
        - All the reviews are related to {topic} topic so detected key points should be relevant to the {topic} topic.
        - Sort the extracted points from most relevant to least relavant based on {sentiment} sentiment
        - Return the result in JSON format where key should be `key points` and extracted points as list sorted 
          from most relevant to least relvant
        - example of result is provided below:
            "key points": [
                "key insight 1",
                "key insight 2"
            ]

    REVIEWS: ```{reviews}```
    """


    prompt = {
        "role": "system",
        "content": "You are an expert business analytics consultant by generating insights and suggestions!",
        "role": "user",
        "content": template
    }

    return prompt


def prompt_template_for_suggestion(topic: str, reviews: list, n_points: int) -> dict:

    template = f"""Detect {n_points} key suggestions to improve the business from the reviews related to {topic} topic:
    ### INSTRUCTIONS: ###
        - Reviews are listed in REVIEWS section and enclosed by triple quotes
        - Analyze the reviews for their mixed sentiments.
        - Detect {n_points} suggestions based on reivews related to {topic} topic.
        - Suggestions should be based on what should be continue, what can be improved, any focused areas.
        - Sort the extracted points from most relevant to least relavant based
        - Return the result in JSON format where key should be `suggestions` and extracted points as list sorted 
          from most relevant to least relvant
        - example of result is provided below:
            "suggestions": [
                "key insight 1",
                "key insight 2"
            ]

    REVIEWS: ```{reviews}```
    """


    prompt = {
        "role": "system",
        "content": "You are an expert business analytics consultant by generating insights and suggestions!",
        "role": "user",
        "content": template
    }

    return prompt


def prompt_template_for_summary(topic: str, reviews: list) -> dict:

    template = f"""Summarize the customer reviews to improve the business from the reviews related to {topic} topic:
    ### INSTRUCTIONS: ###
        - Reviews are listed in REVIEWS section and enclosed by triple quotes
        - Summarize the reviews, summary should include highlighted point, sentiments, feedback and suggestion.
        - Return the result in JSON format where key should be `summary` and extracted points as list sorted 
          from most relevant to least relvant
        - Summary should be short and concise not more than 30 words.
        - example of result is provided below:
            "summary": "Summary of all the reviews"

    REVIEWS: ```{reviews}```
    """


    prompt = {
        "role": "system",
        "content": "You are an expert business analytics consultant by generating insights and suggestions!",
        "role": "user",
        "content": template
    }

    return prompt