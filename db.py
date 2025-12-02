import sqlite3

DB_NAME = "database.db"


def get_connection():

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ================================================
#   TEAM 1 => FUNCTIONS (LOGIN / REGISTER)
# ================================================

def register_user(username, password, role='user'):

       # LOGIN NEW USER

    try:
        conn = get_connection()
        conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                     (username, password, role))
        conn.commit()
        conn.close()
        return True                         # REGISTER SUCCESSFULLY
    except sqlite3.IntegrityError:
        return False                       # USERNAME REPEATED


def login_check(username, password):

     # CHECK LOGIN PROCESS

    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE username=? AND password=?",
                        (username, password)).fetchone()
    conn.close()
    if user:
        return dict(user)  # RETURN DATA OF USER
    return None           # INVALID DATAا


# =========================================================
#      TEAM 2 FUNCTIONS (ADMIN DASHBOARD + CRUD PRODUCTS)
# =========================================================

def add_product(name, category_id, size, color, salary, stock, image_path):

 # ADD NEW PRODUCT

    conn = get_connection()
    conn.execute("""
                 INSERT INTO products (name, category_id, size, color, salary, stock, image)
                 VALUES (?, ?, ?, ?, ?, ?, ?)
                 """, (name, category_id, size, color, salary, stock, image_path))
    conn.commit()
    conn.close()


def edit_product(product_id, name, salary, stock):

    # EDIT PRODUCT

    conn = get_connection()
    conn.execute("UPDATE products SET name=?, salary=?, stock=? WHERE id=?",
                 (name, salary, stock, product_id))
    conn.commit()
    conn.close()


def delete_product(product_id):

    # DELETE PRODUCT

    conn = get_connection()
    conn.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()


def get_all_products():

    #VIEW PRODUCT

    conn = get_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return [dict(row) for row in products]


# =============================================
#   TEAM 3 FUNCTIONS (USER HOME + CART SYSTEM)
# =============================================

def get_products_for_home():

     # VIEW PRODUCTS IN HOME PAGE

    return get_all_products()           # SAME VIEW FUNCTION


def add_to_cart(user_id, product_id, quantity=1):

    # ADD NEW CART

    conn = get_connection()
    conn.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
                 (user_id, product_id, quantity))
    conn.commit()
    conn.close()


def view_cart(user_id):

    # VIEW CART PRODUCTS

    conn = get_connection()

    query = """
            SELECT cart.id, products.name, products.salary, cart.quantity, products.image
            FROM cart
                     JOIN products ON cart.product_id = products.id
            WHERE cart.user_id = ? \
            """
    items = conn.execute(query, (user_id,)).fetchall()
    conn.close()
    return [dict(row) for row in items]


def remove_from_cart(cart_id):

    #REMOVE PRODUCTS FROM CART

    conn = get_connection()
    conn.execute("DELETE FROM cart WHERE id=?", (cart_id,))
    conn.commit()
    conn.close()


# ====================================================
#   TEAM 4 FUNCTIONS (Payment + Feedback)
# ====================================================

def save_payment(order_id, card_number, cvv, expire_date):

    #SAVE PAYMENT METHOD *VISA*

    conn = get_connection()
    conn.execute("INSERT INTO payment (order_id, card_number, cvv, expire_date) VALUES (?, ?, ?, ?)",
                 (order_id, card_number, cvv, expire_date))
    conn.commit()
    conn.close()


def save_feedback(user_id, message):

    #SAVE FEEDBACK

    conn = get_connection()
    conn.execute("INSERT INTO feedback (user_id, message) VALUES (?, ?)",
                 (user_id, message))
    conn.commit()
    conn.close()


# ===================================
# TESTING (TO MAKE SURE OUR JOB IS DONE HERE , **3BDO && 3MMAR** <3)
# ===================================
if __name__ == "__main__":
    print("✅ Team 5: Testing Database Functions...")

    # 1. Test Register
    if register_user("admin", "admin123", "admin"):
        print("   -> Admin User Created Successfully")
    else:
        print("   -> User already exists")

    # 2. Test Login
    user = login_check("admin", "admin123")
    if user:
        print(f"   -> Login Verified for: {user['username']} (Role: {user['role']})")

    print("✅ Team 5 Tasks Completed: DB Setup + CRUD Functions Ready.")

    # BEST WISHES HOMIES ;)