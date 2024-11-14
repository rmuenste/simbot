import configparser
from io import StringIO
from dotenv import load_dotenv
import os


from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
import datetime

from langchain_core.chat_history import BaseChatMessageHistory
import tiktoken

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from IPython.display import Image, display

load_dotenv()

def count_tokens(history: BaseChatMessageHistory, model: str = "gpt-3.5-turbo") -> None:

    encoding = tiktoken.encoding_for_model(model)
    
    current_tokens = sum(len(encoding.encode(msg.content)) for msg in history.messages)

    return f"We currently have {current_tokens}"

def count_tokens_in_string(msg: str, model: str = "gpt-3.5-turbo") -> None:

    encoding = tiktoken.encoding_for_model(model)
    
    current_tokens = len(encoding.encode(msg))

    return current_tokens



BEHAVIOR_STRING= f"""
You are Cleatus from the Simpsons.
"""

price_per_token = 1e-6
prompt_tokens = count_tokens_in_string(BEHAVIOR_STRING)
print(f"Token count for behavior string = {prompt_tokens}, approx. cost of prompt = {prompt_tokens * price_per_token}")

class MyState(TypedDict):
    ini_string: str
    messages: list
    #messages: Annotated[list, add_messages]

prompt = ChatPromptTemplate.from_messages([
    (  "system",
      BEHAVIOR_STRING 
    ),
    MessagesPlaceholder(variable_name="messages"),
])

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

chain = prompt | llm

model_wh = RunnableWithMessageHistory(llm, get_session_history)

chain_wh = RunnableWithMessageHistory(chain, get_session_history)

config = {"configurable": {"session_id": "abc2"}}

agent = StateGraph(MyState)

def simBot(state: MyState):
    print(f"This is the message state: {state['messages']}")
    return MyState(ini_string="nothing", messages=state['messages'])


# Build graph
agent.add_node("sim_bot", simBot)
agent.add_edge(START, "sim_bot")
agent.add_edge("sim_bot", END)
graph = agent.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))
