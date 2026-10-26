import time, logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.qa.chain import build_qa_chain
from app.config import TOP_K

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Mistral")
qa_func = build_qa_chain()

class QueryRequest(BaseModel):
    question: str
    source_filter: str | None = None
    top_k: int = TOP_K

class Source(BaseModel):
    source: str
    page: int | str
    chunk_id: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]
    latency_ms: float
    retrieved_count: int

@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    start = time.perf_counter()
    result = qa_func(req.question, source_filter=req.source_filter)
    elapsed = (time.perf_counter() - start) * 1000

    # Token usage estimate (optional; Mistral SDK may provide usage)
    # For simplicity, log approximate
    logger.info(f"query='{req.question[:60]}...', latency={elapsed:.1f}ms, chunks={len(result['sources'])}")

    return QueryResponse(
        answer=result["answer"],
        sources=result["sources"],
        latency_ms=elapsed,
        retrieved_count=len(result["sources"]),
    )

@app.get("/health")
def health():
    return {"status": "ok"}