"""Here is contained all operations to be performed over the 'sales' table."""

from __future__ import annotations

import sqlite3
from typing import Optional

import pandas as pd

TABLE_CATEGORIES = ["Electronics", "Clothing"]

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


def fetch_data(
    category: Optional[str] = None, date_range: Optional[tuple[str, str]] = None
) -> pd.DataFrame:
    """Fetching data from the table with optional conditions.

    Parameters
    ----------
    category : str, optional
        Category corresponding to the data.
    date_range : tuple of two str, optional
        Range of dates as (min, max), defined as strings. Each date must be defined as
        'YYYY-MM-DD'.
    """
    query = "SELECT product, SUM(sales) as total_sales FROM sales"
    conditions = []
    if category:
        conditions.append(f"category = '{category}'")
    if date_range:
        conditions.append(f"date BETWEEN '{date_range[0]}' AND '{date_range[1]}'")
    if conditions:
        query += "WHERE " + " AND ".join(conditions)
    query += "GROUP BY product"
    return pd.read_sql(query, conn)
