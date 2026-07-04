from app.embedding.embedding import get_embedding
from app.llm.qwen import chat_with_qwen
from app.retriever.rerank import rerank
from app.schemas.chat import SourceResponse
from app.vector_store.faiss_store import vector_store


async def chat_service(query: str):
    query_embedding = get_embedding(query)
    contexts = vector_store.search(
        query_embedding,
        top_k=10
    )
    contexts = rerank(query, contexts, top_k=3)
    content_text = "\n".join(
        [ctx["text"] for ctx in contexts]
    )
    prompt = f"""
        请根据给定资料回答问题。
        资料：
        {content_text}
        问题：
        {query}
        如果资料不足，请回答：未在知识库中找到相关信息。
        """
    answer = chat_with_qwen(prompt)
    sources = [
        SourceResponse(
            content=ctx["text"],
            score=ctx["distance"],
            filename=ctx["source"]
        )
        for ctx in contexts
    ]
    return {
        "query": query,
        "answer": answer,
        "sources": sources
    }
