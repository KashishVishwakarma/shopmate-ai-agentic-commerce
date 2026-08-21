from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.agent import build_commerce_agent
from app.database import init_db
from app.models import ChatRequest, ChatResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="AI Agentic Commerce API", lifespan=lifespan)

# Mount static files folder
app.mount("/static", StaticFiles(directory="static"), name="static")

agent_executor = build_commerce_agent()


@app.get("/")
def serve_home():
    return FileResponse("static/index.html")


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
