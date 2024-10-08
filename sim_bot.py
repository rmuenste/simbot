import getpass
import os
import datetime
import gradio as gr
import configparser
from io import StringIO
from dotenv import load_dotenv
from count_tokens import count_tokens, count_tokens_in_string
from check_valid_ini import is_valid_ini

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from limited_cmh import LimitedChatMessageHistory
from langchain_core.tools import tool
from prompts import *

# We can also save the AIMessage with the INI file in the state
user_file="""
[SigmaFileInfo]
FileType=ToExtrud3D
FileVersion=SIGMA 10.0
Date=07/02/19
SigmaVersion=SIGMA 12.0.1(4492)
ConfigId=XY60_PE_400.xpro-201907020948

[E3DGeometryData]
[E3DGeometryData/Machine]
Type=TSE,SSE,DIE
Unit=mm
Zwickel=straight,curved
MachineName=XY 60
RotationDirection=LEFT,RIGHT
BarrelDiameter=51.5
CenterlineDistance=10
BarrelStraightCut=0.4
NoOfElements=1
NoOfFlights=1
BarrelLength=70.0
"""

@tool
def get_current_state() -> str:
    """This tool returns the current state of the INI file as a string"""
    print("We get the current state")
    return user_file

@tool
def update_state(ini_string: str) -> str:
    """This tool should be called when a new INI response is generated."""
    user_file = ini_string
    print(f"update state tool called, input: {ini_string}")
    return user_file



store = {}

# Update the get_session_history function
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        # max_messages 3 will keep the last 2 AIMessages
        store[session_id] = LimitedChatMessageHistory(max_messages=2)
    return store[session_id]

#======================================================================================================================

price_per_token = 1e-6
prompt_tokens = count_tokens_in_string(BEHAVIOR_STRING)
print(f"Token count for behavior string = {prompt_tokens}, approx. cost of prompt = {prompt_tokens * price_per_token}")

prompt = ChatPromptTemplate.from_messages([
    (  "system",
      BEHAVIOR_STRING 
    ),
    MessagesPlaceholder(variable_name="messages"),
])

#======================================================================================================================

tools = [update_state]

# Alternatively:
# model="gpt-4"
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

model.bind_tools(tools)

chain = prompt | model

chain_wh = RunnableWithMessageHistory(chain, get_session_history)

config = {"configurable": {"session_id": "abc2"}}

def process_query(query, history):
    print(f"This is history: {history}")

    messages = [
            SystemMessage(content=SYSTEM_STRING3),
            HumanMessage(content=query),
    ]

    response = chain_wh.invoke({"messages": HumanMessage(content=query)}, config=config)

    if is_valid_ini(response.content):
        print("We have a new state")
    else:
        print("This is not an ini file response")

    print(f" {response.response_metadata['token_usage']['prompt_tokens']}")

    # sessionHistory is a list of messages, where the AIMessage is a more
    # complicated entry than the HumanMessage or the SystemMessage
    sessionHistory = get_session_history('abc2')

    print(f"session history: {sessionHistory.messages}")

    return response.content

""" Gradio Setup
The gr.Blocks() object:
This is the main container for your entire Gradio application. It represents the overall structure of your interface.

- The with gr.Blocks() as iface: syntax:
  This is using Python's context manager feature. It creates a new scope where all the Gradio components you define 
  are automatically added to the Blocks object 
-Hierarchical structure:
  Within a Blocks context, you can nest other blocks (like gr.Row(), gr.Column(), etc.) to create more complex layouts. This allows for a hierarchical structure in your UI.
-Flexibility:
  Using Blocks gives you more control over the layout and interaction between components. You can add custom CSS, JavaScript, and create more advanced event handlers.
-Automatic launch:
  When you use the with statement, the launch() method is called on the Blocks object (iface in your case) rather than on individual components.

"""
with gr.Blocks() as iface:
    chatbot = gr.ChatInterface(
        fn=process_query,
        title="Simulation Creation Assistant",
        description="A helpful assistant for creating INI files",
        chatbot=gr.Chatbot(height=600),
        retry_btn=None,
        undo_btn=None,
        clear_btn=None,
    )
iface.launch(share=False, server_name="127.0.0.1", server_port=7860, inline=False)

""" Alternative Syntax without Blocks

# Create the chat interface
chatbot = gr.ChatInterface(
    fn=process_query,
    title="Simulation Creation Assistant",
    description="A helpful assistant for creating INI files",
    chatbot=gr.Chatbot(height=600),
    retry_btn=None,
    undo_btn=None,
    clear_btn=None,
)

# Launch the interface
chatbot.launch(share=False, server_name="127.0.0.1", server_port=7860, inline=False)

"""