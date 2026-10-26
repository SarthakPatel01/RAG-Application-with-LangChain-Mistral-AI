import json, time
from pathlib import Path
from app.qa.chain import build_qa_chain
from app.retrieval.retriever import retrieve
from .metrics import recall_at_k, mrr, ndcg_at_k, context_precision_at_k
from .judge import judge_answer

def run(test_set_path="evaluation/test_set.json", k=5):
    with open(test_set_path) as f:
        tests = json.load(f)

    qa = build_qa_chain()
    retrieval_latencies = []
    results = []

    for t in tests:
        q = t["question"]
        rel_ids = t.get("relevant_chunk_ids", [])

        # Retrieval timing
        start = time.perf_counter()
        docs = retrieve(q, k=k)
        lat = (time.perf_counter() - start) * 1000
        retrieval_latencies.append(lat)

        retrieved_ids = [d.metadata.get("chunk_id") for d in docs if d.metadata.get("chunk_id")]

        # QA
        out = qa(q)
        context = "\n".join(d.page_content for d in docs) if docs else ""

        judge = judge_answer(q, out["answer"], context) if docs else {"faithfulness": 0, "relevance": 0}

        results.append({
            "question": q,
            "recall@k": recall_at_k(retrieved_ids, rel_ids, k),
            "mrr": mrr(retrieved_ids, rel_ids),
            "ndcg@k": ndcg_at_k(retrieved_ids, rel_ids, k),
            "context_precision@k": context_precision_at_k(retrieved_ids, rel_ids, k),
            "faithfulness": judge["faithfulness"],
            "relevance": judge["relevance"],
            "latency_ms": lat,
        })

    import numpy as np
    agg = {
        "recall@k": np.mean([r["recall@k"] for r in results]),
        "mrr": np.mean([r["mrr"] for r in results]),
        "ndcg@k": np.mean([r["ndcg@k"] for r in results]),
        "context_precision@k": np.mean([r["context_precision@k"] for r in results]),
        "faithfulness": np.mean([r["faithfulness"] for r in results]),
        "relevance": np.mean([r["relevance"] for r in results]),
        "p50_retrieval_ms": np.percentile(retrieval_latencies, 50),
        "p95_retrieval_ms": np.percentile(retrieval_latencies, 95),
    }

    Path("results").mkdir(exist_ok=True)
    with open("results/eval_results.json", "w") as f:
        json.dump({"aggregate": agg, "per_question": results}, f, indent=2)
    print(json.dumps(agg, indent=2))
    return agg

if __name__ == "__main__":
    run(test_set_path="app/evaluation/test_set.json", k=2)