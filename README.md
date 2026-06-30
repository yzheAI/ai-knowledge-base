# AI知识库助手（RAG基础版）

## 项目简介
基于 FastAPI 的轻量级知识库系统，实现文档上传、PDF/TXT解析、chunk切分的数据处理流程。
并通过 SentenceTransformer 生成向量表示，使用 FAISS 构建向量索引，实现高效语义检索，最终结合大语言模型生成回答

## 功能
- 文件上传（PDF / TXT）
- 文档解析
- 文本chunk切分（基于句子+滑动窗口）
- 数据流处理pipeline
- 向量检索（FAISS）
- 基于检索内容的 LLM 问答（Qwen）
- 检索结果与原文映射（source tracking）

## 技术栈
- FastAPI
- PyPDF2
- Python
- SentenceTransformers（文本向量化）
- FAISS（向量检索） 
- OpenAI Compatible API（Qwen）


## 启动方式

```bash
uvicorn main:app --reload