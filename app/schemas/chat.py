from pydantic import BaseModel


class SourceResponse(BaseModel):
    content: str
    score: float
    metadata: dict


class ChatResponse(BaseModel):
    query: str
    answer: str
    sources: list[SourceResponse]
