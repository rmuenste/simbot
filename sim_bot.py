import getpass
import os
import sys
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

store = {}

# Update the get_session_history function
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        # max_messages 3 will keep the last 2 AIMessages
        store[session_id] = LimitedChatMessageHistory(max_messages=2)
    return store[session_id]

#def get_session_history(session_id: str) -> BaseChatMessageHistory:
#    if session_id not in store:
#        store[session_id] = InMemoryChatMessageHistory()
#    return store[session_id]


@tool
def update_state(ini_string: str) -> str:
    """This tool should be called when a new INI response is generated."""
    global user_file
    user_file = ini_string
    print(f"update state tool called, input: {ini_string}")
    return user_file

price_per_token = 1e-6
prompt_tokens = count_tokens_in_string(BEHAVIOR_STRING_OM)
print(f"Token count for behavior string = {prompt_tokens}, approx. cost of prompt = {prompt_tokens * price_per_token}")

prompt = ChatPromptTemplate.from_messages([
    (  "system",
      BEHAVIOR_STRING_OM
    ),
    MessagesPlaceholder(variable_name="messages"),
])

tools = [update_state]

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

model_with_tools = model.bind_tools(tools)

chain = prompt | model_with_tools

chain2 = prompt | model

model_wh = RunnableWithMessageHistory(model, get_session_history)

chain_wh = RunnableWithMessageHistory(chain, get_session_history)
chain_wh2 = RunnableWithMessageHistory(chain2, get_session_history)

config = {"configurable": {"session_id": "abc2"}}

def process_query(query, history):

    global user_file

    sessionHistory = get_session_history('abc2')
 
#    print("================================== Session Hist ==================================")
#    print(f"session history before:")
#    for msg in sessionHistory.messages:
#        msg.pretty_print()

    response = chain_wh2.invoke({"messages": HumanMessage(content=query)}, config=config)

    # If we have a valid INI file save it in the state
    if is_valid_ini(response.content):
        user_file = response.content

    # sessionHistory is a list of messages, where the AIMessage is a more
    # complicated entry than the HumanMessage or the SystemMessage
    #sessionHistory = get_session_history('abc2')
    #print("================================== Session Hist ==================================")
    #print(f"session history after:")
    #for msg in sessionHistory.messages:
    #    msg.pretty_print()
    print(f"Tokens in prompt: {response.response_metadata['token_usage']['prompt_tokens']}, price of prompt: {float(response.response_metadata['token_usage']['prompt_tokens']) * price_per_token}")
    print(f"Tokens in response: {response.response_metadata['token_usage']['completion_tokens']}, price of response: {float(response.response_metadata['token_usage']['completion_tokens']) * price_per_token}")
    print(f"Total Price of request: {float(response.response_metadata['token_usage']['total_tokens']) * price_per_token}")
    return response.content


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
    iface.launch(share=False, server_name="127.0.0.1", server_port=7862, inline=False)
