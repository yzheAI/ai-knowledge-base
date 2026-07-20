from app.retriever.base import BaseRetriever


class HybridRetriever(BaseRetriever):
    def __init__(
        self,
        faiss_retriever,
        bm25_retriever,
        reranker
    ):
        self.faiss_retriever = faiss_retriever
        self.bm25_retriever = bm25_retriever
        self.reranker = reranker

    def retrieve(
            self,
            query,
            kb_name,
            top_k=5
    ):
        faiss_docs = self.faiss_retriever.retrieve(
            query,
            kb_name,
            top_k
        )

        bm25_docs = self.bm25_retriever.retrieve(
            query,
            kb_name,
            top_k
        )

        docs = self.merge(
            faiss_docs,
            bm25_docs
        )

        results = self.reranker.rank(
            query,
            docs
        )

        return results

    def merge(self, faiss_docs, bm25_docs):
        result = []
        seen = set()
        docs = faiss_docs + bm25_docs
        for doc in docs:
            doc_text = doc["text"]
            if doc_text not in seen:
                seen.add(doc_text)
                result.append(doc)

        return result
