from fastapi import APIRouter, UploadFile, File
from app.config import UPLOAD_DIR
from app.services.pipeline import process_document
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
    return {
        "filename": file.filename,
        "msg": "上传成功",
        "analysis": result
    }


