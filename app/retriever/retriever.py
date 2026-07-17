from app.embedding.embedding import get_embedding
from app.retriever.rerank import rerank
from app.core.container import vector_manager


def retrieve(
        query: str,
        kb_path: str,
        search_top_k: int,
        rerank_top_k: int,
        filters=None,
):
    store = vector_manager.get_store(kb_path)
    query_embedding = get_embedding(query)
    # 转换成 dict
    filter_dict = {}
    if filters:
        filter_dict = filters.model_dump(exclude_none=True)
    # FAISS
    faiss_results = store.search(
        query_embedding,
        top_k=search_top_k,
        filters=filter_dict,
    )

    # BM25（用 index → 转回 text）
    bm25_hits = store.bm25.search(query, top_k=search_top_k)
    bm25_results = []
    for hit in bm25_hits:
        idx = hit["index"]  # index：序号

        item = store.data.get(idx)
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
    seen = set()  # set可以提高效率
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
