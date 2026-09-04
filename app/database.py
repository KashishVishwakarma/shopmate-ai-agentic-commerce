import sqlite3
from typing import List, Dict, Any, Optional

DB_NAME = "commerce.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            rating REAL NOT NULL,
            image_url TEXT NOT NULL
        )
    """)
    
    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            product_id TEXT NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            customer_email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Populate 8 varied catalog items if table is empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_products = [
            (
                "prod_1",
                "Sony WH-1000XM5 Wireless Headphones",
                "Audio",
                "Industry-leading noise cancellation with 30-hour battery life, crystal clear hands-free calling, and multi-point Bluetooth connection.",
                399.99,
                14,
                4.8,
                "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80"
            ),
            (
                "prod_2",
                "Keychron Q1 Pro Custom Mechanical Keyboard",
                "Accessories",
                "Full aluminum CNC machined body, hot-swappable switches, double-gasket design, and wireless QMK/VIA programmable keys.",
                199.00,
                9,
                4.9,
                "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=80"
            ),
            (
                "prod_3",
                "Dell UltraSharp 34-inch Curved USB-C Monitor",
                "Monitors",
                "WQHD 3440 x 1440 resolution, IPS panel, 90W power delivery via USB-C hub, and ultra-thin bezels for productivity workstations.",
                589.99,
                6,
                4.7,
                "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&q=80"
            ),
            (
                "prod_4",
                "Anker 737 Power Bank (PowerCore 24K)",
                "Power",
                "Ultra-powerful 140W fast charging with high capacity 24,000mAh battery and smart digital display showing live output rates.",
                129.99,
                22,
                4.6,
                "https://images.unsplash.com/photo-1609592424307-e234382e88a0?w=800&q=80"
            ),
            (
                "prod_5",
                "Logitech MX Master 3S Wireless Mouse",
                "Accessories",
                "Quiet Click switches with 8,000 DPI track-on-glass optical sensor and ergonomic thumb scroll wheel.",
                99.99,
                18,
                4.9,
                "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&q=80"
            ),
            (
                "prod_6",
                "Apple MacBook Pro 16 M3 Max",
                "Laptops",
                "Liquid Retina XDR display, 36GB unified memory, 1TB blazing-fast SSD, and all-day 22-hour battery life for creative professionals.",
                2499.00,
                4,
                5.0,
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&q=80"
            ),
            (
                "prod_7",
                "CalDigit TS4 Thunderbolt 4 Dock",
                "Docks",
                "18 ports of connectivity including 98W host charging, 2.5 Gigabit Ethernet, DisplayPort 1.4, and multiple high-speed USB-C lanes.",
                399.95,
                8,
                4.7,
                "https://images.unsplash.com/photo-1544652478-6653e09f18a2?w=800&q=80"
            ),
            (
                "prod_8",
                "Bose SoundLink Flex Portable Speaker",
                "Audio",
                "Waterproof and dustproof (IP67) outdoor Bluetooth speaker with PositionIQ technology and deep, balanced sound.",
                149.00,
                30,
                4.5,
                "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&q=80"
            )
        ]
        cursor.executemany(
            """INSERT INTO products 
               (id, name, category, description, price, stock, rating, image_url) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            sample_products
        )
    
    conn.commit()
    conn.close()

def query_products(keyword: str = "") -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = "SELECT * FROM products WHERE name LIKE ? OR description LIKE ? OR category LIKE ?"
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_product(product_id: str) -> Optional[Dict[str, Any]]:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def place_order(product_id: str, quantity: int, customer_email: str) -> Optional[Dict[str, Any]]:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    if not product or product["stock"] < quantity:
        conn.close()
        return None
    
    # Decrement inventory stock
    cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (quantity, product_id))
    
    import uuid
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    
    cursor.execute("""
        INSERT INTO orders (order_id, product_id, product_name, price, quantity, customer_email)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (order_id, product_id, product["name"], product["price"], quantity, customer_email))
    
    conn.commit()
    conn.close()
    
    return {
        "order_id": order_id,
        "product_name": product["name"],
        "quantity": quantity,
        "total": round(product["price"] * quantity, 2),
        "customer_email": customer_email
    }
