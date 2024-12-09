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

store = {}

# Update the get_session_history function
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        # max_messages 3 will keep the last 2 AIMessages
        store[session_id] = LimitedChatMessageHistory(max_messages=2)
    return store[session_id]


current_date = datetime.datetime.now()
date_string_short = current_date.strftime("%m/%d/%y") 

SYSTEM_STRING2 = """
You are a translator to German, you translate all input given to you to the German language.
"""

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

[E3DGeometryData/Machine/Element_1]
GapScrewScrew=0.7 <Clearance between screws in a twin-screw extruder> [mm]
ObjectType=screw <The object is a screw>
Unit=mm <Unit for input parameters>
startposition = 0.0 <Starting position of the screw> [mm]
off_filelist = screw_extended_by_10.off <File containing the 3D geometry of the screw>
off_filelistL = screw_+Y_extended_by_10.off <File for the left-hand side of the screw geometry>
off_filelistR = screw_-Y_extended_by_10.off <File for the right-hand side of the screw geometry>
innerdiameter = 30.9 <Inner diameter of the screw> [mm]
type = OFF,OFF_LR <Type of input geometry; OFF requires `off_filelist`, OFF_LR requires both `off_filelistL` and `off_filelistR`>

[E3DProcessParameters]
ScrewSpeed=300.0 <Rotational speed of the screw> [rpm]
ProcessType=THROUGHPUT <Type of process: mass throughput>
MassThroughput=300.0 <Mass of material processed per hour> [kg/h]
MaterialTemperature=290.0 <Inflow temperature of the material and starting melt temperature> [C deg]
BarrelTemperature=280.0 <Barrel temperature (used if not adiabatic)> [C deg]
ScrewTemperature=_INVALID_ <Screw temperature (used if not adiabatic)> [C deg]
BarrelTemperatureAdiabatic=YES,NO <If NO, a specific ScrewTemperature must be defined>
ScrewTemperatureAdiabatic=YES,NO <If NO, a specific BarrelTemperature must be defined>

[E3DProcessParameters/Material]
Name=PC1 <Name of the material>
Type=Polymer <Type of material>

[E3DProcessParameters/Material/RheologicalData]
CalcVisco=Carreau <Viscosity model used for the material>
CalcTemp=TbTs <Temperature model used for the material>

[E3DProcessParameters/Material/RheologicalData/Carreau]
ZeroViscosity=397.69 <Viscosity at zero shear rate> [Pa.s]
RecipVelocity=0.00029 <Reciprocal of the characteristic shear rate velocity> [s]
Exponent=0.92012 <Exponent in the Carreau viscosity model> [unitless]

[E3DProcessParameters/Material/RheologicalData/TBTS]
standardtemperature = 135.7 <Standard processing temperature> [C deg]
referencetemperature = 300.0 <Reference temperature for rheological calculations> [C deg]

[E3DProcessParameters/Material/ThermoData]
heatconductivity = 0.134 <Thermal conductivity of the material> [W/m/K]
heatconductivityslope = 0.0 <Slope of the thermal conductivity with respect to temperature>
heatcapacity = 1.75 <Specific heat capacity of the material> [kJ/kg/K]
heatcapacityslope = 0.0 <Slope of the heat capacity with respect to temperature>
densitymodel = DENSITY <Density model used for the material>

[E3DProcessParameters/Material/ThermoData/Density]
Density=1.0 <Density of the melt> [g/cm3]
DensitySlope=0.0 <Slope of the density with respect to temperature>

[E3DSimulationsettings]
MeshQuality=coarse, medium, fine <Mesh resolution>
HexMesher=TwinScrew / HollowCylinder <Mesh generator type: TwinScrew or HollowCylinder>
KTPRelease=NO <Flag indicating whether KTP release is activated>
"""

BEHAVIOR_STRING= f"""
You are an assistant for creating INI file. You can take this INI file as a template: {REDUCED_EXPLANATION_STRING}
This is an INI file enriched with information about the key-value pairs which is inside the angled brackets. In square brackets I have the standard units for the values (if applicable).
A user may now send a message in which he defines one or more key value pairs. Your task is to find and replace the values in the template by the value(s) given in user's message. If you
find in the chat history a previous reply with a full INI file then update values in this file instead of the template INI file. 
Your reply always includes the full(every section), updated INI file without the extra information in angled or square brackets. A user may enter keys in the German language if so try to find the matching key and replace its value.
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

def is_valid_ini(ini_string: str) -> bool:
    """This functions returns true if the string ini_string is a valid INI file, else false"""
    config = configparser.ConfigParser()
    ini_stream = StringIO(ini_string)
    
    try:
        config.read_file(ini_stream)
        # If no sections are parsed, it's not valid
        if len(config.sections()) == 0:
            return False
        return True
    except (configparser.MissingSectionHeaderError, configparser.ParsingError):
        return False


from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from IPython.display import Image, display

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

agent = StateGraph(MyState)

def simBot(state: MyState):
    print(f"This is the message state: {state['messages']}")
    response = {"messages": [chain.invoke(state["messages"])]}
    aiMessage = response['messages']
    
    msg = aiMessage[-1]
    if is_valid_ini(msg.content):
        print("LLM returned a valid INI file")
    else:
        print("LLM response is not an INI file")

    return MyState(ini_string=msg.content, messages=response["messages"])


# Build graph
agent.add_node("sim_bot", simBot)
agent.add_edge(START, "sim_bot")
agent.add_edge("sim_bot", END)
graph = agent.compile()

messages = [HumanMessage(content="Zwickel = straight BarrelDiameter = 65 BarrelLength = 71 Type=SSE RotationDirection=LEFT" )]
messages = graph.invoke({"messages": messages, "ini_string": "Bullshit"})

for m in messages['messages']:
    m.pretty_print()