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
            top_k=5
    ):
        store = self.vector_manager.get_store(
            kb_name
        )

        if store is None:
            raise KnowledgeBaseEmptyError(
                "知识库不存在"
            )

        return store.bm25.search(
            query,
            top_k
        )
