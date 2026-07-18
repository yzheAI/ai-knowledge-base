## v2_rag.md
```mermaid
graph TD
A[User Query + Knowledge Base] --> B[FastAPI Chat API]

B --> C[RAG Service]

C --> D[VectorStoreManager]

D --> E[Load Knowledge Base Instance]

E --> F1[FAISS Vector Store]
E --> F2[BM25 Index]


C --> G[Query Embedding]

G --> F1

F1 --> H1[Semantic TopK Retrieval]

F2 --> H2[Keyword TopK Retrieval]


H1 --> I[Hybrid Retrieval Merge]

H2 --> I


I --> J[Deduplication]

J --> K[CrossEncoder Rerank]

K --> L[Context Construction]

L --> M[Qwen LLM]

M --> N[Answer + Source Tracking]
