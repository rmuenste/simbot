import os
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

current_date = datetime.datetime.now()
date_string_short = current_date.strftime("%m/%d/%y") 

SYSTEM_STRING3 = """
You are a helpful assistant for creating configuration files
"""

REDUCED_EXPLANATION_STRING =f"""
[SigmaFileInfo]
FileType=undefined <Internal parameter identifying the file type>
FileVersion=undefined <Internal version parameter>
Date={date_string_short} <The current date>
SigmaVersion=undefined <Internal version of SIGMA used>
ConfigId=undefined <Internal system job ID>
[E3DGeometryData]
[E3DGeometryData/Machine]
Type=undefined <Extruder type; can be TSE,SSE,DIE>
Unit=undefined <Unit for input parameters; can be mm, cm, dm, ...>
Zwickel=undefined <Barrel shape; can be straight or curved>
MachineName=undefined <Extruder name>
RotationDirection=undefined <Extruder rotation direction: LEFT (default) or RIGHT>
BarrelDiameter=undefined <Barrel diameter (default: 2 * screw diameter + 2 * screw clearance), [mm]>
CenterlineDistance=undefined <Centerline distance between axes, required for TSE simulations, [mm]>
BarrelStraightCut=undefined <Depth of the V-cut (default: 2.5 percent of BarrelDiameter, used only for twin screws),  [mm]>
NoOfElements=undefined <Number of elements in the extruder>
NoOfFlights=undefined <Number of flights in the extruder>
BarrelLength=undefined <Length of the barrel/housing, [mm]>
"""

REDUCED_EXPLANATION_STRING2 =f"""
[SigmaFileInfo]
FileType=ToExtrud3D <Internal parameter identifying the file type>
FileVersion=SIGMA 10.0 <Internal version parameter>
Date={date_string_short} <The current date>
SigmaVersion=SIGMA 12.0.1(4492) <Internal version of SIGMA used>
ConfigId=XY60_PE_400.xpro-201907020948 <Internal system job ID>
[E3DGeometryData]
[E3DGeometryData/Machine]
Type=TSE,SSE,DIE <Extruder type>
Unit=mm <Unit for input parameters>
Zwickel=straight,curved <Barrel shape; can be straight or curved>
MachineName=XY 60 <Extruder name>
RotationDirection=LEFT,RIGHT <Extruder rotation direction: LEFT (default) or RIGHT>
BarrelDiameter=51.5 <Barrel diameter (default: 2 * screw diameter + 2 * screw clearance)> [mm]
CenterlineDistance=41.5 <Centerline distance between axes, required for TSE simulations> [mm]
BarrelStraightCut=0.4 <Depth of the V-cut (default: 2.5 percent of BarrelDiameter, used only for twin screws)> [mm]
NoOfElements=1 <Number of elements in the extruder>
NoOfFlights=1 <Number of flights in the extruder>
BarrelLength=70.0 <Length of the barrel/housing> [mm]
"""

