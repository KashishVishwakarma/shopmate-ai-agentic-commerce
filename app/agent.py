from app.tools import search_products, add_to_cart, view_cart

class MockAgentExecutor:
    def invoke(self, inputs: dict) -> dict:
        user_text = inputs.get("input", "").lower()

        if "search" in user_text or "find" in user_text:
            results = search_products.invoke({"query": ""})
            return {"output": f"Found items: {results}"}
        
        elif "cart" in user_text:
            items = view_cart.invoke({})
            return {"output": f"Your current cart: {items}"}
            
        return {"output": "Mock Agent: I can help you search products or view your cart. (No API key needed!)"}

def build_commerce_agent():
    return MockAgentExecutor()
