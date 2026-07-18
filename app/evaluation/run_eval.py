from app.evaluation.evaluator import RetrieverEvaluator
from app.config import JSON_PATH
from app.retriever.retriever_adapter import retriever_adapter


evaluator = RetrieverEvaluator(
    JSON_PATH
)

result = evaluator.evaluate(
    retriever_adapter,
)
print(result)

