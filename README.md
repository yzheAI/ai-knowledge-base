# AI知识库助手（RAG基础版）

## 项目简介
基于 FastAPI 的轻量级知识库系统，实现文档上传、PDF/TXT解析、chunk切分的数据处理流程。
并通过 SentenceTransformer 生成向量表示，使用 FAISS 构建向量索引，
在检索阶段，系统采用 **归一化 embedding + cosine similarity（FAISS Inner Product）** 实现语义检索，
并结合大语言模型（Qwen）生成最终回答，实现“检索增强生成”的完整闭环。

## 已完成功能
- 文件上传（PDF / TXT）
- 文档解析
- 文本chunk切分（基于句子+滑动窗口）
- 数据流处理pipeline
- 向量检索（FAISS）
- BM25 关键词检索
- Hybrid Retrieval（FAISS + BM25）
- CrossEncoder Rerank 重排序
- Metadata Filter（元数据过滤）
- Source Tracking（答案来源追踪）
- 基于检索内容的 LLM 问答（Qwen）
- 检索结果与原文映射（source tracking）
- 删除文档
- 全局异常处理
- 检索评估

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
├── api/              # 接口层
├── services/         # 业务逻辑
├── document/         # 文档解析与 Pipeline
├── embedding/        # Embedding 模块
├── retriever/        # FAISS、BM25、Rerank
├── vector_store/     # FAISS 向量存储
├── schemas/          # Pydantic 数据模型
├── exceptions/       # 全局异常处理
├── llm/              # qwen 模型调用
├── prompts/          # 构建 prompt
└── config.py         # 项目配置



## 启动方式

```bash
uvicorn main:app --reload


## 后续计划

- [x] Retriever Recall Evaluation
- [ ] 多知识库管理
- [ ] 对话历史（Conversation Memory）
- [ ] Hybrid Score Fusion
- [ ] 多路 Retriever
- [ ] Elasticsearch 检索
- [ ] Milvus / Chroma 向量数据库
- [ ] Docker 部署
- [ ] 前端页面