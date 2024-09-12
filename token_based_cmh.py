from langchain_core.chat_history import BaseChatMessageHistory
import tiktoken

def trim_history(history: BaseChatMessageHistory, max_tokens: int = 2000, model: str = "gpt-3.5-turbo") -> None:
    encoding = tiktoken.encoding_for_model(model)
    
    while True:
        current_tokens = sum(len(encoding.encode(msg.content)) for msg in history.messages)
        if current_tokens <= max_tokens:
            break
        
        # Remove the oldest message
        history.messages.pop(0)

class TrimmedChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, max_tokens: int = 2000, model: str = "gpt-3.5-turbo"):
        self.messages = []
        self.max_tokens = max_tokens
        self.model = model

    def add_message(self, message):
        self.messages.append(message)
        self.trim_history()

    def trim_history(self):
        # Implement the trimming logic here
        pass  # Use the logic from the previous trim_history function

## Then use this in your get_session_history function
#def get_session_history(session_id: str) -> BaseChatMessageHistory:
#    if session_id not in store:
#        store[session_id] = TrimmedChatMessageHistory()
#    return store[session_id]