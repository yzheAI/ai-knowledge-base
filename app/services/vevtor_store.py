import faiss
import numpy as np


# 封装FAISS，实现 存向量+存原文+搜相似文本
class VectorStore:

    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)  # L2距离
        self.texts = []

    # 添加文本与向量
    def add(self, embeddings, texts):
        embeddings = np.array(embeddings).astype("float32")  # 转成FAISS需要的格式

        if len(embeddings.shape) == 1:
            embeddings = embeddings.reshape(1, -1)
        self.index.add(embeddings)  # 向量存入索引
        self.texts.extend(texts)  # 原文存入列表

    def search(self, query_embedding, top_k=3):
        query_embedding = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)
        results = []
        for i in indices[0]:
            if i < len(self.texts):
                results.append(self.texts[i])

        return results
