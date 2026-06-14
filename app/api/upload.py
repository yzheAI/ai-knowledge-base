from fastapi import APIRouter, UploadFile, File, Query
from app.config import UPLOAD_DIR
from app.services.embedding import get_embedding
from app.services.llm import chat_with_qwen
from app.services.pipeline import process_document
from app.services.store import vector_store
from app.schemas.chat import ChatResponse, SourceResponse
from app.schemas.response_schema import ResponseModel
from utils.response import success, error
import os


router = APIRouter(prefix="/files", tags=["文件上传"])
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post('/')
async def upload_file(file: UploadFile = File(...)):  # 表示文件上传类型，参数必须传
    # 上传文档
    file_path = os.path.join(UPLOAD_DIR, file.filename)  # 拼接路径
    with open(file_path, "wb") as f:
        content = await file.read()  # 异步读取用户上传的文件内容
        f.write(content)

    result = process_document(file_path)
    vector_store.add(result["vectors"], result["chunks"])
    vector_store.save()
    return {
        "filename": file.filename,
        "msg": "上传成功",
        "analysis": result
    }


@router.post('/search')
async def read_file(query: str = Query(...)):
    if not vector_store.texts:
        return {"query": query, "results": [], "msg": "向量库为空，请先上传文档"}

    query_embedding = get_embedding(query)
    result = vector_store.search(
        query_embedding,
        top_k=3
    )
    return result


@router.get('/')
async def get_files():
    files = os.listdir(UPLOAD_DIR)
    return {
        "count": len(files),
        "files": files
    }


@router.post('/chat', response_model=ResponseModel[ChatResponse])
async def chat(query: str):
    query_embedding = get_embedding(query)
    contexts = vector_store.search(
        query_embedding,
        top_k=3
    )
    content_text = "\n".join(
        [ctx["text"] for ctx in contexts]
    )
    prompt = f"""
    请根据给定资料回答问题。
    资料：
    {content_text}
    问题：
    {query}
    如果资料中没有答案，请明确说明。
    """
    answer = chat_with_qwen(prompt)
    sources = [
        SourceResponse(
            content=ctx["text"],
            score=ctx["distance"]
        )
        for ctx in contexts
    ]
    return success({
        "query": query,
        "answer": answer,
        "sources": sources
    })
