from collections import deque


class ConversationMemory:
    def __init__(self, max_turns: int = 5):
        self.max_messages = max_turns * 2
        self.history = deque(maxlen=self.max_messages)

    def add_user_message(self, message: str):
        self.history.append({
            "role": "user",
            "content": message,
        })

    def add_assistant_message(self, message: str):
        self.history.append({
            "role": "assistant",
            "content": message,
        })

    def get_history(self):
        return list(self.history)

    def clear(self):
        self.history.clear()
