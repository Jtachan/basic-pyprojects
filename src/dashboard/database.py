"""Here is contained all operations to be performed over the 'sales' table."""

import sqlite3

# Connect to the database:
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Creating the table:
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT NOT NULL,
        category TEXT NOT NULL,
        sales REAL NOT NULL,
        date TEXT NOT NULL,
    )
""")
conn.commit()


def reset_table() -> None:
    """Purging the data from the table and populating it to default values."""
    # Deletion of all previous data:
    cursor.execute("DELETE FROM sales")

    # Population to default values:
    sales_data = [
        ("Laptop", "Electronics", 1200.50, "2023-10-01"),
        ("Phone", "Electronics", 800.00, "2023-10-02"),
        ("Shirt", "Clothing", 25.99, "2023-10-03"),
        ("Jeans", "Clothing", 45.99, "2023-10-04"),
        ("Tablet", "Electronics", 600.00, "2023-10-05"),
        ("Shoes", "Clothing", 70.00, "2023-10-06"),
    ]
    cursor.executemany(
        "INSERT INTO sales (product, category, sales, date) VALUES (?, ?, ?, ?)",
        sales_data,
    )
    conn.commit()
