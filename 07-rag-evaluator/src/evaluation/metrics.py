"""RAG evaluation metrics: MRR, Precision@K, Recall@K."""

def mean_reciprocal_rank(retrieved_ids: list, relevant_ids: set) -> float:
    for rank, doc_id in enumerate(retrieved_ids, 1):
        if doc_id in relevant_ids:
            return 1.0 / rank
    return 0.0

def precision_at_k(retrieved_ids: list, relevant_ids: set, k: int) -> float:
    top_k = retrieved_ids[:k]
    hits = sum(1 for doc_id in top_k if doc_id in relevant_ids)
    return hits / k if k > 0 else 0.0

def recall_at_k(retrieved_ids: list, relevant_ids: set, k: int) -> float:
    top_k = retrieved_ids[:k]
    hits = sum(1 for doc_id in top_k if doc_id in relevant_ids)
    return hits / len(relevant_ids) if relevant_ids else 0.0

def evaluate_retrieval(results: list[dict], ground_truth: dict) -> dict:
    mrr_scores, p_at_5, r_at_5 = [], [], []
    for result in results:
        query = result["query"]
        retrieved_ids = [r["document"]["id"] for r in result["retrieved"]]
        relevant_ids = set(ground_truth.get(query, []))
        mrr_scores.append(mean_reciprocal_rank(retrieved_ids, relevant_ids))
        p_at_5.append(precision_at_k(retrieved_ids, relevant_ids, 5))
        r_at_5.append(recall_at_k(retrieved_ids, relevant_ids, 5))
    return {
        "mrr": sum(mrr_scores) / len(mrr_scores) if mrr_scores else 0,
        "precision_at_5": sum(p_at_5) / len(p_at_5) if p_at_5 else 0,
        "recall_at_5": sum(r_at_5) / len(r_at_5) if r_at_5 else 0,
    }
