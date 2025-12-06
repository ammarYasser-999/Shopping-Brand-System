import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import os
import time
import base64

# --- Constants ---
DB_NAME = 'market_db.db'
IMAGE_DIR = "product_images"

# Set the page configuration for wide layout (Admin view)
st.set_page_config(page_title="Admin Dashboard", layout="wide")

# Create image storage directory if it doesn't exist
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# --- Database Functions (CRUD Operations) ---

def init_db():
    """Initialize database, create tables, and insert default users. (Kept for DB structure)."""
    # NOTE: To guarantee DB structure is correct, we delete the old file if it exists.
    if os.path.exists(DB_NAME):
         # Optional: Remove if you want to keep old products, but better for testing stability
         # os.remove(DB_NAME) 
         pass 

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Users Table (Kept for data integrity, even if not used for login)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            is_admin INTEGER DEFAULT 0, 
            last_login TEXT 
        )
    ''')
    
    # Products Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            brand TEXT,
            price REAL,
            stock INTEGER,
            image_path_1 TEXT, 
            image_path_2 TEXT, 
            image_path_3 TEXT
        )
    ''')
    
    # Insert default users
    c.execute("INSERT OR IGNORE INTO users (username, password, is_admin, last_login) VALUES (?, ?, ?, ?)", 
              ('Ahmed', 'ahmed123', 1, 'Never'))
    c.execute("INSERT OR IGNORE INTO users (username, password, is_admin, last_login) VALUES (?, ?, ?, ?)", 
              ('user', '12345', 0, 'Never'))
              
    conn.commit()
    conn.close()


def add_product(name, brand, price, stock, path1, path2, path3):
    """Add a new product with image paths."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO products (name, brand, price, stock, image_path_1, image_path_2, image_path_3) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                  (name, brand, price, stock, path1, path2, path3))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def update_product_data(product_id, name, brand, price, stock):
    """Update basic product details."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE products SET name=?, brand=?, price=?, stock=? WHERE id=?", 
              (name, brand, price, stock, product_id))
    conn.commit()
    conn.close()

def update_product_images(product_id, path_col, new_path):
    """Update a specific image path."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"UPDATE products SET {path_col}=? WHERE id=?", (new_path, product_id))
    conn.commit()
    conn.close()

def get_product_by_id(product_id):
    """Retrieve product by ID."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = c.fetchone()
    conn.close()
    return product

def view_all_products():
    """Retrieve all products."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return df

def delete_product(product_id):
    """Delete a product and its image files."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Delete associated image files
    c.execute("SELECT image_path_1, image_path_2, image_path_3 FROM products WHERE id=?", (product_id,))
    paths = c.fetchone()
    if paths:
        for path in paths:
            if path and os.path.exists(path):
                os.remove(path)
        
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()

