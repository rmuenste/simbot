import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.tools import StructuredTool
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

calculator = StructuredTool.from_function(func=multiply)
print(calculator.invoke({"a" : 2, "b" : 3}))

#========================================================================

def translate(words: str) -> str:  
    """Translates a key words from English to German"""
    #for word in words:
    print(words) 

    return words

my_dict = {
    "Schnecke" : "Screw", 
    "Dichte" : "Density", 
    "Durchsatz" : "Throughput" 
}
def translate2(words: List[str]) -> List[str]:  
    """Translates a list of key words from English to German"""
    translation = []
    for word in words:
        value = my_dict.get(word, "")
        translation.append(value)

    return translation


#========================================================================
translator = StructuredTool.from_function(func=translate)
#print(translator.invoke(["Schnecke", "Hohlraum", "Spiel"]))
print(translator.invoke("Schnecke"))

class TranslatorInput(BaseModel):
    words: List[str] = Field(description="List of words")

translator2 = StructuredTool.from_function(
    func=translate2,
    name="Translator2",
    description="translate list of words",
    args_schema=TranslatorInput,
    return_direct=True,
    )

words = ["Schnecke", "Dichte", "Durchsatz"]
input_data = {"words" : words}

print(translator2.invoke(input_data))

class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")

calculator0 = StructuredTool.from_function(
    func=multiply,
    name="Calculator",
    description="multiply numbers",
    args_schema=CalculatorInput,
    return_direct=True,
    # coroutine= ... <- you can specify an async method if desired as well
)

print(calculator0.invoke({"a": 2, "b": 3}))
print(calculator0.name)
print(calculator0.description)
print(calculator0.args)