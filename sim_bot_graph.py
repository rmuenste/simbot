import os
import datetime
from io import StringIO
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from count_tokens import count_tokens, count_tokens_in_string
from prompts import *
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from check_valid_ini import is_valid_ini

# Load the environment variables
load_dotenv()

# Show the token metrics and price of the current prompt
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

agent = StateGraph(MyState)

def simBot(state: MyState):
    print(f"This is the message state: {state['messages']}")
    response = {"messages": [chain.invoke(state["messages"])]}
    aiMessage = response['messages']

    # response['messages] is a list of messages
    # aiMessage[-1] is the last msg in the message list
    msg = aiMessage[-1]
    if is_valid_ini(msg.content):
        print("LLM returned a valid INI file")
    else:
        print("LLM response is not an INI file")

    return MyState(ini_string=msg.content, messages=state['messages'] + response["messages"])

# Build graph
agent.add_node("sim_bot", simBot)
agent.add_edge(START, "sim_bot")
agent.add_edge("sim_bot", END)
graph = agent.compile()

messages = [HumanMessage(content="Zwickel = straight BarrelDiameter = 65")]
messages = graph.invoke({"messages": messages, "ini_string": "Bullshit"})
print(messages)
for m in messages['messages']:
    m.pretty_print()