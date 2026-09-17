import os

from dotenv import load_dotenv
from openai import OpenAI

from .retriever import search_documents


# Load environment variables
load_dotenv()


# Get OpenRouter API key
api_key = os.getenv("OPENROUTER_API_KEY")


# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


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

Give a short and direct answer.
"""

    return prompt


def answer_question(question):

    # Find relevant chunks
    top_results = search_documents(question)

    # Combine chunks
    context = "\n\n".join(
        top_results["text"].tolist()
    )

    # Build prompt
    prompt = build_prompt(
        question,
        context
    )

    # Send prompt to LLM
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Get answer
    answer = response.choices[0].message.content

    return answer