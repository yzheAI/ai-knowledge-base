from app.vector_store.store_manager import VectorStoreManager
from app.retriever.faiss_retriever import FaissRetriever
from app.retriever.bm25_retriever import BM25Retriever
from app.retriever.hybrid_retriever import HybridRetriever
from app.retriever.rerank import rerank

vector_manager = VectorStoreManager()


faiss_retriever = FaissRetriever(
    vector_manager=vector_manager,
)

bm25_retriever = BM25Retriever(
    vector_manager=vector_manager,
)


class Reranker:
    def rank(
            self,
            query,
            docs
    ):
        return rerank(
            query=query,
            docs=docs,
        )


reranker = Reranker()

hybrid_retriever = HybridRetriever(
    faiss_retriever,
    bm25_retriever,
    reranker
)

