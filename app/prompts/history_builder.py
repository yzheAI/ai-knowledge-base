from app.memory.conversation_memory import ConversationMemory


def build_history(memory: ConversationMemory):
    history = memory.get_history()
    if not history:
        return ""
    line = []
    for item in history:
        if item["role"] == "user":
            role = "User"
        else:
            role = "Assistant"
        line.append(
            f"{role}: {item['name']}"
        )
    return "\n".join(line)
