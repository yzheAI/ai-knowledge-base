from app.core.container import hybrid_retriever


class RetrieverAdapter:
    def search(self, query, kb_name, top_k=5):

        return hybrid_retriever.retrieve(
            query=query,
            kb_name=kb_name,
            top_k=top_k
        )


retriever_adapter = RetrieverAdapter()
