from src.rag.generator import client, answer_question
from src.agent.decision import choose_tool, split_question
from src.agent.sql_tool import data_tool


def run_agent(question):

    # Decide which source should answer the question
    decision = choose_tool(question)

    print("Tool selected:", decision)


    # Question about documents
    if decision == "DOCUMENT":

        answer = answer_question(question)


    # Question about PostgreSQL data
    elif decision == "DATA":

        answer = data_tool(question)


    # Question needs both documents and database
    elif decision == "BOTH":

        # Split the question into two parts
        document_question, data_question = split_question(question)

        # Answer document part
        document_answer = answer_question(
            document_question
        )

        # Answer database part
        data_answer = data_tool(
            data_question
        )

        # Combine both results
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


    # Question is outside available sources
    else:

        answer = (
            "I don't have enough information in the current data sources "
            "to answer this question."
        )


    return answer