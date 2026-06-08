import faiss
import numpy as np
import pickle
import os

from app.config import INDEX_PATH, TEXT_PATH


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

    def save(self, index_path=INDEX_PATH, texts_path=TEXT_PATH):
        os.makedirs("data", exist_ok=True)
        faiss.write_index(self.index, index_path)
        with open(texts_path, "wb") as f:
            pickle.dump(self.texts, f)

    def load(self, index_path=INDEX_PATH, texts_path=TEXT_PATH):
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)

        if os.path.exists(texts_path):
            with open(texts_path, "rb") as f:
                self.texts = pickle.load(f)
