import os
import json
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import openai
import shutil

CHROMA_PATH = "./chroma_storage"
DATA_PATH = "sim"

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()
#---- Set OpenAI API key 
# Change environment variable name from "OPENAI_API_KEY" to the name given in 
# your .env file.
openai.api_key = os.environ['OPENAI_API_KEY']

def load_documents():
    documents = []
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            rows = json.load(f)
    except Exception as e:
        print(f"Error loading documents: {e}")
        documents = []
        return documents

    for row in rows:
        text_content = "\n".join([f"{key}: {value}" for key, value in row.items()])
        doc = Document(page_content=text_content, metadata={"source": "some data"})
        documents.append(doc)
    return documents

def save_vectorstore(documents: list[Document]):
    # Use OpenAI Embeddings to transform text into vector embeddings
    embedding_function = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding_function,
        persist_directory=CHROMA_PATH
    )

    print(f"Saved {len(documents)} documents to {CHROMA_PATH}.")    

def clear_vectorstore():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)