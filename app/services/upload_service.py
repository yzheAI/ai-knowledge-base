import os
import uuid
from datetime import datetime

from app.config import UPLOAD_DIR, SEARCH_TOP_K
from app.document.pipeline import process_document
from app.embedding.embedding import get_embedding
from app.exceptions.exceptions import DocumentNotFound, KnowledgeBaseEmptyError
from app.vector_store.faiss_store import vector_store


async def upload(file):
    # 上传文档
    file_path = os.path.join(UPLOAD_DIR, file.filename)  # 拼接路径
    with open(file_path, "wb") as f:
        content = await file.read()  # 异步读取用户上传的文件内容
        f.write(content)
    # 获取信息
    result = process_document(str(file_path))
    metadata = result["metadata"]
    metadata.update({
        "source": file.filename,
        "upload_time": datetime.now().isoformat()
    })

    doc_id = str(uuid.uuid4())
    vector_store.add(
        result["vectors"],
        result["chunks"],
        doc_id=doc_id,
        metadata=metadata
    )
    vector_store.save()
    return {
        "filename": file.filename,
        "msg": "上传成功",
        "analysis": result
    }


async def search_files(query: str):
    if not vector_store.data:
        raise KnowledgeBaseEmptyError()
    query_embedding = get_embedding(query)
    result = vector_store.search(
        query_embedding,
        top_k=SEARCH_TOP_K
    )
    return result


async def get_all_files():
    docs = {}
    for item in vector_store.data.values():
        doc_id = item["doc_id"]
        metadata = item["metadata"]

        if doc_id not in docs:
            docs[doc_id] = {
                "doc_id": doc_id,
                "metadata": metadata,
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
        raise DocumentNotFound(message="文档不存在")
    return success_flag
