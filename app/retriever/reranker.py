from app.retriever.rerank import rerank


class CrossEncoderReranker:
    def rank(
            self,
            query,
            docs
    ):
        return rerank(
            query,
            docs
        )
