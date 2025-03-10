"""Operations over a database with SQLite.

This script will create an 'inventory.db' file. If the file already exists and the
script is re-run, then the table will be updated again.
"""

import sqlite3

# Connect to SQLite database (or create it).
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create a 'products' table:
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL CHECK (price > 0),
        quantity INTEGER NOT NULL
    )
""")


def add_product(name: str, price: float, quantity: int):
    """Inserting a new product into the table.
    The 'id' is not required due to the 'AUTOINCREMENT', which will fill this up
    automatically with the next free unused integer.
    All other arguments are the same as the columns of the table.
    """
    try:
        cursor.execute(
            "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
            (name, price, quantity),
        )
        conn.commit()
        print(f"Added product: {name}")
    except sqlite3.IntegrityError as e:
        print("Could not add the product due to the following issue -->", e)


def get_products():
    """Selecting all the rows from the 'products' table."""
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()


def update_product(product_id: int, new_quantity: float):
    """Updating a single product to modify its quantity.
    By only providing the id, the code will also get the name of the product.
    """
    cursor.execute("SELECT name FROM products WHERE id = ?", (product_id,))
    result = cursor.fetchone()

    if result:
        product_name = result[0]
        cursor.execute(
            "UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id)
        )
        conn.commit()
        print(
            f"Updated product '{product_name}' (ID {product_id})"
            f" to quantity {new_quantity}"
        )
    else:
        print(f"Product ID {product_id} not found.")


def delete_product(product_name: str):
    """Removing the whole row of the product from the table."""
    cursor.execute("SELECT id FROM products WHERE name = ?", (product_name,))
    result = cursor.fetchone()

    if result:
        product_id = result[0]
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        print(f"Deleted product '{product_name}' (ID {product_id})")
    else:
        print(f"Product '{product_name}' not found.")


# Example usage
if __name__ == "__main__":
    # Adding initial products
    add_product("Laptop", 999.99, 10)
    add_product("Phone", 449.99, 20)
    print("Products:", get_products())

    # Trying to add an incorrect product (negative value)
    add_product("Guitar", -50, 3)

    # Updating a product
    update_product(1, 5)
    print("Products after update:", get_products())

    # Deleting a product
    delete_product("Phone")
    print("Products after deletion:", get_products())

    # Adding a new product after having other deleted (see the new value of 'id')
    add_product("Keyboard", 80.00, 15)
    print("Products after new addition:", get_products())
