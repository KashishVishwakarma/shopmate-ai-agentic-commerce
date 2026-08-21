import sqlite3
from typing import List, Dict, Any, Optional

DB_NAME = "commerce.db"

def init_db():
    """Initialize SQLite database with a sample product catalog."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            session_id TEXT,
            product_id TEXT,
            quantity INTEGER,
            PRIMARY KEY (session_id, product_id)
        )
    """)
    
    # Seed initial items if empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ("prod_1", "Wireless Noise-Canceling Headphones", "Over-ear Bluetooth headphones with active noise cancellation", 149.99, 15),
            ("prod_2", "Ergonomic Mechanical Keyboard", "RGB backlit keyboard with hot-swappable switches", 89.99, 8),
            ("prod_3", "USB-C Multiport Hub", "7-in-1 adapter with 4K HDMI, USB 3.0, and 100W PD", 34.50, 25),
            ("prod_4", "4K Ultra-Wide Monitor", "34-inch curved display for productivity and gaming", 399.00, 4)
        ]
        cursor.executemany(
            "INSERT INTO products (id, name, description, price, stock) VALUES (?, ?, ?, ?, ?)",
            sample_products
        )
    
    conn.commit()
    conn.close()

def query_products(keyword: str) -> List[Dict[str, Any]]:
    """Search products by name or description."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT * FROM products WHERE name LIKE ? OR description LIKE ?"
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_product(product_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single product by ID."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
