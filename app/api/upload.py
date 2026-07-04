from fastapi import APIRouter, UploadFile, File, Query
from app.config import UPLOAD_DIR
from app.embedding.embedding import get_embedding
from app.llm.qwen import chat_with_qwen
from app.document.pipeline import process_document
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
    file_path = os.path.join(UPLOAD_DIR, file.filename)  # 拼接路径
    with open(file_path, "wb") as f:
        content = await file.read()  # 异步读取用户上传的文件内容
        f.write(content)

    try:
        result = process_document(file_path)
    except ValueError as e:
        return error(str(e), code=400)
    doc_id = str(uuid.uuid4())
    vector_store.add(
        result["vectors"],
        result["chunks"],
        doc_id=doc_id,
        source=file.filename
    )
    vector_store.save()
    return {
        "filename": file.filename,
        "msg": "上传成功",
        "analysis": result
    }


@upload_router.post('/search')
async def read_file(query: str = Query(...)):
    if not vector_store.data:
        return {"query": query, "results": [], "msg": "向量库为空，请先上传文档"}

    query_embedding = get_embedding(query)
    result = vector_store.search(
        query_embedding,
        top_k=3
    )
    return result


@upload_router.get('/files_message')
async def get_files():
    # files = os.listdir(UPLOAD_DIR)
    docs = {}
    for item in vector_store.data.values():
        doc_id = item["doc_id"]
        source = item["source"]

        if doc_id not in docs:
            docs[doc_id] = {
                "doc_id": doc_id,
                "source": source,
                "chunk_count": 1
            }
        else:
            docs[doc_id]["chunk_count"] += 1
    return {
        "count": len(docs),
        "files": list(docs.values())
    }


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
    success_flag = vector_store.delete(doc_id)
    if not success_flag:
        return error("文档不存在", code=404)
    return success(msg="删除成功")
