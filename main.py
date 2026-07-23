import uvicorn
from fastapi import FastAPI

from app.api.chat import chat_router
from app.api.upload import upload_router as upload_router
from app.exceptions.handlers import register_exception_handlers

app = FastAPI(title="AI知识库助手")
register_exception_handlers(app)
app.include_router(upload_router)
app.include_router(chat_router)
if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        # host="127.0.0.1",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
