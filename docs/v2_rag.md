## v2_rag.md
```mermaid
graph TD
A[User Query] --> B[FastAPI Chat API]
B --> C[Embedding Model]
C --> D[FAISS Vector Search]
D --> E[TopK Results]
E --> F[Rerank CrossEncoder]
F --> G[Context Construction]
G --> H[Qwen LLM API]
H --> I[Answer Response]