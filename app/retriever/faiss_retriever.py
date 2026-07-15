from app.vector_store.faiss_store import vector_store
from app.embedding.embedding import get_embedding


class FaissRetriever:
    def __init__(self):
        self.vector_store = vector_store

    def search(self, query, top_k=5):
        embedding = get_embedding(query)
        result = self.vector_store.search(
            embedding,
            top_k
        )
        return result


faiss_retriever = FaissRetriever()
