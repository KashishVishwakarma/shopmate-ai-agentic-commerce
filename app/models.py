from pydantic import BaseModel, Field
from typing import List, Optional

class Product(BaseModel):
    id: str
    name: str
    description: str
    price: float
    stock: int

class CartItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int = Field(default=1, ge=1)

class Cart(BaseModel):
    items: List[CartItem] = []
    total: float = 0.0

class ChatRequest(BaseModel):
    message: str = Field(..., example="Can you find mechanical keyboards under $100 and add one to my cart?")
    session_id: Optional[str] = Field(default="default_session")

class ChatResponse(BaseModel):
    response: str
    session_id: str
