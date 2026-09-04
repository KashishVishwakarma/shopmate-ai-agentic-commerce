from app.database import query_products, get_product
import re

class SmartCommerceAgent:
    def invoke(self, inputs: dict) -> dict:
        text = inputs.get("input", "").strip().lower()
        
        # 1. Greetings
        if text in ["hi", "hello", "hey", "sup", "greetings"]:
            return {
                "output": "Hello! I am your AI Shopping Assistant. You can ask me to search gear (e.g., 'show laptops', 'best headphones'), ask for features/specs, or check pricing and stock."
            }

        # 2. Cart inquiries
        if "cart" in text:
            return {
                "output": "You can inspect your cart anytime or click 'View & Order' on any product card to initiate an instant checkout."
            }

        # 3. Clean keywords to query database
        # Strip common conversational filler words
        stop_words = ["find", "search", "show", "me", "what", "is", "the", "are", "tell", "about", 
                      "check", "give", "details", "feature", "features", "do", "you", "have", "any", "look", "for", "please"]
        
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        search_terms = [w for w in tokens if w not in stop_words]
        
        # Search query matching
        results = []
        if search_terms:
            for term in search_terms:
                matches = query_products(term)
                for item in matches:
                    if item not in results:
                        results.append(item)
        else:
            # Fallback to general search if user typed "show products"
            results = query_products("")

        # 4. Handle Found Products
        if results:
            # If user asked about a specific single product's features or price
            if len(results) == 1 or any(k in text for k in ["detail", "feature", "spec", "price", "stock"]):
                p = results[0]
                return {
                    "output": (
                        f"Here are the details for **{p['name']}**:\n\n"
                        f"• **Category:** {p['category']}\n"
                        f"• **Price:** ${p['price']:.2f}\n"
                        f"• **Rating:** ★ {p['rating']} / 5.0\n"
                        f"• **Availability:** {p['stock']} units left in stock\n"
                        f"• **Key Features:** {p['description']}\n\n"
                        f"Would you like to place an order for this item?"
                    )
                }

            # If multiple products match
            summary_lines = []
            for p in results[:3]:  # Top 3 matches
                summary_lines.append(f"• **{p['name']}** — ${p['price']:.2f} (★ {p['rating']} | {p['stock']} in stock)")

            matched_list = "\n".join(summary_lines)
            return {
                "output": (
                    f"I found {len(results)} matching product(s):\n\n"
                    f"{matched_list}\n\n"
                    f"Type the name of any product to see full specs or click 'View & Order' on the card."
                )
            }

        # 5. Fallback when nothing is found
        return {
            "output": f"I couldn't find any items matching '{text}'. Try searching for **laptops**, **headphones**, **keyboards**, **monitors**, or **chargers**."
        }

def build_commerce_agent():
    return SmartCommerceAgent()
