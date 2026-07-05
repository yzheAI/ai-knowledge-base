import faiss
import numpy as np
import pickle
import os

from app.config import INDEX_PATH, TEXT_PATH
from app.retriever.bm25 import bm25_retriever


# 封装FAISS，实现 存向量+存原文+搜相似文本
class VectorStore:

    def __init__(self, dim: int):
        # IDMap 包装
        base_index = faiss.IndexFlatIP(dim)
        self.index = faiss.IndexIDMap(base_index)

        self.data = {}
        self.next_id = 0  # 全局唯一ID分配器的状态变量,生成起点
        self.texts = []

    # 添加文本与向量
    def add(self, embeddings, texts, doc_id, metadata):
        embeddings = np.array(embeddings).astype("float32")  # 转成FAISS需要的格式

        if len(embeddings.shape) == 1:
            embeddings = embeddings.reshape(1, -1)

        self.texts.extend(texts)
        bm25_retriever.build(self.texts)

        # 索引范围
        ids = np.arange(self.next_id, self.next_id + len(texts))
        self.next_id += len(texts)

        # index 添加向量和显式索引
        self.index.add_with_ids(embeddings, ids)  # 存入 list[list[float]] 和 list[int]，每个向量对应一个序号
        for i, text in zip(ids, texts):
            # 使用字典，data[i]（i唯一）存放信息
            self.data[int(i)] = {
                "text": text,
                "doc_id": doc_id,
                "chunk_id": int(i),
                "metadata": metadata
            }

    def search(self, query_embedding, top_k=3):
        query_embedding = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            item = self.data.get(int(idx))
            if not item:
                continue

            results.append({
                "text": item["text"],
                "doc_id": item["doc_id"],
                "distance": float(distance),
                "metadata": item["metadata"]
            })

        return results

    def save(self, index_path=INDEX_PATH, texts_path=TEXT_PATH):
        os.makedirs("data", exist_ok=True)
        faiss.write_index(self.index, index_path)
        with open(texts_path, "wb") as f:
            pickle.dump({
                "data": self.data,
                "next_id": self.next_id
            }, f)

    def load(self, index_path=INDEX_PATH, texts_path=TEXT_PATH):
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)

        if os.path.exists(texts_path):
            with open(texts_path, "rb") as f:
                obj = pickle.load(f)
                self.data = obj["data"]
                self.next_id = obj["next_id"]
        # 恢复 texts
        self.texts = [item["text"] for item in self.data.values()]

        # 重建 BM25
        if self.texts:
            bm25_retriever.build(self.texts)

    def delete(self, doc_id):
        ids = []
        for chunk_id, item in self.data.items():
            if item["doc_id"] == doc_id:
                ids.append(chunk_id)
        if not ids:
            return False
        # 一次性删除FAISS的内容
        ids_array = np.array(ids).astype("int64")
        self.index.remove_ids(ids_array)
        # 循环删除text的内容
        for chunk_id in ids:
            self.data.pop(chunk_id, None)  # None: chunk_id不存在时不报错
        # 保存索引
        self.save()
        return True


vector_store = VectorStore(384)
vector_store.load()
