from app.core.container import vector_manager
from app.embedding.embedding import get_embedding


class FaissRetriever:
    def search(self, query, kb_name, top_k=5):
        store = vector_manager.get_store(kb_name)
        embedding = get_embedding(query)
        result = store.search(
            embedding,
            top_k
        )
        return result
