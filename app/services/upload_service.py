import os
import uuid
from app.config import UPLOAD_DIR
from app.document.pipeline import process_document
from app.embedding.embedding import get_embedding
from app.vector_store.faiss_store import vector_store
from utils.response import error, success


async def upload(file):
    # 上传文档
    file_path = os.path.join(UPLOAD_DIR, file.filename)  # 拼接路径
    with open(file_path, "wb") as f:
        content = await file.read()  # 异步读取用户上传的文件内容
        f.write(content)

    result = process_document(str(file_path))

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


async def search_files(query: str):
    if not vector_store.data:
        return {"query": query, "results": [], "msg": "向量库为空，请先上传文档"}

    query_embedding = get_embedding(query)
    result = vector_store.search(
        query_embedding,
        top_k=3
    )
    return result


async def get_all_files():
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


async def file_delete(doc_id):
    success_flag = vector_store.delete(doc_id)
    if not success_flag:
        return error("文档不存在", code=404)
    return success(msg="删除成功")
