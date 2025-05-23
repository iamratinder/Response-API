import logging
from langchain_groq import ChatGroq
from typing import Optional 
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_model() -> Optional[ChatGroq]:
    try:
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        model = ChatGroq(
            model_name="llama3-8b-8192",
            temperature=1.2
        )
        logger.info("Chat model initialized successfully")
        return model
    
    except Exception as e:
        logger.error(f"Failed to initialize chat model: {str(e)}")
        return None