EXPLANATION_STRING =f"""
[SigmaFileInfo]
FileType=undefined <Internal parameter identifying the file type>
FileVersion=undefined <Internal version parameter>
Date={date_string_short} <The current date>
SigmaVersion=undefined <Internal version of SIGMA used>
ConfigId=undefined <Internal system job ID, user may refer to this as srid>

[E3DGeometryData]
[E3DGeometryData/Machine]
Type=undefined <Extruder type, possible values: TSE,SSE,DIE >
Unit=undefined <Unit for input parameters, mm, cm, dm, m, ... etc.>
Zwickel=undefined <Barrel shape; can be straight or curved>
MachineName=undefined <Extruder name>
RotationDirection=undefined <Extruder rotation direction: LEFT (default) or RIGHT>
BarrelDiameter=undefined <Barrel diameter (default: 2 * screw diameter + 2 * screw clearance), German: Zylinderdurchmesser> [mm]
CenterlineDistance=undefined <Centerline distance between axes, required for TSE simulations> [mm]
BarrelStraightCut=undefined <Depth of the V-cut (default: 2.5 percent of BarrelDiameter, used only for twin screws), user may refer to this as vcut> [mm]
NoOfElements=undefined <Number of elements in the extruder>
NoOfFlights=undefined <Number of flights in the extruder, can use single flight (German: eingängig)>
BarrelLength=undefined <Length of the barrel/housing, German: Länge, Gehäuselänge or similar> [mm]

[E3DGeometryData/Machine/Element_1]
GapScrewScrew=undefined <Clearance between screws in a twin-screw extruder, German: Schneckenspiel> [mm]
ObjectType=undefined <The object is a screw>
Unit=undefined <Unit for input parameters, mm, cm, dm, m, ... etc.>
startposition = undefined <Starting position of the screw> [mm]
type = undefined <Type of input geometry; if set to OFF then *.off values are assigned to off_filelist if OFF_LR is set values are assigned to off_filelistL and off_filelistR>
off_filelist = undefined <File containing the 3D geometry of the screw, this key-value is used if type=OFF in this section>
off_filelistL = undefined <File for the left-hand side of the screw geometry, this key-value is used if type=OFF_LR in this section>
off_filelistR = undefined <File for the right-hand side of the screw geometry, this key-value is used if type=OFF_LR in this section>
innerdiameter = undefined <Inner diameter of the screw, German: Kerndurchmesser, Maximaler Schneckendurchmesser> [mm]
outerdiameter = undefined <Outer diameter of the screw, German: Minimaler Schneckendurchmesser> [mm]

[E3DProcessParameters]
ScrewSpeed=undefined <Rotational speed of the screw> [rpm]
ProcessType=undefined <Type of process: mass throughput, can be: THROUGHPUT>
MassThroughput=undefined <Mass of material processed per hour, German: Durchsatz, Massendurchsatz > [kg/h]
MaterialTemperature=undefined <Inflow temperature of the material and starting melt temperature> [C deg]
BarrelTemperature=undefined <Barrel temperature (used if not adiabatic); can be called T_barrel> [C deg]
ScrewTemperature=undefined <Screw temperature (used if not adiabatic); can be called T_screw> [C deg]
BarrelTemperatureAdiabatic=undefined <If NO, a specific ScrewTemperature must be defined, can be YES,NO>
ScrewTemperatureAdiabatic=undefined <If NO, a specific BarrelTemperature must be defined, can be YES,NO>

[E3DProcessParameters/Material]
Name=undefined <Name of the material>
Type=undefined <Type of material>

[E3DProcessParameters/Material/RheologicalData]
CalcVisco=undefined <Viscosity model used for the material, can be: Carreau>
CalcTemp=undefined <Temperature model used for the material, can be: TbTs>

[E3DProcessParameters/Material/RheologicalData/Carreau]
ZeroViscosity=undefined <Viscosity at zero shear rate, a user may refer to as A which comes from the carreau model formula> [Pa.s]
RecipVelocity=undefined <Reciprocal of the characteristic shear rate velocity, can be called B> [s]
Exponent=undefined <Exponent in the Carreau viscosity model, can be called C> [unitless]

[E3DProcessParameters/Material/RheologicalData/TBTS]
standardtemperature = undefined <Standard processing temperature, user may refer to this as T:S or similar> [C deg]
referencetemperature = undefined <Reference temperature for rheological calculations, user may refer to this as T:B or similar> [C deg]

[E3DProcessParameters/Material/ThermoData]
heatconductivity = undefined <Thermal conductivity of the material> [W/m/K]
heatconductivityslope = undefined <Slope of the thermal conductivity with respect to temperature>
heatcapacity = undefined <Specific heat capacity of the material, can be cp> [kJ/kg/K]
heatcapacityslope = undefined <Slope of the heat capacity with respect to temperature>
densitymodel = undefined <Density model used for the material, can be: DENSITY>

[E3DProcessParameters/Material/ThermoData/Density]
Density=undefined <Density of the melt> [g/cm3]
DensitySlope=undefined <Slope of the density with respect to temperature>

[E3DSimulationsettings]
MeshQuality=undefined <Mesh resolution, can be: coarse, medium, fine >
HexMesher=undefined <Mesh generator type: TwinScrew or HollowCylinder>
KTPRelease=undefined <Flag indicating whether KTP release is activated; NO or YES>
"""

BEHAVIOR_STRING= f"""
You are an assistant for creating INI file. You can take this INI file as a template: {EXPLANATION_STRING}
This is an INI file enriched with information about the key-value pairs which is inside the angled brackets. In square brackets I have the standard units for the values (if applicable).
The user should either all at once or message by message send values which should be processed by the assistant.
A user may send a message in which he defines one or more key value pairs. Your task is to find and replace the values in the template by the value(s) given in user's message. If you
find in the chat history a previous reply with a full INI file then we continue to update values in this file instead of starting from the template INI file. 
Always reply with the complete (all sections), updated INI file, omitting units and the explanatory text in angled and square brackets. If the user provides keys in German, identify the corresponding English keys in the template and update their values.
A user may also ask questions about the key-values in the INI file. If you identify a users message as a question about the meaning of a key-value pair in the INI file, try to explain it 
based on the information provided in the angled brackets after the particular key-value pair. If you find no angled backets after the key-value pairs try to explain based on your world knowledge.
"""

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
    (  "system",
      BEHAVIOR_STRING 
    ),
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
def translate_tool(state: MyState):

    query = state["messages"][-1].content
    updated_query = apply_translations(query, my_dict)
    state["messages"][-1].content = updated_query
    return state

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
    example = "Zwickel = straight BarrelDiameter = 65 BarrelLength = 71 Type=SSE RotationDirection=LEFT"
    messages = [HumanMessage(content=query)]
    with open("log.txt", "a") as f:
        f.write(human)
        f.write(messages[0].content + "\n")

#for m in messages['messages']:
#    m.pretty_print()

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

