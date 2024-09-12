import gradio as gr
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages([
    (  "system",
      "You are a helpful assistant" 
    ),
    MessagesPlaceholder(variable_name="messages"),
])

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

chain = prompt | model

model_wh = RunnableWithMessageHistory(model, get_session_history)

chain_wh = RunnableWithMessageHistory(chain, get_session_history)

config = {"configurable": {"session_id": "abc2"}}

def process_query(query, history):
    print(f"This is history: {history}")
    #model = ChatOpenAI(model="gpt-4")
    
    #response = model_wh.invoke(messages, config=config)
    response = chain_wh.invoke({"messages": HumanMessage(content=query)}, config=config)

    sessionHistory = get_session_history('abc2')
    print(f"This is session history: {sessionHistory}")
    return response.content