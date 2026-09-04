from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from app.agent import build_commerce_agent
from app.database import init_db, query_products, get_product, place_order
from app.models import ChatRequest

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="AI Agentic Commerce API", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

agent_executor = build_commerce_agent()

class PlaceOrderRequest(BaseModel):
    product_id: str
    quantity: int = 1
    email: EmailStr

@app.get("/")
def serve_home():
    return FileResponse("static/index.html")

@app.get("/api/products")
def list_products(search: str = ""):
    return query_products(search)

@app.get("/api/products/{product_id}")
def view_product(product_id: str):
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/orders/place")
def execute_order(request: PlaceOrderRequest):
    order = place_order(request.product_id, request.quantity, request.email)
    if not order:
        raise HTTPException(status_code=400, detail="Unable to place order. Insufficient stock or invalid product.")
    return order

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = agent_executor.invoke({
            "input": request.message,
            "chat_history": []
        })
        
        matched_items = []
        user_query = request.message.lower()
        if any(w in user_query for w in ["find", "search", "show", "look for", "catalog", "get"]):
            cleaned = user_query.replace("find", "").replace("search", "").replace("show", "").replace("look for", "").strip()
            matched_items = query_products(cleaned)
            
        return {
            "response": response["output"],
            "session_id": request.session_id or "guest",
            "matched_products": matched_items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
