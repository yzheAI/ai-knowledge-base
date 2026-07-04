import uvicorn
from fastapi import FastAPI

from app.api.chat import chat_router
from app.api.upload import upload_router as upload_router
app = FastAPI(title="AI知识库助手")
app.include_router(upload_router)
app.include_router(chat_router)
if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
