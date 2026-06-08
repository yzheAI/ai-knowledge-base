from fastapi import APIRouter, UploadFile, File, Query
from app.config import UPLOAD_DIR
from app.services.embedding import get_embedding
from app.services.pipeline import process_document
from app.services.store import vector_store
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

