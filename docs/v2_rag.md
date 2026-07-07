## v2_rag.md
```mermaid
graph TD
A[User Query] --> B[FastAPI Chat API]
B --> C[Query Embedding]
C --> D1[FAISS Semantic Search]
B --> D2[BM25 Keyword Search]
D1 --> E[TopK Results]
D2 --> E
E --> F[Metadata Filter]
F --> G[Deduplication]
G --> H[CrossEncoder Rerank]
H --> I[Context Construction]
I --> J[Qwen LLM]
J --> K[Answer + Sources]
