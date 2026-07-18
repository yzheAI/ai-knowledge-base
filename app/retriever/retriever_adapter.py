from app.retriever.retriever import retrieve


class RetrieverAdapter:
    def search(self, query, kb_name, top_k=5):

        return retrieve(
            query=query,
            kb_name=kb_name,
            search_top_k=10,
            rerank_top_k=top_k
        )


retriever_adapter = RetrieverAdapter()
