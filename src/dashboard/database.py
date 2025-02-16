"""Here is contained all operations to be performed over the 'sales' table."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Optional

import pandas as pd

TABLE_CATEGORIES = ["Electronics", "Clothing"]


@contextmanager
def get_db_connection() -> sqlite3.connect:
    """Context manager for database connection."""
    conn = sqlite3.connect("sales.db")
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()


def init_table() -> None:
    """Table initialization.

    Creation of the table 'sales' when this one does not exist.
    All values of the table are set to some default values by removing all data any
    previous existing table had and commiting it again.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Creating the table:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT NOT NULL,
                category TEXT NOT NULL,
                sales REAL NOT NULL,
                date TEXT NOT NULL
            )
        """)
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
    with get_db_connection() as conn:
        query = "SELECT product, SUM(sales) as total_sales FROM sales"
        conditions, params = [], []
        if category:
            conditions.append("category = ?")
            params.append(category)
        if date_range:
            conditions.append("date BETWEEN ? AND ?")
            params.extend(date_range)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " GROUP BY product"
        return pd.read_sql(query, conn, params=params)
