import os

import psycopg2
from dotenv import load_dotenv

from src.rag.generator import client


# Load variables from .env
load_dotenv()


# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)


def data_tool(question):

    # Database structure
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


    # Ask LLM to create SQL
    prompt = f"""
Write a PostgreSQL query to answer the user's question.

Database schema:

{schema}

Rules:
- Use only the tables and columns listed above.
- Return only SQL.
- Use only SELECT or WITH queries.
- Never modify the database.
- Ignore NULL values when comparing numeric values.
- For current parking information use parking_locations.
- For current traffic information use traffic_locations.
- For historical parking information use parking_observations.
- For historical traffic information use traffic_observations.

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


    # Get generated SQL
    sql = response.choices[0].message.content.strip()


    # Remove markdown if LLM returns ```sql
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()


    print("Generated SQL:")
    print(sql)


    # Safety check
    if not (
        sql.upper().startswith("SELECT")
        or sql.upper().startswith("WITH")
    ):
        return "Unsafe SQL query."


    # Run SQL
    cursor = conn.cursor()

    try:

        cursor.execute(sql)

        rows = cursor.fetchall()

        columns = [
            column[0]
            for column in cursor.description
        ]

        result = [
            dict(zip(columns, row))
            for row in rows
        ]

    except Exception as error:

        conn.rollback()

        result = f"Database error: {error}"

    finally:

        cursor.close()


    return result