import os
import uuid
from datetime import datetime
from app.knowledge_base.manager import KnowledgeManager
from app.config import SEARCH_TOP_K, KNOWLEDGE_BASE_PATH
from app.document.pipeline import process_document
from app.embedding.embedding import get_embedding
from app.exceptions.exceptions import DocumentNotFound, KnowledgeBaseEmptyError
from app.core.container import container


async def upload(file, kb_name):
    # 定义路径
    kdg = KnowledgeManager(KNOWLEDGE_BASE_PATH)
    kb_path = kdg.create(kb_name)
    upload_dir = os.path.join(
        kb_path,
        "files"
    )

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    # 上传文档
    file_path = os.path.join(upload_dir, file.filename)  # 拼接路径
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
    store = container.vector_manager.get_store(
        kb_name
    )
    store.add(
        result["vectors"],
        result["chunks"],
        doc_id=doc_id,
        metadata=metadata
    )

    store.save(kb_path)
    return {
        "filename": file.filename,
        "msg": "上传成功",
        "analysis": result
    }


async def search_files(query: str, kb_name):
    store = container.vector_manager.get_store(
        kb_name
    )

    if not store.data:
        raise KnowledgeBaseEmptyError()

    query_embedding = get_embedding(query)

    result = store.search(
        query_embedding,
        top_k=SEARCH_TOP_K
    )
    return result


async def get_all_files(kb_name):
    docs = {}
    store = container.vector_manager.get_store(kb_name)

    for item in store.data.values():

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


async def file_delete(doc_id, kb_name):
    kdg = KnowledgeManager(KNOWLEDGE_BASE_PATH)
    store = container.vector_manager.get_store(kb_name)
    kb_path = kdg.get_path(kb_name)
    success_flag = store.delete(doc_id, kb_path)
    if not success_flag:
        raise DocumentNotFound(message="文档不存在")
    return success_flag
