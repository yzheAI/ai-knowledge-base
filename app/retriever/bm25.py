from rank_bm25 import BM25Okapi
import jieba


class BM25Retriever:
    def __init__(self):
        self.corpus = []
        self.tokenizer = []
        self.bm25 = None

    def build(self, texts: list[str]):
        self.corpus = texts
        self.tokenizer = [list(jieba.cut(t)) for t in texts]  # 语句分词
        self.bm25 = BM25Okapi(self.tokenizer)  # 初始化 BM25 模型，完成索引构建

    def search(self, query: str, top_k: int = 5):
        if not self.bm25:
            return []
        # 对查询语句分词
        query_tokens = list(jieba.cut(query))
        # 计算query和所有语料的BM25相似度分数
        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(
            enumerate(scores),  # 下标+分数配对
            key=lambda x: x[1],
            reverse=True
        )
        return [
            {
                "bm25_score": float(score),
                "index": idx
            }
            for idx, score in ranked[:top_k]
        ]


bm25_retriever = BM25Retriever()

