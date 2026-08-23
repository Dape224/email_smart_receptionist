import os
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

def model():
    llm = ChatMistralAI(
        model= "mistral-medium-2505",
        api_key= api_key,
        temperature = 0.0
    )
    return llm