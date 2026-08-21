from langchain.tools import tool

# Mock product database
CATALOG = [
    {"id": "prod_1", "name": "Wireless Noise-Canceling Headphones", "price": 149.99, "stock": 12},
    {"id": "prod_2", "name": "Ergonomic Mechanical Keyboard", "price": 89.99, "stock": 5},
    {"id": "prod_3", "name": "USB-C Multiport Hub", "price": 34.50, "stock": 20},
]

CART = []

@tool
def search_products(query: str) -> list[dict]:
    """Search the product catalog by name or keyword."""
    return [p for p in CATALOG if query.lower() in p["name"].lower()]

@tool
def add_to_cart(product_id: str, quantity: int = 1) -> str:
    """Add a product to the user's shopping cart."""
    product = next((p for p in CATALOG if p["id"] == product_id), None)
    if not product:
        return f"Product with ID {product_id} not found."
    if product["stock"] < quantity:
        return f"Insufficient stock for {product['name']}."
    
    CART.append({"product_id": product_id, "name": product["name"], "price": product["price"], "quantity": quantity})
    return f"Added {quantity}x {product['name']} to cart."

@tool
def view_cart() -> list[dict]:
    """View current items and total inside the shopping cart."""
    return CART
