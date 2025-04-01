from ..singleton import singleton
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os
import dotenv
dotenv.load_dotenv()

@singleton
class LLM:
    def __init__(self):
        self.gpt_4 = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY"),
            model_kwargs={"response_format": {"type": "json_object"}}
        )
        self.groq_llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            # model="llama-3.1-8b-instant",
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY"),
            model_kwargs={"response_format": {"type": "json_object"}}
        )
    def get_gpt_4(self):
        return self.gpt_4
    
    def get_groq_llm(self):
        return self.groq_llm
