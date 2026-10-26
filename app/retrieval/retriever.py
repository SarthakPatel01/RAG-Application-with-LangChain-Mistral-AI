from app.ingestion.pipeline import get_vectorstore
from app.config import TOP_K

def retrieve(query: str, source_filter: str = None, k: int = TOP_K):
    store = get_vectorstore()
    search_kwargs = {"k": k}
    if source_filter:
        search_kwargs["filter"] = {"source": source_filter}
    retriever = store.as_retriever(search_type="similarity", search_kwargs=search_kwargs)
    return retriever.invoke(query)