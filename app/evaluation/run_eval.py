from app.evaluation.evaluator import RetrieverEvaluator
from app.config import JSON_PATH
from app.retriever.retriever_adapter import RetrieverAdapter
from app.core.container import faiss_retriever, bm25_retriever, hybrid_retriever


evaluator = RetrieverEvaluator(
    JSON_PATH
)

f_retriever = RetrieverAdapter(
    faiss_retriever,
)

b_retriever = RetrieverAdapter(
    bm25_retriever,
)

h_b_retriever = RetrieverAdapter(
    hybrid_retriever,
)

result_faiss = evaluator.evaluate(
    f_retriever,
)

result_bm25 = evaluator.evaluate(
    b_retriever,
)

result_hybrid = evaluator.evaluate(
    h_b_retriever,
)

print(f"Faiss: {result_faiss}")
print(f"Bm25: {result_bm25}")
print(f"Hybrid: {result_hybrid}")

