from sentence_transformers import CrossEncoder
from app.config import RERANK_MODEL_PATH, DEVICE
rerank_model = None


def get_rerank_model():
    global rerank_model
    if rerank_model is None:
        rerank_model = CrossEncoder(
            RERANK_MODEL_PATH,
            device=DEVICE
        )
    return rerank_model


def rerank(query: str, docs: list[dict], top_k: int = 3):
    model = get_rerank_model()
    # 构建二元组(query, doc["text"])
    pairs = [(query, doc["text"]) for doc in docs]
    # 计算并取出scores
    scores = model.predict(pairs)
    # 为docs[i]内部的字典新增一个键值对，新增分数字段
    for i, score in enumerate(scores):
        docs[i]["rerank_score"] = float(score)
    docs = sorted(docs, key=lambda x: x["rerank_score"], reverse=True)
    return docs[:top_k]
