from fastapi import APIRouter, UploadFile, File, Query, Form
from app.config import UPLOAD_DIR
from app.services.upload_service import upload, search_files, get_all_files, file_delete
from utils.response import success
import os


upload_router = APIRouter(prefix="/files", tags=["文件上传"])
os.makedirs(UPLOAD_DIR, exist_ok=True)


@upload_router.post('/')
async def upload_file(
        file: UploadFile = File(...),
        kb_name: str = Form(...)
):  # 表示文件上传类型，参数必须传
    # 上传文档
    result = await upload(
        file,
        kb_name
    )

    return success(result)


@upload_router.post('/search')
async def read_file(
        query: str = Query(...),
        kb_name: str = Query()
):
    result = await search_files(
        query,
        kb_name
    )
    return success(msg=result)


@upload_router.get('/files_message')
async def get_files():
    result = await get_all_files()
    return success(msg=result)


@upload_router.delete("/{doc_id}")
async def delete_file(doc_id: str):
    await file_delete(doc_id)
    return success(msg="删除成功")
