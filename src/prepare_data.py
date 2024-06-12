import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def process_data(
    input_file_path: str, 
    output_file_path: str, 
    sample_rows: int = None
) -> bool:
    """Preprocessing of raw data
    """

    try:
        if sample_rows:
            df = pd.read_csv(
                input_file_path
                , nrows=sample_rows
            )
        else:
            df = pd.read_csv(
                input_file_path
                , nrows=sample_rows
            )

        df_text = df.loc[:, ["reviews.text"]]
        df_text.columns = ["text"]

        df_text["id"] = df_text.index

        df_text.to_csv(output_file_path, index=False)

        return True
    except Exception as e:
        print(e)
        return False

def tag_type_to_reviews(
    reviews_file_path: str,
    topics_file_path: str
) -> bool:

    try:
        topics_df = pd.read_csv(topics_file_path)
        reviews_df = pd.read_csv(reviews_file_path)
        reviews_df = pd.merge(
            left=reviews_df,
            right=topics_df.groupby(["id"]).agg(CNT = ("id", "count")).reset_index(),
            on=["id"],
            how="left"
        )
        reviews_df["type"] = reviews_df.CNT.apply(lambda x: "predict" if np.isnan(x) else "groundtruth" )
        reviews_df = reviews_df.drop(columns=["CNT"])
        
        reviews_df.to_csv(reviews_file_path, index=False)
        return True
    except Exception as e:
        print(e)
        return False


def preprocess_model_data(
    reviews_file_path: str,
    topics_file_path: str,
    modeldata_file_path: str
) -> bool:

    try:
        topics_df = pd.read_csv(topics_file_path)
        reviews_df = pd.read_csv(reviews_file_path)
        df = pd.merge(
            left=topics_df,
            right=reviews_df,
            on=["id"],
            how="inner"
        )
        df = df.groupby(["id", "text"])['topic'].agg(lambda col: ','.join(col)).reset_index()
        #df["topic"] = df.topic.str.split(",")
        df = df.loc[:, ["text", "topic"]]
        df.columns = ["text", "topics"]
        df.to_csv(modeldata_file_path, index=False)
        return True
    except Exception as e:
        print(e)
        return False

def split_data(
    modeldata_file_path: str,
    train_file_path: str,
    test_file_path: str,
    test_size=.1
) -> bool:

    try:
        model_df = pd.read_csv(modeldata_file_path)
        train_df, test_df = train_test_split(model_df, test_size=test_size)

        train_df.to_csv(train_file_path, index=False)
        test_df.to_csv(test_file_path, index=False)

        return True
    except Exception as e:
        print(e)
        return False
