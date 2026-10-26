from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from app.config import MISTRAL_API_KEY

JUDGE_PROMPT = """You are an evaluator. Given a question, an answer, and the retrieved context, score the following on a 1-5 scale:
1. Faithfulness: Is every claim in the answer supported by the context? (1=hallucinated, 5=fully grounded)
2. Answer Relevance: Does the answer address the question? (1=irrelevant, 5=perfect)
Return ONLY a JSON: {{"faithfulness": <int>, "relevance": <int>}}

Question: {question}
Answer: {answer}
Context: {context}"""

def judge_answer(question, answer, context):
    llm = ChatMistralAI(model="mistral-small-latest", temperature=0, mistral_api_key=MISTRAL_API_KEY)
    prompt = ChatPromptTemplate.from_template(JUDGE_PROMPT)
    chain = prompt | llm
    import json
    resp = chain.invoke({"question": question, "answer": answer, "context": context})
    return json.loads(resp.content)