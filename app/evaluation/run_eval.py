from app.evaluation.evaluator import RetrieverEvaluator
from app.retriever.faiss_retriever import faiss_retriever
from app.config import JSON_PATH


evaluator = RetrieverEvaluator(
    JSON_PATH
)


result = evaluator.evaluate(
    faiss_retriever,
)

print(result)

