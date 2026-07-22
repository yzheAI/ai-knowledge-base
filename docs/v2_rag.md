# v2_rag.md

## 1. Overview

v2版本在基础 RAG 系统上进行了升级，引入
- Multi Knowledge Base
- Hybrid Retrieval
- BM25 Key Retrieval
- CrossEncoder Rerank
- Retriever Evaluation

整体实现从简单向量检索升级为完整 RAG Pipeline。

## Overall Architecture
```mermaid
graph TD
A[User Query] --> B[FastAPI Chat API]

B --> C[RAG Service]

C --> D[KnowledgeBase Selector]

D --> E[VectorStoreManager]

E --> F[Load Knowledge Base Instance]

F --> G1[FAISS Vector Index]
F --> G2[BM25 Keyword Index]


C --> H[Query Processing]

H --> I1[Embedding Model]

H --> I2[Jieba Tokenization]

I1 --> G1

I2 --> G2

G1 --> J1[Semantic Retrieval]

G2 --> J2[Keyword Retrieval]

J1 --> K[Hybrid Merge]

J2 --> K


K --> L[Deduplication]

L --> M[CrossEncoder Reranker]

M --> N[Top-k Context]

N --> O[Qwen LLM]

O --> P[Answer + Source Tracking]
