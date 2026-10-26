import numpy as np

def recall_at_k(retrieved_ids, relevant_ids, k):
    topk = set(retrieved_ids[:k])
    return len(topk & set(relevant_ids)) / len(relevant_ids) if relevant_ids else 0.0

def mrr(retrieved_ids, relevant_ids):
    for i, rid in enumerate(retrieved_ids, 1):
        if rid in relevant_ids:
            return 1.0 / i
    return 0.0

def ndcg_at_k(retrieved_ids, relevant_ids, k):
    topk = retrieved_ids[:k]
    dcg = sum(1.0 / np.log2(i+2) for i, rid in enumerate(topk) if rid in relevant_ids)
    idcg = sum(1.0 / np.log2(i+2) for i in range(min(len(relevant_ids), k)))
    return dcg / idcg if idcg > 0 else 0.0

def context_precision_at_k(retrieved_ids, relevant_ids, k):
    topk = retrieved_ids[:k]
    hits = [1 if rid in relevant_ids else 0 for rid in topk]
    precisions = []
    cum = 0
    for i, h in enumerate(hits, 1):
        if h:
            cum += 1
            precisions.append(cum / i)
    return sum(precisions) / min(k, len(relevant_ids)) if precisions else 0.0