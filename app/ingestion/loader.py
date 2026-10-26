from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, UnstructuredHTMLLoader, TextLoader
import markdown

SUPPORTED = {".pdf": PyPDFLoader, ".html": UnstructuredHTMLLoader, ".htm": UnstructuredHTMLLoader, ".md": TextLoader}

def load_document(path: Path):
    ext = path.suffix.lower()
    if ext not in SUPPORTED:
        raise ValueError(f"Unsupported: {ext}")
    loader = SUPPORTED[ext](str(path))
    docs = loader.load()
    # For markdown, convert to plain text
    if ext == ".md":
        for d in docs:
            d.page_content = markdown.markdown(d.page_content)
    return docs