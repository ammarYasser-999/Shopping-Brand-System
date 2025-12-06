import streamlit as st
import pandas as pd
from PIL import Image
import os
import time
import base64
import db  # 1. هنا السر: استدعينا ملف تيم 5 عشان نكلم الداتا بيز الأصلية

# --- إعدادات الصفحة ---
# بنحطها في try-except عشان لو الملف ده اتفتح كجزء من main.py ميعملش error
try:
    st.set_page_config(page_title="Admin Dashboard", layout="wide")
except:
    pass

IMAGE_DIR = "product_images"

# إنشاء فولدر الصور لو مش موجود
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# --- دوال مساعدة (للصور) ---
def save_uploaded_file(uploaded_file, product_name):
    """حفظ الصورة المرفوعة في الفولدر وإرجاع المسار"""
    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1]
        timestamp = int(time.time())
        # تنظيف الاسم عشان ميعملش مشاكل في الويندوز
        safe_name = "".join([c for c in product_name if c.isalpha() or c.isdigit()]).rstrip()
        file_path = os.path.join(IMAGE_DIR, f"{safe_name}_{timestamp}.{file_extension}")
        
        img = Image.open(uploaded_file)
        img.save(file_path)
        return file_path
    return None

# --- صفحة الأدمن الرئيسية ---
def admin_page():
    st.title("Admin Dashboard 🔒")
    st.markdown("### 🛒 Management System (Connected to Main DB)")
    st.write("---")
    
    # القائمة الجانبية
    st.sidebar.title("Control Panel")
    action = st.sidebar.radio(
        "Choose Operation:",
        ["View All Products", "Add New Product", "Edit Product", "Delete Product"]
    )
    
    # ==========================================
    # 1. VIEW PRODUCTS (عرض المنتجات)
    # ==========================================
    if action == "View All Products":
        st.header("📦 Current Inventory")
        
        # بننادي دالة تيم 5 لجلب المنتجات
        products = db.get_all_products()
        
        if products:
            # تحويل القائمة لجدول Pandas عشان العرض يبقى شيك
            df = pd.DataFrame(products)
            
            # ترتيب وتنظيف شكل الجدول للعرض
            if not df.empty:
                # نختار الأعمدة المهمة بس للعرض
                display_df = df[['id', 'name', 'salary', 'stock', 'size', 'color', 'category_id']]
                st.dataframe(display_df, use_container_width=True)
                
                st.write("---")
                st.subheader("🖼️ Product Gallery")
                
                # عرض الصور في شبكة (Grid)
                cols = st.columns(4)
                for index, row in df.iterrows():
                    with cols[index % 4]:
                        # التأكد إن فيه صورة والمسار موجود فعلاً
                        if row.get('image') and os.path.exists(row['image']):
                            st.image(row['image'], caption=f"{row['name']}\n{row['salary']} EGP")
                        else:
                            st.info(f"No Image: {row['name']}")
        else:
            st.info("The database is currently empty. Go to 'Add New Product' to start.")

    # ==========================================
    # 2. ADD PRODUCT (إضافة منتج)
    # ==========================================
    elif action == "Add New Product":
        st.header("➕ Add New Product")
        
        with st.form("add_product_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Product Name")
                # حولنا الـ Brand لـ Category ID عشان الداتا بيز بتاعتك
                category_id = st.selectbox("Category", [1, 2, 3, 4], format_func=lambda x: f"Category {x}")
                salary = st.number_input("Price (EGP)", min_value=1.0, step=10.0)
            
            with col2:
                # خانات زيادة عشان الداتا بيز بتاعتك محتاجاها
                size = st.selectbox("Size", ["S", "M", "L", "XL", "Free Size"])
                color = st.text_input("Color", "Black")
                stock = st.number_input("Stock Quantity", min_value=1, step=1)

            st.subheader("Product Image")
            uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
            
            submitted = st.form_submit_button("Save Product", type="primary")
            
            if submitted:
                if name and salary and stock and uploaded_file:
                    # 1. نحفظ الصورة على الجهاز
                    image_path = save_uploaded_file(uploaded_file, name)
                    
                    # 2. نبعت البيانات لدالة تيم 5 (add_product)
                    try:
                        db.add_product(name, category_id, size, color, salary, stock, image_path)
                        st.success(f"✅ Product '{name}' added successfully to the Main Database!")
                    except Exception as e:
                        st.error(f"Error adding product: {e}")
                else:
                    st.warning("⚠️ Please fill all fields and upload an image.")

    # ==========================================
    # 3. EDIT PRODUCT (تعديل منتج)
    # ==========================================
    elif action == "Edit Product":
        st.header("✏️ Edit Product Details")
        
        products = db.get_all_products()
        if products:
            # عمل قائمة منسدلة بأسماء المنتجات للاختيار منها
            product_options = {f"{p['name']} (ID: {p['id']})": p for p in products}
            selected_option = st.selectbox("Select Product to Edit", list(product_options.keys()))
            
            # جلب بيانات المنتج المختار
            selected_product = product_options[selected_option]
            
            with st.form("edit_form"):
                new_name = st.text_input("Name", value=selected_product['name'])
                new_salary = st.number_input("Price", value=float(selected_product['salary']))
                new_stock = st.number_input("Stock", value=int(selected_product['stock']))
                
                # دالة edit_product في db.py بتقبل (id, name, salary, stock)
                if st.form_submit_button("Update Product"):
                    db.edit_product(selected_product['id'], new_name, new_salary, new_stock)
                    st.success("Product updated successfully!")
                    st.rerun()
        else:
            st.info("No products available to edit.")

    # ==========================================
    # 4. DELETE PRODUCT (مسح منتج)
    # ==========================================
    elif action == "Delete Product":
        st.header("🗑️ Delete Product")
        
        products = db.get_all_products()
        if products:
            product_dict = {f"{p['name']} (ID: {p['id']})": p['id'] for p in products}
            
            selected_name = st.selectbox("Select Product to Delete", list(product_dict.keys()))
            
            st.warning("⚠️ This action cannot be undone.")
            if st.button("Permanently Delete", type="primary"):
                product_id = product_dict[selected_name]
                
                # مناداة دالة المسح من تيم 5
                db.delete_product(product_id)
                st.success("Product deleted from Database.")
                time.sleep(1)
                st.rerun()
        else:
            st.info("No products to delete.")

# تشغيل الصفحة (للتجربة المباشرة)
if __name__ == "__main__":
    admin_page()