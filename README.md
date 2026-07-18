# AI知识库助手（Multi-Knowledge Base RAG System）

## 项目简介
基于 FastAPI 的多知识库系统RAG（Retrieval Augmented Generation）问答系统，实现文档上传、PDF/TXT解析、chunk切分的数据处理流程。
并通过 SentenceTransformer 生成向量表示，使用 FAISS 构建向量索引，
系统支持多个独立知识库管理，每个知识库拥有独立的数据目录、FAISS向量索引以及BM25关键词索引，实现知识库之间的数据隔离。
在检索阶段，系统通过 SentenceTransformer 生成归一化 embedding，
使用 FAISS IndexFlatIP 实现基于 cosine similarity 的语义检索，
同时结合 BM25 关键词检索进行 Hybrid Retrieval，
并使用 CrossEncoder 对候选结果进行重排序。
并结合大语言模型（Qwen）生成最终回答，实现“检索增强生成”的完整闭环。

## 已完成功能

### 文档处理
- 文件上传（PDF / TXT）
- 文档解析
- 文本chunk切分（基于句子+滑动窗口）
- 数据流处理pipeline

### 检索系统
- 向量检索（FAISS）
- BM25 关键词检索
- Hybrid Retrieval（FAISS + BM25）
- CrossEncoder Rerank 重排序
- Metadata Filter（元数据过滤）
- Source Tracking（答案来源追踪）

### 多知识库管理
- 支持创建多个独立知识库
- 每个知识库独立维护 FAISS Index
- 每个知识库独立维护 BM25 Index
- VectorStoreManager 管理不同知识库实例
- 知识库数据持久化加载

### LLM问答
- 基于检索内容的 LLM 问答（Qwen）
- 检索结果与原文映射（source tracking）
- Conversation Memory 对话历史管理

### 工程能力
- 删除文档
- 全局异常处理
- Recall@K 检索评估
- MRR (Mean Reciprocal Rank)

## 技术栈
- FastAPI
- PyPDF2
- Python
- SentenceTransformers（文本向量化）
- FAISS（向量检索） 
- OpenAI Compatible API（Qwen）
- Pickle（本地持久化）
- rank-bm25
- CrossEncoder
- Retriever Evaluation 测试体系


## 项目结构

```text
app/
├── api/                 # API接口层
├── services/            # 业务逻辑
├── document/            # 文档解析与Pipeline
├── embedding/           # Embedding模块
├── retriever/           # FAISS、BM25、Rerank、Retriever
├── vector_store/        # 向量存储与管理
│   ├── faiss_store.py
│   └── store_manager.py
├── knowledge_base/      # 知识库管理
├── evaluation/          # 检索评估
├── schemas/             # Pydantic模型
├── exceptions/          # 全局异常处理
├── llm/                 # Qwen调用
├── prompts/             # Prompt构建
└── config.py            # 项目配置


data/
└── knowledge_bases/
    ├── copper_based/
    │   ├── files/
    │   ├── faiss.index
    │   ├── texts.pkl
    │   └── bm25.pkl
    │
    └── another_kb/
        ├── files/
        ├── faiss.index
        ├── texts.pkl
        └── bm25.pkl

## 启动方式

```bash
uvicorn main:app --reload


## 后续计划

- [√] Retriever Recall Evaluation
- [√] 多知识库管理
- [√] 对话历史（Conversation Memory）
- [ ] Hybrid Score Fusion
- [ ] 多路 Retriever
- [ ] Elasticsearch 检索
- [ ] Milvus / Chroma 向量数据库
- [ ] Docker 部署
- [ ] 前端页面