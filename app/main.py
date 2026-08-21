from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.models import ChatRequest, ChatResponse
from app.database import init_db
from app.agent import build_commerce_agent

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs when the server boots up (creates tables & seeds catalog)
    init_db()
    yield

app = FastAPI(title="AI Agentic Commerce API", lifespan=lifespan)
agent_executor = build_commerce_agent()

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Agentic Commerce API"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = agent_executor.invoke({
            "input": request.message,
            "chat_history": []
        })
        return ChatResponse(
            response=response["output"],
            session_id=request.session_id or "default_session"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

