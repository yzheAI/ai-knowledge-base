from app.embedding.embedding import get_embedding
from app.retriever.rerank import rerank
from app.vector_store.faiss_store import vector_store
from app.retriever.bm25 import bm25_retriever


def retrieve(
        query: str,
        search_top_k: int = 10,
        rerank_top_k: int = 3,
):
    query_embedding = get_embedding(query)
    # FAISS
    faiss_results = vector_store.search(
        query_embedding,
        top_k=search_top_k,
    )

    # BM25（用 index → 转回 text）
    bm25_hits = bm25_retriever.search(query, top_k=search_top_k)
    bm25_results = []
    for hit in bm25_hits:
        idx = hit["index"]  # index：序号
        if idx < len(vector_store.data):
            item = vector_store.data.get(idx)
            if item:
                bm25_results.append({
                    "text": item["text"],
                    "doc_id": item["doc_id"],
                    "distance": hit["bm25_score"],
                    "metadata": item["metadata"],
                    "source": item["metadata"].get("source")
                })
    # 合并
    merged = faiss_results + bm25_results
    # 去重
    seen = set()
    dedup = []
    for item in merged:
        key = item["text"]
        if key not in seen:
            seen.add(key)
            dedup.append(item)
    contexts = rerank(
        query,
        dedup,
        top_k=rerank_top_k,
    )
    return contexts