def view_all_users():
    """Retrieve all users."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT username, last_login FROM users", conn)
    conn.close()
    return df

# --- Helper Functions ---

def image_to_base64(image_path):
    """Convert image file to Base64 for HTML display."""
    try:
        if not os.path.exists(image_path):
            return ""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return ""

def save_uploaded_file(uploaded_file, product_name, index):
    """Save the uploaded file to the image directory."""
    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1]
        timestamp = int(time.time())
        file_path = os.path.join(IMAGE_DIR, f"{product_name}{index}{timestamp}.{file_extension}")
        img = Image.open(uploaded_file)
        img.save(file_path)
        return file_path
    return ""

# --- Streamlit Pages (UI) ---

def admin_page():
    """Admin Dashboard for Product Management (Direct access, no login)."""
    st.title("Admin Dashboard 🔒")
    st.subheader("Store Management and Metrics")
    st.write("---")
    
    st.sidebar.title("Admin Options")
    
    admin_action = st.sidebar.radio(
        "Select Action:",
        ["View & Edit Products", "Add New Product", "Delete Products", "User & Visitor Metrics"]
    )
    
    # --- 1. Add New Product ---
    if admin_action == "Add New Product":
        st.header("Add New Product")
        with st.form("add_product_form", clear_on_submit=True):
            product_name = st.text_input("1. Product Name")
            product_brand = st.text_input("2. Brand")
            product_price = st.number_input("3. Price", min_value=0.01, format="%.2f")
            product_stock = st.number_input("4. Stock Quantity", min_value=0, step=1)
            
            st.subheader("Add Product Images (Up to 3)")
            uploaded_file_1 = st.file_uploader("Main Image", type=["png", "jpg", "jpeg"], key="img1")
            uploaded_file_2 = st.file_uploader("Additional Image 1 (Optional)", type=["png", "jpg", "jpeg"], key="img2")
            uploaded_file_3 = st.file_uploader("Additional Image 2 (Optional)", type=["png", "jpg", "jpeg"], key="img3")
            
            submitted = st.form_submit_button("Add Product", type="primary")
            
            if submitted:
                if product_name and product_brand and product_price and product_stock and uploaded_file_1:
                    
                    path1 = save_uploaded_file(uploaded_file_1, product_name, 1)
                    path2 = save_uploaded_file(uploaded_file_2, product_name, 2)
                    path3 = save_uploaded_file(uploaded_file_3, product_name, 3)
                    
                    if add_product(product_name, product_brand, product_price, product_stock, path1, path2, path3):
                        st.success(f"Product '{product_name}' added successfully! Images saved.")
                        st.rerun() 
                    else:
                        st.error("Failed to add product. Product name might already exist.")
                else:
                    st.error("Please fill in the required fields and select a main image.")
        
    # --- 2. View & Edit Products ---
    elif admin_action == "View & Edit Products":
        st.header("View and Edit Products")
        
        # ✅ Get fresh data for display
        products_df = view_all_products()
        
        if not products_df.empty:
            
            # Comprehensive Product Display Table
            st.subheader("📊 Comprehensive Product List")
            
            products_display_df = products_df[['id', 'name', 'brand', 'price', 'stock', 'image_path_1']].copy()
            products_display_df = products_display_df.rename(columns={'id': 'ID', 'name': 'Product Name', 'price': 'Price', 'image_path_1': 'Image Path', 'brand': 'Brand', 'stock': 'Stock'})
            
            # Create HTML column for image display
            products_display_df['Image'] = products_display_df['Image Path'].apply(
                lambda x: f'<img src="data:image/png;base64,{image_to_base64(x)}" width="80" style="border-radius: 5px;"/>' if x and os.path.exists(x) else 'No Image'
            )
            
            # Display the table using HTML (Note: Removed 'brand' column from HTML display for compactness, but kept in DF)
            st.markdown(
                products_display_df[['ID', 'Image', 'Product Name', 'Brand', 'Price', 'Stock']].to_html(escape=False, index=False), 
                unsafe_allow_html=True
            )
            
            st.markdown("---")

            # Detailed Editing Section 
            st.subheader("Edit Product Details and Images")
            
            # ✅ Get fresh data for selectbox
            products_df_for_select = view_all_products()
            product_names = products_df_for_select['name'].tolist()
            
            if not product_names:
                 st.info("No products available for editing.")
                 return
                 
            selected_name_to_edit = st.selectbox("Select Product to Edit:", product_names, key="select_edit_product")
            
            selected_product = products_df_for_select[products_df_for_select['name'] == selected_name_to_edit].iloc[0]
            product_id = selected_product['id']
            
            # --- Edit Basic Data Form ---
            with st.form(key="edit_product_data_form"):
                
                new_name = st.text_input("Name", value=selected_product['name'])
                new_brand = st.text_input("Brand", value=selected_product['brand'])
                new_price = st.number_input("Price", min_value=0.01, format="%.2f", value=selected_product['price'])
                new_stock = st.number_input("Stock Quantity", min_value=0, step=1, value=selected_product['stock'])
                
                data_submitted = st.form_submit_button("Save Basic Edits", type="primary")
                
                if data_submitted:
                    update_product_data(product_id, new_name, new_brand, new_price, new_stock)
                    st.success("Basic data saved successfully.")
                    st.rerun()

            st.markdown("---")
            
            # --- Edit Images Form ---
            st.subheader("Edit/Delete Product Images")
            
            current_product = get_product_by_id(product_id)
            current_paths = {
                'image_path_1': current_product[5] if current_product else None,
                'image_path_2': current_product[6] if current_product else None,
                'image_path_3': current_product[7] if current_product else None,
            }

            img_cols = st.columns(3)
            
            for i, col_name in enumerate(['image_path_1', 'image_path_2', 'image_path_3']):
                with img_cols[i]:
                    st.markdown(f"*Image {i+1}*")
                    current_path = current_paths[col_name]
                    
                    # 1. Display Current Image
                    if current_path and os.path.exists(current_path):
                        st.image(current_path, use_column_width=True)
                        
                        # 2. Delete Option
                        if st.button(f"❌ Delete Image {i+1}", key=f"delete_img_{i}", type="secondary"): 
                            os.remove(current_path)
                            update_product_images(product_id, col_name, "")
                            st.success(f"Image {i+1} deleted successfully.")
                            st.rerun()
                    else:
                        st.info("No image currently")

                    # 3. Upload/Change Option
                    uploaded_file = st.file_uploader(f"Upload New Image {i+1}", type=["png", "jpg", "jpeg"], key=f"upload_img_{i}")
                    
                    if uploaded_file:
                        if st.button(f"Save New Image {i+1}", key=f"save_new_img_{i}", type="secondary"):
                            # If old image exists, delete it first
                            if current_path and os.path.exists(current_path):
                                os.remove(current_path)
                                
                            new_path = save_uploaded_file(uploaded_file, selected_name_to_edit, i+1)
                            update_product_images(product_id, col_name, new_path)
                            st.success(f"Image {i+1} updated successfully.")
                            st.rerun()
                            
        else:
            st.info("No products registered yet.")

    # --- 3. Delete Products ---
    elif admin_action == "Delete Products":
        st.header("Delete Product")
        products_df = view_all_products()
        
        if not products_df.empty:
            st.subheader("Available Products for Deletion")
            
            products_display = products_df[['id', 'name', 'brand', 'price', 'stock']].copy()
            products_display.columns = ['ID', 'Name', 'Brand', 'Price', 'Stock']
            st.dataframe(products_display, hide_index=True, use_container_width=True)

            product_options = {row['name']: row['id'] for index, row in products_df.iterrows()}
            selected_name = st.selectbox("Select Product to Delete:", list(product_options.keys()))
            
            if selected_name:
                if st.button(f"Permanently Delete Product '{selected_name}'", type="secondary"): 
                    selected_id = product_options[selected_name]
                    delete_product(selected_id)
                    st.warning(f"Product '{selected_name}' deleted successfully.")
                    st.rerun()
        else:
            st.info("No products to delete.")

    # --- 4. User Metrics (Display only) ---
    elif admin_action == "User & Visitor Metrics":
        st.header("User and Visitor Metrics")
        
        st.subheader("Registered User Logins")
        users_df = view_all_users()
        users_df = users_df.rename(columns={'username': 'Username', 'last_login': 'Last Login'})
        st.dataframe(users_df, use_container_width=True, hide_index=True)
        
        st.subheader("Total User Count")
        st.metric(label="Registered Users / Visitors", value=len(users_df))


# --- Main Execution ---

if __name__ == '__main__':
    # Initialize DB (Keeps the DB file in the working directory: market_db.db)
    init_db()
    
    # Direct access to the Admin Page (Login removed)
    admin_page()