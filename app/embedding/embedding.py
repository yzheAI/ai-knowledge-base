from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL


# 加载模型
model = SentenceTransformer(EMBEDDING_MODEL)


def get_embedding(text: str):
    return model.encode(text, normalize_embeddings=True)  # 调用模型编码方法，把text变成数字向量


def get_embeddings(texts: list[str]):
    return model.encode(texts, normalize_embeddings=True).tolist()
