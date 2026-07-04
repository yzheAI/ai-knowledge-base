from app.embedding.embedding import get_embedding
from app.retriever.rerank import rerank
from app.vector_store.faiss_store import vector_store


def retrieve(
        query: str,
        search_top_k: int = 10,
        rerank_top_k: int = 3,
):
    query_embedding = get_embedding(query)
    contexts = vector_store.search(
        query_embedding,
        top_k=search_top_k,
    )
    contexts = rerank(
        query,
        contexts,
        top_k=rerank_top_k,
    )
    return contexts
