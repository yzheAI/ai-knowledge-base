from pydantic import BaseModel


class SourceResponse(BaseModel):
    content: str
    score: float
    metadata: dict


class ChatResponse(BaseModel):
    query: str
    answer: str
    sources: list[SourceResponse]
    kb_name: str


class MetadataFilter(BaseModel):
    file_type: str | None = None
    source: str | None = None


class ChatRequest(BaseModel):
    query: str
    filters: MetadataFilter | None = None
