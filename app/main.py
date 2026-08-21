from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import build_commerce_agent
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(title="AI Agentic Commerce API")
agent_executor = build_commerce_agent()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_user"

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Agentic Commerce API"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = agent_executor.invoke({
            "input": request.message,
            "chat_history": []
        })
        return {"response": response["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
