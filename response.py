from fastapi import FastAPI, HTTPException, status
from chat.setup import setup_model as chat_model_setup
from jokes.setup import setup_model as joke_model_setup
from jokes.create_joke_template import initial_prompt, final_prompt
from jokes.get_joke import get_joke
import os
import logging
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import random 

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatPrompt(BaseModel):
    text: str = Field(..., min_length=1, description="The prompt text for chat") # ... -> required field

class JokePrompt(BaseModel):
    topic: str = Field(..., min_length=1, description="The topic for joke generation")

chat_model = chat_model_setup()
joke_model = joke_model_setup()

if not chat_model:
    raise RuntimeError("Failed to initialize chat model")
if not joke_model:
    raise RuntimeError("Failed to initialize joke model")

@app.post("/chat", response_model=Dict[str, str])
async def chat_endpoint(prompt: ChatPrompt):
    try:
        result = chat_model.invoke(prompt.text)
        return {"response": result.content}
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate chat response"
        )

@app.post("/joke", response_model=Dict[str, str])
async def joke_endpoint(prompt: JokePrompt):
    try:
        styles = ['sarcastic', 'pun-based', 'absurdist', 'dark', 'dad joke', 'meta', 'observational']
        random_style = random.choice(styles)
        initial = initial_prompt()
        initial_prompt_input = initial.invoke({"random_style":random_style, "topic":prompt.topic})
        initial_result = joke_model.invoke(initial_prompt_input)
        final = final_prompt()
        final_prompt_input = final.invoke({"random_style":random_style, "topic":prompt.topic, "joke":initial_result})
        result = joke_model.invoke(final_prompt_input)
        return {"joke": result.content}
    except Exception as e:
        logger.error(f"Joke generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate joke"
        )

@app.get("/", response_model=Dict[str, str])
async def root():
    return {"message": "Welcome"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")