import os
import random
import sys
import json
import datetime
import gradio as gr
import configparser
from io import StringIO
from dotenv import load_dotenv
from count_tokens import count_tokens, count_tokens_in_string
from check_valid_ini import is_valid_ini
import uuid
from search_replace import apply_translations
from example_ini import EXAMPLE_INI

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, RemoveMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from limited_cmh import LimitedChatMessageHistory
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field
from typing import List, Dict
from prompts import *

load_dotenv()


def pprint_messages(messages):
    for m in messages['messages']:
        m.pretty_print()

current_date = datetime.datetime.now()
date_string_short = current_date.strftime("%m/%d/%y") 


PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

price_per_token = 1e-6
prompt_tokens = count_tokens_in_string(BEHAVIOR_STRING)
print(f"Token count for behavior string = {prompt_tokens}, approx. cost of prompt = {prompt_tokens * price_per_token}")

#===========================================================================
# TOOLS 
#===========================================================================
with open("translation_dict.json", "r", encoding="utf-8") as f:
    my_dict = json.load(f)

#========================================================================


#===========================================================================

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from IPython.display import Image, display
from langgraph.checkpoint.memory import MemorySaver

class MyState(TypedDict):
    ini_string: str
    messages: Annotated[list, add_messages]

prompt = ChatPromptTemplate.from_messages([
    ("system", BEHAVIOR_STRING),
    MessagesPlaceholder(variable_name="messages"),
])

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

chain = prompt | llm

ANALYZER_SYSTEM= f"""
You are part in a chain of LLM calls for a system that generates INI files which describe CFD simulations. Your input will be a list (one or more elements) of
key-value pairs. The only rule is that to the left side of the key-value separator sign is the key and to the right the value with arbitrary use of whitespaces, tabs etc.
Your task is to filter out the key value pairs and to transform it to structured output in the form:
key1 = value1 \n
key2 = value2 \n
...
key_last = value_last \n
"""


analyzer_prompt = ChatPromptTemplate.from_messages([
    (  "system",
    ANALYZER_SYSTEM 
    ),
    MessagesPlaceholder(variable_name="messages"),
])

analyzer_chain = analyzer_prompt | llm

#===========================================================================
# Node functions
#===========================================================================

#===========================================================================
def request_router(state: MyState):
    if random.random() > 0.5:
      return "QUESTION"
    else:
      return "INI"
#===========================================================================
# Translate tool node:
# The node performs a deterministic search and replace operation that
# translates a list of "tricky" keywords from German to English.
# It has no "fuzzy" component so it is not able to i.e. account for 
# spelling mistakes that a user could make.
#===========================================================================
def translate_tool(state: MyState):

    query = state["messages"][-1].content
    updated_query = apply_translations(query, my_dict)
    state["messages"][-1].content = updated_query
    return state

#===========================================================================
# Simple check node:
# The node function enforces some simple rules in the INI file and
# updates them in-place. 
#===========================================================================
def simple_check(state: MyState):

    aiMessage = state['messages']
    ini_file = state["ini_string"]
    config = configparser.ConfigParser()
    config.optionxform = str # preserve the case

    ini_stream = StringIO(ini_file)
    config_string = state["ini_string"]
    
    try:
        config.read_file(ini_stream)
        # If no sections are parsed, it's not valid
        if len(config.sections()) == 0:
            return state
    except (configparser.MissingSectionHeaderError, configparser.ParsingError):
        return state
    
    # Rule 1.
    if config['E3DGeometryData/Machine/Element_1']['type'] == "OFF_LR":
      config['E3DGeometryData/Machine/Element_1']['off_filelist'] = "undefined"
      output = StringIO()
      config.write(output)
      config_string = output.getvalue()
      output.close()
      state['messages'][-1].content = config_string

    return MyState(ini_string=config_string, messages=state["messages"])

#===========================================================================
# Simulation Bot SimBot Node:
# This function contains the main LLM call
#===========================================================================
def simBot(state: MyState):
    #print(f"This is the message state: {state['messages']}")
    response = {"messages": [chain.invoke(state["messages"])]}
    aiMessage = response['messages']
    
    msg = aiMessage[-1]
    if is_valid_ini(msg.content):
        print("LLM returned a valid INI file")
        return MyState(ini_string=msg.content, messages=response["messages"])
    else:
        print("LLM response is not an INI file")
        return MyState(messages=response["messages"])

