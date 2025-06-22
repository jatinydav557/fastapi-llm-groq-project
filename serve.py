from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("Missing GROQ_API_KEY")

# Model
model = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)

# Prompt and chain
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Translate the following into {language}:"),
    ("user", "{text}")
])
parser = StrOutputParser()
chain = prompt_template | model | parser

# FastAPI app
app = FastAPI(
    title="Langchain Translation API",
    version="1.0",
    description="A FastAPI wrapper over a LangChain + Groq translation chain"
)

# Pydantic input
class TranslationInput(BaseModel):
    text: str
    language: str

# Manual POST endpoint 
@app.post("/translate")
def translate(input: TranslationInput):
    result = chain.invoke({"text": input.text, "language": input.language})
    return {"output": result}

# Local run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
