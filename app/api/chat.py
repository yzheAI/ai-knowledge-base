from fastapi import APIRouter
from app.services.rag_service import chat_service
from utils.response import success

chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.post("/chat")
async def chat(query: str):
    response = await chat_service(query)
    return success(response)