#===========================================================================
# Filter Node:
# The node function deletes messages that are not related to the INI file
# We keep a maximum of 2 messages to reduce the amount of tokens used.
# There is still the possibility to keep a log of the full conversation,
# but not to send them to the GPT-API to save tokens.
#===========================================================================
def filter_messages(state: MyState):
    """ If none of the leftover messages is an ini file we 
        insert the ini file from the current state. We can also
        save the AIMessage in the state variable
    """

    ini_msg = state['ini_string']

    # Generate a random UUID (UUID4)
    unique_id = str(uuid.uuid4())

    if state['messages'][-1] != ini_msg:
        state['messages'].append(AIMessage(content=ini_msg, id=unique_id))

    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state['messages'][:-3]]
    return MyState(messages=delete_messages)

def output(state: MyState):
    """ Output processing node """
    #for m in state['messages']:
    #    m.pretty_print()
    return state

#===========================================================================


#===========================================================================
# Variant without persistant memory
#===========================================================================
# Build simple graph
#agent.add_node("sim_bot", simBot)
#agent.add_edge(START, "sim_bot")
#agent.add_edge("sim_bot", END)
#agent = StateGraph(MessagesState)
#graph = agent.compile()

#===========================================================================
# Variant with persistant memory where the state is saved
#===========================================================================
# Get the memory module
memory = MemorySaver()

# Define the agent
agent = StateGraph(MyState)

# Build graph with filtering
agent.add_node("translate_tool", translate_tool)
agent.add_node("filter", filter_messages)
agent.add_node("sim_bot", simBot)
agent.add_node("sim_check", simple_check)

# Graph connectivity
agent.add_edge(START, "translate_tool")
agent.add_edge("translate_tool", "sim_bot")

agent.add_edge("sim_bot", "sim_check")
agent.add_edge("sim_check", "filter")
agent.add_edge("filter", END)

graph = agent.compile(checkpointer=memory)
#===========================================================================


#===========================================================================
# Version with translation node
#===========================================================================
# Get the memory module
#memory = MemorySaver()
#
## Define the agent
#agent = StateGraph(MyState)
#
## Build graph with filtering
#agent.add_node("translate_tool", translate_tool)
#agent.add_node("output", output)
#
#
## Graph connectivity
#agent.add_edge(START, "translate_tool")
#agent.add_edge("translate_tool", "output")
#agent.add_edge("output", END)
##agent.add_edge("filter", END)
#
#graph = agent.compile(checkpointer=memory)
#===========================================================================

# Specify a thread
config = {"configurable": {"thread_id": "1"}}

def process_query(query, history):

    global user_file
    human = "================================ Human Message =================================\n"
    ai = "================================== Ai Message ==================================\n"
    messages = [HumanMessage(content=query)]
    with open("log.txt", "a") as f:
        f.write(human)
        f.write(messages[0].content + "\n")

    #===========================================================================
    # Variant without persistant memory
    #===========================================================================
    #nextState = graph.invoke({"messages": messages, "ini_string": "Bullshit"})

    #===========================================================================
    # Variant with persistant memory where the state is saved
    #===========================================================================
    nextState = graph.invoke({"messages": messages, "ini_string": "Bullshit"}, config)
    reply = nextState['messages'][-1].content
    with open("log.txt", "a") as f:
        f.write(ai)
        f.write(reply + "\n")

    return reply

#===========================================================================
# Here we pass the gradio api interface function process_query to gradio
# in order to create and launch a nice chat user interface
#===========================================================================
with gr.Blocks() as iface:
    chatbot = gr.ChatInterface(
        fn=process_query,
        title="Simulation Creation Assistant",
        description="A helpful assistant for creating INI files",
        chatbot=gr.Chatbot(height=600),
#        retry_btn=None,
#        undo_btn=None,
#        clear_btn=None,
    )
    iface.launch(share=False, server_name="127.0.0.1", server_port=7862, inline=False)

