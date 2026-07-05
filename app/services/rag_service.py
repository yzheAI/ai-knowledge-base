from app.llm.qwen import chat_with_qwen
from app.prompts.rag_prompt import build_prompt
from app.retriever.retriever import retrieve
from app.schemas.chat import SourceResponse


async def chat_service(query: str):
    contexts = retrieve(
        query,
        search_top_k=10,
        rerank_top_k=3
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
