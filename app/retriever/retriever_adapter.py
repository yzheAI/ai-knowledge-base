from app.retriever.retriever import retrieve


class RetrieverAdapter:
    def search(self, query, kb_path, top_k=5):

        return retrieve(
            query=query,
            kb_path=kb_path,
            search_top_k=10,
            rerank_top_k=top_k
        )


retriever_adapter = RetrieverAdapter()
