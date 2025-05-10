import logging
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from typing import Optional

logger = logging.getLogger(__name__)

def get_joke(joke_template: PromptTemplate, chat_model: ChatGroq, topic: str) -> str:
    try:
        if not isinstance(chat_model, ChatGroq):
            raise ValueError("Invalid chat model instance")
        
        if not isinstance(joke_template, PromptTemplate):
            raise ValueError("Invalid joke template instance")

        if not topic or not isinstance(topic, str):
            raise ValueError("Invalid topic provided")

        prompt = joke_template.invoke({"topic": topic})
        response = chat_model.invoke(prompt)
        return response.content.strip()
    
    except Exception as e:
        logger.error(f"Error generating joke: {str(e)}")
        return "Sorry, I couldn't generate a joke at the moment. Please try again later."