from langchain_text_splitters import TokenTextSplitter
import tiktoken

def split_documents(docs, chunk_size=500, overlap=75):
    splitter = TokenTextSplitter(
        encoding_name="cl100k_base",
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )
    return splitter.split_documents(docs)