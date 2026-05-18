from langchain_community.chat_message_histories import FileChatMessageHistory
from app.config import settings as config

class ChatHistoryService(object):
    def __init__(self):
        self.history = FileChatMessageHistory(file_path=config.chat_history_path)

    def add_user_message(self, message):
        self.history.add_user_message(message)

    def add_ai_message(self, message):
        self.history.add_ai_message(message)

    def get_messages(self):
        return self.history.messages

    def clear(self):
        self.history.clear()

    def get_history_text(self, session_id: str = "default"):
        messages = getattr(self.history, "messages", []) or []
        if not messages:
            return ""

        lines = []
        for msg in messages:
            role = getattr(msg, "type", None) or getattr(msg, "role", None) or (msg.get('role') if isinstance(msg, dict) else 'message')
            content = getattr(msg, "content", None) or (msg.get('content') if isinstance(msg, dict) else str(msg))
            lines.append(f"{role}: {content}")

        return "\n".join(lines)