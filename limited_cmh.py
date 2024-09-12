from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage

class LimitedChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, max_messages: int = 5):
        self._messages: list[BaseMessage] = []
        self.max_messages = max_messages

    def add_message(self, message: BaseMessage) -> None:
        self._messages.append(message)
        self._trim_history()

    def _trim_history(self) -> None:
        if len(self._messages) > self.max_messages:
            self._messages = self._messages[-self.max_messages:]

    def clear(self) -> None:
        self._messages = []

    @property
    def messages(self) -> list[BaseMessage]:
        return self._messages