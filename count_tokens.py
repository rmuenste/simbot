from langchain_core.chat_history import BaseChatMessageHistory
import tiktoken

def count_tokens(history: BaseChatMessageHistory, model: str = "gpt-3.5-turbo") -> None:

    encoding = tiktoken.encoding_for_model(model)
    
    current_tokens = sum(len(encoding.encode(msg.content)) for msg in history.messages)

    return f"We currently have {current_tokens}"

def count_tokens_in_string(msg: str, model: str = "gpt-3.5-turbo") -> None:

    encoding = tiktoken.encoding_for_model(model)
    
    current_tokens = len(encoding.encode(msg))

    return current_tokens
        