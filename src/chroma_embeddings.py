"""
module: chroma_embeddings.py
author: Amandeep Singh
last modified: 14-Apr-2024

functions:
    gen_embeddings_for_listings:
        - generate and load embeddings for the listings

    store_embeddings_to_chroma:
        - store embeddings to the vector database
    
    query_vector_store:
        - fetch the recommendation based on user query

"""

import os
import shutil
import uuid
import json
import chromadb
import pandas as pd
from pathlib import Path
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb.utils.embedding_functions as embedding_functions
from langchain_openai import OpenAIEmbeddings


def gen_embeddings_for_listings(
    review_file_path="data/reviews.csv", 
    collection_name="customer_reviews"
):

    examples = pd.read_csv(review_file_path).text.tolist()
    store_embeddings_to_chroma(
        examples=examples, 
        collection_name=collection_name
    )    

def query_vector_store(
    query, 
    collection_name="customer_reviews"
):

    embeddings = OpenAIEmbeddings()
    persistent_client = chromadb.PersistentClient()
    langchain_chroma = Chroma(
        client=persistent_client,
        collection_name=collection_name,
        embedding_function=embeddings,
    )

    docs = langchain_chroma.similarity_search(query)

    return docs

def load_docs(reviews_file_path):

    examples = pd.read_csv(review_file_path).text.tolist()

    return examples

def store_embeddings_to_chroma(examples, collection_name):

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    model_name="text-embedding-ada-002"
                )

    try:
        shutil.rmtree("./chroma")
    except:
        pass

    persistent_client = chromadb.PersistentClient()

    collection = persistent_client.get_or_create_collection(
        collection_name,
        embedding_function=openai_ef)

    for example in examples:
        collection.add(
            ids=[str(uuid.uuid1())],  documents=example
        )

