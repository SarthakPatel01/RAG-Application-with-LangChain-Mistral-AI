from app.ingestion.pipeline import get_vectorstore
from app.config import TOP_K

def retrieve(query: str, source_filter: str = None, k: int = TOP_K):
    """
    Retrieves the top-k most relevant document chunks for a given query.
    
    Args:
        query (str): The user's question or search string.
        source_filter (str, optional): Filter to search only within a specific document 
                                       (e.g., "rag_handbook.pdf"). Defaults to None.
        k (int): The number of chunks to retrieve. Defaults to the TOP_K env variable.
        
    Returns:
        List[Document]: A list of LangChain Document objects containing the text 
                        and metadata (source, page, chunk_id).
    """
   
    store = get_vectorstore()
    
  
    search_kwargs = {"k": k}
    
  
    if source_filter:
        search_kwargs["filter"] = {"source": source_filter}
        
    
    retriever = store.as_retriever(
        search_type="similarity", 
        search_kwargs=search_kwargs
    )
    
   
    documents = retriever.invoke(query)
    
    return documents