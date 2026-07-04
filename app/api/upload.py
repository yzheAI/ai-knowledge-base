from fastapi import APIRouter, UploadFile, File, Query
from app.config import UPLOAD_DIR
from app.embedding.embedding import get_embedding
from app.llm.qwen import chat_with_qwen
from app.document.pipeline import process_document
from app.services.upload_service import upload, search_files, get_all_files, file_delete
from app.vector_store.faiss_store import vector_store
from app.schemas.chat import ChatResponse, SourceResponse
from app.schemas.response_schema import ResponseModel
from utils.response import success, error
from app.retriever.rerank import rerank
import uuid
import os


upload_router = APIRouter(prefix="/files", tags=["文件上传"])
os.makedirs(UPLOAD_DIR, exist_ok=True)


@upload_router.post('/')
async def upload_file(file: UploadFile = File(...)):  # 表示文件上传类型，参数必须传
    # 上传文档
    try:
        result = await upload(file)
        return success(result)
    except Exception as e:
        return error(str(e), code=400)


@upload_router.post('/search')
async def read_file(query: str = Query(...)):
    result = await search_files(query)
    return result


@upload_router.get('/files_message')
async def get_files():
    result = await get_all_files()
    return result


@upload_router.post("/chat")
async def chat(query: str):
    query_embedding = get_embedding(query)
    contexts = vector_store.search(
        query_embedding,
        top_k=10
    )
    contexts = rerank(query, contexts, top_k=3)
    content_text = "\n".join(
        [ctx["text"] for ctx in contexts]
    )
    prompt = f"""
    请根据给定资料回答问题。
    资料：
    {content_text}
    问题：
    {query}
    如果资料不足，请回答：未在知识库中找到相关信息。
    """
    answer = chat_with_qwen(prompt)
    sources = [
        SourceResponse(
            content=ctx["text"],
            score=ctx["distance"],
            filename=ctx["source"]
        )
        for ctx in contexts
    ]
    return success({
        "query": query,
        "answer": answer,
        "sources": sources
    })


@upload_router.delete("/{doc_id}")
async def delete_file(doc_id: str):
    result = await file_delete(doc_id)
    return result
