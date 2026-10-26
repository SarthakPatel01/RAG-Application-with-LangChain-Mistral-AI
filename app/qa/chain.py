from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import RetrievalQA
from langchain_core.documents import Document
from app.config import MISTRAL_API_KEY, TOP_K
from app.retrieval.retriever import retrieve

SYSTEM_TEMPLATE = """You are an assistant that answers using ONLY the provided context.
If the context does not contain the answer, say: "I cannot answer from the available documents."
Always cite the source and page numbers from the context.

Context:
{context}"""

def format_context(docs):
    parts = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", "N/A")
        parts.append(f"[{src}, p.{page}]\n{d.page_content}")
    return "\n\n---\n\n".join(parts)

def build_qa_chain():
    llm = ChatMistralAI(
        model="ministral-3b-2512",
        temperature=0.0,
        mistral_api_key=MISTRAL_API_KEY,
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_TEMPLATE),
        ("human", "{question}"),
    ])
  
    def qa(question: str, source_filter: str = None):
        docs = retrieve(question, source_filter=source_filter, k=TOP_K)
        if not docs:
            return {
                "answer": "I cannot answer from the available documents.",
                "sources": [],
            }
        context = format_context(docs)
        chain = prompt | llm
        response = chain.invoke({"context": context, "question": question})
        return {
            "answer": response.content,
            "sources": [
                {"source": d.metadata.get("source"), "page": d.metadata.get("page"), "chunk_id": d.metadata.get("chunk_id")}
                for d in docs
            ],
        }
    return qa