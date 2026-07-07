from app.llm.qwen import chat_with_qwen
from app.prompts.rag_prompt import build_prompt
from app.retriever.retriever import retrieve
from app.schemas.chat import SourceResponse
from app.config import SEARCH_TOP_K, RERANK_TOP_K


async def chat_service(query: str, filters: dict | None):
    contexts = retrieve(
        query,
        search_top_k=SEARCH_TOP_K,
        rerank_top_k=RERANK_TOP_K,
        filters=filters,
    )
    content_text = "\n".join(
        [ctx["text"] for ctx in contexts]
    )
    prompt = build_prompt(
        query,
        content_text
    )
    answer = chat_with_qwen(prompt)
    sources = [
        SourceResponse(
            content=ctx["text"],
            score=ctx["distance"],
            metadata=ctx["metadata"]
        )
        for ctx in contexts
    ]
    return {
        "query": query,
        "answer": answer,
        "sources": sources
    }
