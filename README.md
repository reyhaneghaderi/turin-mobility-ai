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

- English: How much does parking cost per hour in the Central ZTL?
- Italian: Quanto costa il parcheggio all'ora nella ZTL Centrale?
- English: What are the normal hours for paid parking in Turin?
- Italian: Quali sono gli orari normali della sosta a pagamento a Torino?
- English: Can motorcycles park in blue parking spaces without displaying a permit?
- Italian: Le moto possono parcheggiare nelle strisce blu senza esporre un contrassegno?
- English: When are Euro 3 and Euro 4 diesel vehicles restricted from driving in Turin?
- Italian: Quando è vietata la circolazione dei veicoli diesel Euro 3 ed Euro 4 a Torino?
- English: Which vehicles are restricted all year, every day, from midnight to midnight?
- Italian: Quali veicoli sono soggetti a limitazioni tutto l'anno, tutti i giorni, dalle 0 alle 24?
- English: Which parking has the highest occupancy rate?
- Italian: Quale parcheggio ha il tasso di occupazione più alto?
- English: Which parking has the largest total capacity?
- Italian: Quale parcheggio ha la capacità totale più grande?
- English: How many parking locations are currently active and how many are inactive?
- Italian: Quanti parcheggi sono attualmente attivi e quanti sono inattivi?
- English: What is the current average traffic speed across all measurement points?
- Italian: Qual è la velocità media attuale del traffico in tutti i punti di misurazione?
- English: Which roads have high traffic flow but low speed?
- Italian: Quali strade hanno un flusso di traffico elevato ma una velocità bassa?

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
