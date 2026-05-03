# AI知识库助手（RAG基础版）

## 项目简介
基于 FastAPI 的轻量级知识库系统，实现文档上传、PDF/TXT解析、chunk切分的数据处理流程。

## 功能
- 文件上传（PDF / TXT）
- 文档解析
- 文本chunk切分（滑动窗口）
- 数据流处理pipeline

## 技术栈
- FastAPI
- PyPDF2
- Python

## 启动方式

```bash
uvicorn main:app --reload