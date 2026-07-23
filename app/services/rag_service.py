from app.config import SEARCH_TOP_K
from app.llm.qwen import chat_with_qwen
from app.memory.conversation_memory import ConversationMemory
from app.prompts.history_builder import build_history
from app.prompts.rag_prompt import build_prompt
from app.schemas.chat import SourceResponse
from app.core.container import container
memory = ConversationMemory()


async def chat_service(query: str, kb_name, filters=None):

    history = build_history(memory)

    if filters:
        filters = filters.model_dump(
            exclude_none=True
        )

    contexts = container.hybrid_retriever.retrieve(
        query,
        kb_name,
        top_k=SEARCH_TOP_K,
        filters=filters,
    )
    content_text = "\n".join(
        [ctx["text"] for ctx in contexts]
    )

    prompt = build_prompt(
        query,
        content_text,
        history
    )

    answer = chat_with_qwen(prompt)

    memory.add_user_message(query)
    memory.add_assistant_message(answer)

    sources = [
        SourceResponse(
            content=ctx["text"],
            score=ctx["score"],
            metadata=ctx["metadata"]
        )
        for ctx in contexts
    ]
    return {
        "query": query,
        "answer": answer,
        "sources": sources
    }
