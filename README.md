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

* **Limited RAG knowledge base:** The assistant currently uses only 3 Turin mobility documents, so questions outside this scope may not be answered.

* **Limited historical data:** The PostgreSQL database currently contains about 7 days of traffic and parking history, which limits long-term trend analysis and forecasting.

* **No predictive ML model yet:** The current system focuses on real-time data, analytics, RAG, and AI-assisted queries rather than traffic or parking prediction.

* **No dedicated vector database:** Because the RAG knowledge base is still small, embeddings are searched directly using similarity search. A vector database could be added as the document collection grows.

* **Dependence on external services:** Real-time traffic and parking data come from the **5T Torino Open Data APIs**, while AI responses use the **OpenRouter free LLM API**. Temporary downtime, rate limits, or service changes may affect availability.

* **Prototype deployment:** The application is designed as a working portfolio prototype rather than a production-grade system. A production version would require stronger monitoring, testing, security, logging, and failure recovery.


## Tech Stack

Python · Pandas · NumPy · PostgreSQL · SQL · Requests · XML · PyPDF · tiktoken · Sentence Transformers · scikit-learn · RAG · LLM · Prompt Engineering

## Author

Reyhaneh Ghaderi Chermahini

GitHub: https://github.com/reyhanehghaderi  
LinkedIn: https://linkedin.com/in/reyhanehghaderi
