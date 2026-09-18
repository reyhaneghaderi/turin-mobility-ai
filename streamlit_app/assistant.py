import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import psycopg2
import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# Environment variables
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")


# --------------------------------------------------
# OpenRouter client
# --------------------------------------------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


# --------------------------------------------------
# PostgreSQL connection
# --------------------------------------------------
# Create a NEW connection whenever a database
# question is received.
# This avoids stale connections in Streamlit Cloud.
# --------------------------------------------------

def get_db_connection():

    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        sslmode="require"
    )


# --------------------------------------------------
# Project paths
# --------------------------------------------------

base_dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

chunks_path = os.path.join(
    base_dir,
    "data",
    "rag",
    "chunks.csv"
)

embeddings_path = os.path.join(
    base_dir,
    "data",
    "rag",
    "embeddings.npy"
)


# --------------------------------------------------
# Load RAG data
# --------------------------------------------------

chunks_df = pd.read_csv(chunks_path)

all_embeddings = np.load(embeddings_path)


# --------------------------------------------------
# Embedding model
# --------------------------------------------------

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


# --------------------------------------------------
# Router
# --------------------------------------------------

def choose_tool(question):

    prompt = f"""
Choose the correct source for the user's question.

DOCUMENT:
Use for parking prices, parking hours, ZTL rules,
traffic restrictions, permits and regulations.

DATA:
Use for parking availability, parking occupancy,
traffic speed, traffic flow and historical data.

BOTH:
Use when both documents and database data are needed.

UNKNOWN:
Use when the question cannot be answered
from the documents or database.

Question:
{question}

Answer only:
DOCUMENT
DATA
BOTH
or
UNKNOWN
"""

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    decision = response.choices[0].message.content.strip()

    return decision


# --------------------------------------------------
# PostgreSQL / Natural-language-to-SQL tool
# --------------------------------------------------

def data_tool(question):

    schema = """
parking_locations:
name, id, status, total, free, tendance, lat, lng, collected_at

parking_observations:
observation_id, parking_id, status, free, tendance, collected_at

traffic_locations:
sensor_id, road_name, direction, lat, lng, period,
flow, speed, road_id, offset, collected_at

traffic_observations:
observation_id, sensor_id, direction, offset,
period, flow, speed, collected_at
"""

    prompt = f"""
Write a PostgreSQL query to answer the user's question.

Database:

{schema}

Rules:
- Use only these four tables.
- Return only SQL.
- Use only SELECT or WITH.
- Never modify the database.
- Ignore NULL values when comparing or ranking numeric values.
- For parking availability, use free IS NOT NULL.
- For current parking data, use parking_locations.
- For current traffic data, use traffic_locations.
- For historical data, use the observation tables.

Question:
{question}
"""

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()


    # --------------------------------------------------
    # Basic SQL safety check
    # --------------------------------------------------

    if not (
        sql.upper().startswith("SELECT")
        or sql.upper().startswith("WITH")
    ):

        return "Database error: Only SELECT or WITH queries are allowed."


    # --------------------------------------------------
    # Fresh database connection for each request
    # --------------------------------------------------

    conn = None
    cursor = None

    try:

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute(sql)

        rows = cursor.fetchall()

        columns = [
            column[0]
            for column in cursor.description
        ]

        data = [
            dict(zip(columns, row))
            for row in rows
        ]

        return data


    except Exception as e:

        if conn is not None:

            try:
                conn.rollback()

            except Exception:
                pass

        return f"Database error: {e}"


    finally:

        if cursor is not None:

            try:
                cursor.close()

            except Exception:
                pass


        if conn is not None:

            try:
                conn.close()

            except Exception:
                pass


# --------------------------------------------------
# Document semantic search
# --------------------------------------------------

def search_documents(question):

    question_embedding = model.encode(question)

    similarities = cosine_similarity(
        [question_embedding],
        all_embeddings
    )[0]

    results_df = chunks_df.copy()

    results_df["similarity"] = similarities

    top_results = results_df.sort_values(
        "similarity",
        ascending=False
    ).head(3)

    return top_results


# --------------------------------------------------
# RAG prompt
# --------------------------------------------------

def build_prompt(question, context):

    prompt = f"""
You are a Turin mobility assistant.

Use only the information provided in the context below.
Do not use outside knowledge or invent information.

Ignore context that is not relevant to the user's question.

If the context does not contain enough information to answer,
say that you do not have enough information.

Answer only what the user asks.
Answer in the same language as the user's question.
Keep the answer short, clear, and direct.

Context:
{context}

Question:
{question}
"""

    return prompt


# --------------------------------------------------
# Document question answering
# --------------------------------------------------

def answer_question(question):

    top_results = search_documents(question)

    context = "\n\n".join(
        top_results["text"].tolist()
    )

    prompt = build_prompt(
        question,
        context
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    return answer


# --------------------------------------------------
# Split BOTH question
# --------------------------------------------------

def split_question(question):

    prompt = f"""
Split the user's question into two parts.

DOCUMENT:
The part about rules, prices, ZTL, restrictions,
parking rules, permits or regulations.

DATA:
The part about traffic or parking measurements
stored in PostgreSQL.

Keep the same language as the user's question.

Question:
{question}

Return exactly:

DOCUMENT: ...
DATA: ...
"""

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    text = response.choices[0].message.content

    document_question = (
        text.split("DOCUMENT:")[1]
        .split("DATA:")[0]
        .strip()
    )

    data_question = (
        text.split("DATA:")[1]
        .strip()
    )

    return document_question, data_question


# --------------------------------------------------
# Main agent
# --------------------------------------------------

def run_agent(question):

    decision = choose_tool(question)


    # --------------------------------------------------
    # DOCUMENT
    # --------------------------------------------------

    if decision == "DOCUMENT":

        answer = answer_question(question)


    # --------------------------------------------------
    # DATA
    # --------------------------------------------------

    elif decision == "DATA":

        answer = data_tool(question)


    # --------------------------------------------------
    # BOTH
    # --------------------------------------------------

    elif decision == "BOTH":

        document_question, data_question = split_question(
            question
        )

        document_answer = answer_question(
            document_question
        )

        data_answer = data_tool(
            data_question
        )

        prompt = f"""
Answer the original question using both results.

Original question:
{question}

Document result:
{document_answer}

Database result:
{data_answer}

Give one clear and short answer.
Answer in the same language as the original question.
"""

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        answer = response.choices[0].message.content


    # --------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------

    elif decision == "UNKNOWN":

        answer = (
            "I do not have information "
            "to answer this question."
        )


    # --------------------------------------------------
    # Unexpected router response
    # --------------------------------------------------

    else:

        answer = "I cannot answer this question."


    return answer