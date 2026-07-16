from app.evaluation.evaluator import RetrieverEvaluator
from app.retriever.faiss_retriever import faiss_retriever
from app.config import JSON_PATH
from app.retriever.retriever_adapter import retriever_adapter


evaluator = RetrieverEvaluator(
    JSON_PATH
)


result = evaluator.evaluate(
    faiss_retriever,
)

print(result)

result = evaluator.evaluate(
    retriever_adapter,
)
print(result)

