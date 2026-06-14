from pydantic import BaseModel


class SourceResponse(BaseModel):
    content: str
    score: float


class ChatResponse(BaseModel):
    query: str
    answer: str
    sources: list[SourceResponse]