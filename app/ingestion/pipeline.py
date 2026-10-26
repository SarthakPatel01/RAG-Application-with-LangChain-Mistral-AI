import hashlib
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.config import *
from .loader import load_document
from .splitter import split_documents
from functools import lru_cache




@lru_cache(maxsize=1)
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": EMBEDDING_DEVICE},
        encode_kwargs={"normalize_embeddings": True},
    )

def get_vectorstore():
    return Chroma(
        collection_name=CHROMA_COLLECTION,
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=get_embeddings(),
    )

def chunk_id(doc, index):
    """Deterministic ID: file path + chunk index + content hash for idempotency."""
    raw = f"{doc.metadata.get('source','')}_{index}_{doc.page_content[:100]}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def ingest_file(file_path: str):
    path = Path(file_path)
    docs = load_document(path)
    # Enrich metadata
    for d in docs:
        d.metadata["source"] = path.name
        if "page" not in d.metadata:
            d.metadata["page"] = 0

    chunks = split_documents(docs, CHUNK_SIZE, CHUNK_OVERLAP)
    ids = [chunk_id(c, i) for i, c in enumerate(chunks)]

    # Add chunk index to metadata
    for i, c in enumerate(chunks):
        c.metadata["chunk_id"] = ids[i]
        c.metadata["chunk_index"] = i

    store = get_vectorstore()
    store.add_documents(documents=chunks, ids=ids)  # upsert semantics with same IDs
    print(f"Ingested {len(chunks)} chunks from {path.name}")