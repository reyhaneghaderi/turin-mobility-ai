from pathlib import Path

import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHUNKS_FILE = PROJECT_ROOT / "data" / "rag" / "chunks.csv"

EMBEDDINGS_FILE = PROJECT_ROOT / "data" / "rag" / "embeddings.npy"


# Load embedding model
model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def create_embeddings():

    # Load chunks
    chunks_df = pd.read_csv(CHUNKS_FILE)

    all_embeddings = []

    for i in range(len(chunks_df)):

        # Get chunk text
        chunk_text = chunks_df.loc[i, "text"]

        # Create embedding
        embedding = model.encode(chunk_text)

        # Save embedding
        all_embeddings.append(embedding)

        print(
            "Created embedding for:",
            chunks_df.loc[i, "source"],
            "- Chunk",
            chunks_df.loc[i, "chunk_number"]
        )

    # Convert list to numpy array
    all_embeddings = np.array(all_embeddings)

    # Save embeddings
    np.save(
        EMBEDDINGS_FILE,
        all_embeddings
    )

    print()
    print("Number of chunks:", len(chunks_df))
    print("Number of embeddings:", len(all_embeddings))
    print("Embeddings saved to:")
    print(EMBEDDINGS_FILE)

    return all_embeddings


if __name__ == "__main__":
    create_embeddings()