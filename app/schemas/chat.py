from pydantic import BaseModel


class SourceResponse(BaseModel):
    content: str
    score: float
    filename: str


class ChatResponse(BaseModel):
    query: str
    answer: str
    sources: list[SourceResponse]
