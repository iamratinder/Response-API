from fastapi import FastAPI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


chat_model = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

class Prompt(BaseModel):
    text: str

@app.post("/chat")
async def chat_endpoint(prompt: Prompt):
    result = chat_model.invoke(prompt.text)
    return {"response": result.content}

@app.get("/")
async def root():
    return {"message": "Welcome to the Chat API"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)