# RAG Application with LangChain & Mistral AI

## Features
- **Ingestion**: PDF/Markdown support with token-based chunking (500 tokens, 75 overlap) and deterministic ID upserts (idempotent).
- **Retrieval**: ChromaDB vector store with metadata filtering.
- **Generation**: Mistral AI with strict context adherence (refuses to hallucinate).
- **Evaluation**: Automated metrics (Recall@K, MRR, nDCG, LLM-judge).

## Installation
1. `python -m venv .venv && .venv\Scripts\activate`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your `MISTRAL_API_KEY`.

## Usage
**1. Ingest a Document:**
`python -c "from app.ingestion.pipeline import ingest_file; ingest_file('data/rag_handbook.pdf')"`

**2. Start the API:**
`uvicorn app.api.main:app --reload`
Navigate to `http://localhost:8000/docs` to test the `/query` endpoint.

**3. Run Evaluation:**
`python -m app.evaluation.run_eval`
Results are saved in `results/eval_results.json`.

## Trade-offs and Limitations
- **Chunking:** Fixed token chunking (500/75) works generally but may split context on highly structured tables.
- **Embeddings:** Local MiniLM model is fast and free but less nuanced than OpenAI's `text-embedding-3-large`.
- **When to switch to Managed DB:** If vectors exceed 1 million, or if multi-region replication/automated backups are required, switch to Pinecone or Qdrant Cloud.