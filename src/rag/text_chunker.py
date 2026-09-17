from pathlib import Path

import pandas as pd
import tiktoken

from .pdf_loader import pdf_files, extract_pdf_text
from .text_cleaner import clean_text


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = PROJECT_ROOT / "data" / "rag" / "chunks.csv"


# Tokenizer
encoding = tiktoken.get_encoding("cl100k_base")


# Chunk settings
CHUNK_SIZE = 100
CHUNK_OVERLAP = 20


def create_chunks():

    all_chunks = []

    for pdf_path in pdf_files:

        # 1. Extract raw text from PDF
        raw_text = extract_pdf_text(pdf_path)

        # 2. Clean text
        cleaned_text = clean_text(raw_text)

        # 3. Convert text to tokens
        tokens = encoding.encode(cleaned_text)

        print("PDF:", pdf_path.name)
        print("Cleaned tokens:", len(tokens))

        start = 0
        chunk_number = 1

        # 4. Create chunks
        while start < len(tokens):

            end = start + CHUNK_SIZE

            # Take tokens for this chunk
            chunk_tokens = tokens[start:end]

            # Convert tokens back to text
            chunk_text = encoding.decode(chunk_tokens)

            # Save chunk
            all_chunks.append({
                "source": pdf_path.name,
                "chunk_number": chunk_number,
                "token_count": len(chunk_tokens),
                "text": chunk_text
            })

            # Move forward keeping overlap
            start = start + CHUNK_SIZE - CHUNK_OVERLAP

            chunk_number = chunk_number + 1

    # Convert chunks to DataFrame
    chunks_df = pd.DataFrame(all_chunks)

    # Create output folder if necessary
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save chunks
    chunks_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("Total chunks:", len(chunks_df))
    print("Chunks saved to:")
    print(OUTPUT_FILE)

    return chunks_df


if __name__ == "__main__":
    create_chunks()