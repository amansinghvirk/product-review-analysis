
import pandas as pd

from src.topics_extraction import get_topics, get_generalized_topics
from src.sentiments import get_sentiment



def get_sentiments_dataframe(
    df: pd.DataFrame, 
    sentiment_class: list, 
    llm_model: str
) -> pd.DataFrame:
    sentiments_df = pd.DataFrame({c: pd.Series(dtype=t) for c, t in {'id': 'str', 'sentiment': 'str'}.items()})
    for idx in df.index:

        review_id = df.id[idx]
        review = df.text[idx]
        print(f"Processing review {review_id}")

        try:
            sentiment = get_sentiment(review, sentiment_class, llm_model)

            if sentiment:
                sentiments_df = pd.concat(
                    [
                        sentiments_df,
                        pd.DataFrame({
                            'id': [review_id],
                            'sentiment': sentiment.get("Sentiment")
                        })
                    ]
                )


        except Exception as e:
            print(e)
            continue

    return sentiments_df

def get_topics_dataframe(df: pd.DataFrame, llm_model: str) -> tuple:
    topics_df = pd.DataFrame({c: pd.Series(dtype=t) for c, t in {'id': 'str', 'topic': 'str', 'explanation': 'str'}.items()})
    for idx in df.index:

        review_id = df.id[idx]
        review = df.text[idx]
        print(f"Processing review {review_id}")

        try:
            topics = get_topics(review, llm_model)
            if topics:
                review_topic = []
                topic_explanation = []
                for topic, explanation in topics.items():
                    review_topic.append(topic)
                    topic_explanation.append(explanation)
                topics_df = pd.concat([
                    topics_df,
                    pd.DataFrame({
                        'id': [review_id] * len(review_topic),
                        'topic': review_topic,
                        'explanation': topic_explanation
                    })
                ])
        except Exception as e:
            print(e)
            continue

    return topics_df


def get_generalized_topics_dataframe(topics_df: pd.DataFrame, llm_model: str, topics_list: list) -> tuple:

    try:
 
        topics_to_generalize = ""
        for idx in topics_df.index:
            topics_to_generalize = (
                topics_to_generalize 
                + "\n" 
                + f"({topics_df.id[idx]}, {topics_df.topic[idx]} {topics_df.explanation[idx]})"
            )
        gneralized_topics = get_generalized_topics(topics_to_generalize, llm_model, topics_list)


        gneralized_topics_df = pd.DataFrame({
            'id': gneralized_topics.keys(),
            'topic': gneralized_topics.values()
        })

        gneralized_topics_df = gneralized_topics_df.explode("topic")
        gneralized_topics_df["topic"] = gneralized_topics_df.topic.apply(
            lambda topic: topic if topic in topics_list else 'Other'
        )
        gneralized_topics_df["topic"] = gneralized_topics_df.topic.apply(
            lambda topic: "Other" if topic.lower() == "other" else topic
        )

        return gneralized_topics_df
    except Exception as e:
        print(e)
        return None


    