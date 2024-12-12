from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, List, Field

local_dict = {}

class TranslatorInput(BaseModel):
    # This property must be part of the input dict
    words: List[str] = Field(description="List of words")

def translate(words: List[str]) -> List[str]:  
    """Translates a list of key words from English to German"""
    translation = []
    for word in words:
        value = local_dict.get(word, "")
        translation.append(value)

    return translation

translator = StructuredTool.from_function(
    func=translate,
    name="Translator",
    description="translate list of words",
    args_schema=TranslatorInput,
    return_direct=True,
    )

words = ["Schnecke", "Dichte", "Durchsatz"]
input_data = {"words" : words}

print(translator.invoke(input_data))
