from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

chat = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)

response = chat.invoke("Translate 'How are you?' into French")
print(response.content)
