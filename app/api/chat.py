from fastapi import APIRouter

from app.schemas.chat import ChatRequest
from app.services.rag_service import chat_service
from utils.response import success

chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.post("/chat")
async def chat(request: ChatRequest):
    response = await chat_service(
        query=request.query,
        filters=request.filters
    )
    return success(response)
