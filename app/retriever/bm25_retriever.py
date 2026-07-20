from app.exceptions.exceptions import KnowledgeBaseEmptyError
from app.retriever.base import BaseRetriever


class BM25Retriever(BaseRetriever):
    def __init__(
            self,
            vector_manager
    ):
        self.vector_manager = vector_manager

    def retrieve(
            self,
            query: str,
            kb_name: str,
            top_k=5,
            filters=None
    ):
        store = self.vector_manager.get_store(
            kb_name
        )

        if store is None:
            raise KnowledgeBaseEmptyError(
                "知识库不存在"
            )

        hits = store.bm25.search(
            query,
            top_k
        )

        results = []

        for hit in hits:
            idx = hit["chunk_id"]

            item = store.data.get(idx)

            if item is None:
                continue

            if filters is not None:
                matched = all(
                    item["metadata"].get(k) == v
                    for k, v in filters.items()
                )

                if not matched:
                    continue

            results.append({
                "text": item["text"],
                "doc_id": item["doc_id"],
                "distance": hit["score"],
                "metadata": item["metadata"]
            })

        return results
