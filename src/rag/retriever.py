from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from .embeddings import model


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHUNKS_FILE = PROJECT_ROOT / "data" / "rag" / "chunks.csv"

EMBEDDINGS_FILE = PROJECT_ROOT / "data" / "rag" / "embeddings.npy"


# Load chunks
chunks_df = pd.read_csv(CHUNKS_FILE)


# Load embeddings
all_embeddings = np.load(EMBEDDINGS_FILE)


def search_documents(question):

    # Convert question to embedding
    question_embedding = model.encode(question)

    # Compare question with all document chunks
    similarities = cosine_similarity(
        [question_embedding],
        all_embeddings
    )[0]

    # Copy chunk table
    results_df = chunks_df.copy()

    # Add similarity scores
    results_df["similarity"] = similarities

    # Select top 3 results
    top_results = results_df.sort_values(
        "similarity",
        ascending=False
    ).head(3)

    return top_results