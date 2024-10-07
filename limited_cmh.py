from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from check_valid_ini import is_valid_ini
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


class LimitedChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, max_messages: int = 3):
        self._messages: list[BaseMessage] = []
        self.max_messages = max_messages

    def add_message(self, message: BaseMessage) -> None:
        self._messages.append(message)
        self._trim_history()

    def _trim_history(self) -> None:
        """ If none of the leftover messages is an ini file we 
            insert the ini file from the current state. We can also
            save the AIMessage in the state variable
        """

        filtered_msg = ""
        for msg in reversed(self._messages):
            if is_valid_ini(msg.content): 
                filtered_msg = msg.content
                break

        if len(self._messages) > self.max_messages:
            self._messages = self._messages[-self.max_messages:]
            self._messages.append(AIMessage(content=filtered_msg))


    def clear(self) -> None:
        self._messages = []

    @property
    def messages(self) -> list[BaseMessage]:
        return self._messages