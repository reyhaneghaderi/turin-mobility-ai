from src.rag.generator import client


def choose_tool(question):

    prompt = f"""
Choose the correct source for the user's question.

DOCUMENT:
Use for information from official documents:
- parking prices and tariffs
- parking hours
- ZTL rules
- traffic restrictions
- permits and regulations

DATA:
Use for information from PostgreSQL:
- available parking spaces
- parking occupancy
- traffic speed
- traffic flow
- historical traffic or parking data

BOTH:
Use when the question needs both DOCUMENT and DATA.

UNKNOWN:
Use when the question cannot be answered
from the documents or PostgreSQL data.

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