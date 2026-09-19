# Turin Mobility AI Assistant

An end-to-end Data & GenAI prototype that combines Turin traffic and parking data with official mobility documents to answer natural-language questions.

🔗 **Live Demo:** [turin-mobility-ai-assistant.streamlit.app](https://turin-mobility-ai-assistant.streamlit.app)
### Project Management

Development was tracked through a structured project plan covering
data engineering, PostgreSQL, analytics, RAG, AI agent development,
evaluation, and deployment.

📊 [View the project tracker](docs/Turin_Mobility_AI_Project_Tracker.xlsx)
## Business Problem

Mobility information is spread across different sources. A driver may need to check traffic, parking availability, parking rules, ZTL access, and vehicle restrictions before making a simple decision.

This project brings these sources together in one AI assistant.

## What the System Does

The system can answer questions about:

- current traffic speed and flow
- parking availability
- recent historical mobility data
- parking prices and payment hours
- ZTL rules
- vehicle restrictions
- questions that need both database data and official documents

## Architecture

`5T APIs → Python Data Processing → PostgreSQL`

`Official PDFs → Cleaning → Chunking → Embeddings → Semantic Search → RAG`

`User Question → LLM Router → DOCUMENT / DATA / BOTH / UNKNOWN → Final Answer`

## Data and AI

Traffic and parking data are collected from 5T APIs and processed with Python.

Structured mobility data is queried with PostgreSQL and SQL.

Official documents are processed with PDF text extraction, tokenization, chunking, multilingual SentenceTransformer embeddings, cosine similarity, and RAG.

The LLM is used for question routing, SQL generation, and final answer generation.

## Example Questions

- How many free spaces are available at Porta Nuova?
- What is the current traffic speed on Corso Francia?
- How much does parking cost in the Central ZTL?
- Are Diesel Euro 4 vehicles restricted?
- Can I enter the ZTL and find available parking?

## Current Limitations

- 3 documents in the RAG knowledge base
- about 7 days of historical data
- no predictive ML model yet
- no dedicated vector database
- no production deployment yet

## Tech Stack

Python · Pandas · NumPy · PostgreSQL · SQL · Requests · XML · PyPDF · tiktoken · Sentence Transformers · scikit-learn · RAG · LLM · Prompt Engineering

## Author

Reyhaneh Ghaderi Chermahini

GitHub: https://github.com/reyhanehghaderi  
LinkedIn: https://linkedin.com/in/reyhanehghaderi
