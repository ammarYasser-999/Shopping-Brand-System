import streamlit as st
import db  # بنستدعي ملف تيم 5
import sqlite3 # محتاجين دي بس عشان نظبط بيانات البدء
import base64

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Fashion Brand", layout="wide")

def set_video_bg(video_path):
    """
    دالة بتاخد مسار الفيديو وتحطه خلفية للموقع كله
    """
    try:
        with open(video_path, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        
        video_tag = f"""
        <style>
            .stApp {{
                background: transparent;
            }}
            #myVideo {{
                position: fixed;
                right: 0;
                bottom: 0;
                min-width: 100%; 
                min-height: 100%;
                z-index: -1;
                object-fit: cover;
                opacity: 0.8; /* شفافية الفيديو عشان الكلام يبان (ممكن تغيرها) */
            }}
            /* تعديل لون النصوص عشان تبان فوق الفيديو */
            h1, h2, h3, h4, p, span, div {{
                text-shadow: 2px 2px 4px #000000; /* ظل أسود للكلام */
            }}
        </style>
        <video autoplay muted loop id="myVideo">
            <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
        </video>
        """
        st.markdown(video_tag, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("⚠️ ملف الفيديو مش موجود! تأكد إن اسمه bg_video.mp4 جوة فولدر images")
    except Exception as e:
        pass

# --- تشغيل الخلفية هنا ---
# السطر ده هو اللي بينادي الدالة اللي فوق
set_video_bg('images/bg_video.mp4')

# ==========================================

# ==========================================
# دالة تغيير الخط والألوان (Styling)
# ==========================================
def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. استيراد خط 'Cairo' من جوجل */
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;700&display=swap');

        /* 2. تطبيق الخط على كل الموقع */
        html, body, [class*="css"] {
            font-family: 'Cairo', sans-serif;
        }

        /* 3. تغيير لون النصوص */
        /* هنا خلينا اللون أبيض عشان يبان مع الفيديو */
        h1, h2, h3, h4, h5, h6, p, span, div, label {
            color: #FFFFFF !important;  /* غير الكود ده لو عايز لون تاني */
            text-shadow: 2px 2px 5px #000000; /* ظل أسود للكلام عشان القراءة */
        }
        
        /* 4. تظبيط لون الأزرار */
        .stButton button {
            color: #000000 !important; /* لون الكلام جوه الزرار (أسود) */
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

# تشغيل الستايل
apply_custom_style()
# ==========================================
# دالة سحرية لتهيئة البيانات (من غير ما نلمس ملفات تيم 5)
# ==========================================
def init_data_fix():
    # 1. إنشاء الداتابيز لو مش موجودة
    try:
        import init_db
    except:
        pass
    
    # 2. إضافة التصنيفات (Categories) يدوياً 
    # (هنفترض: 1 = رجالي, 2 = حريمي)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (1, 'Men')")
        cursor.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (2, 'Women')")
        conn.commit()
    except:
        pass
    
    # 3. هل فيه منتجات؟ لو مفيش، ضيف شوية
    # 3. هل فيه منتجات؟ لو مفيش، ضيف شوية
    existing_products = db.get_all_products()
    if not existing_products:
        # الترتيب: (الاسم, رقم القسم, المقاس, اللون, السعر, المخزون, مسار الصورة)
        
        db.add_product("Classic Shirt", 1, "M", "White", 450.0, 10, "images/shirt.jpg.jpg")
        db.add_product("Slim Jeans", 1, "32", "Blue", 600.0, 15, "images/jeans.jpg.jpg")
      
        db.add_product("Summer Dress", 2, "S", "Red", 750.0, 8, "images/dress.jpeg")
        db.add_product("Dress", 2, "OneSize", "Brown", 950.0, 20, "images/dress2.jpg")
    conn.close()

# تشغيل التهيئة
init_data_fix()

# ==========================================
#  الواجهة 
# ==========================================

# --- 2. متغيرات الجلسة (Session State) ---
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'selected_cat_id' not in st.session_state: 
    st.session_state['selected_cat_id'] = None # بنستخدم ID مش اسم
if 'selected_product' not in st.session_state:
    st.session_state['selected_product'] = None
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = 1  # يوزر وهمي للتجربة

def go_to(page_name):
    st.session_state['page'] = page_name
    st.rerun()

# --- 3. تصميم الصفحات ---

# === الصفحة الرئيسية (HOMEPAGE) ===
def render_home():
    st.markdown("<h1 style='text-align: center; color: #00FFFF;'> RAWNAQ BRAND </h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #666;'>Style for Men & Women</h4>", unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👔 SHOP MEN COLLECTION", use_container_width=True):
            st.session_state['selected_cat_id'] = 1 # رقم القسم الرجالي في الداتابيز
            go_to('category')   
    with col2:
        if st.button("👗 SHOP WOMEN COLLECTION", use_container_width=True):
            st.session_state['selected_cat_id'] = 2 # رقم القسم الحريمي في الداتابيز
            go_to('category')

    st.write("")
    try:
       st.image("images/home.jpg", use_container_width=True)
    except:
        st.write("Welcome Image")

# === صفحة القسم (CATEGORY PAGE) ===
def render_category():
    cat_id = st.session_state['selected_cat_id']
    cat_name = "Men" if cat_id == 1 else "Women"
    
    if st.button("⬅️ Back to Home"):
        go_to('home')
        
    st.title(f"{cat_name} Section")
    
    # 1. نجيب كل المنتجات من تيم 5
    all_products = db.get_all_products()
    
    # 2. نفلترها عندنا احنا (عشان تيم 5 معندوش دالة فلترة)
    # بنشوف لو category_id بتاع المنتج بيساوي القسم اللي اخترناه
    products = [p for p in all_products if p['category_id'] == cat_id]
    
    if not products:
        st.warning(f"عفواً، لا توجد منتجات حالياً! 😅")
        return

    # عرض المنتجات
    cols = st.columns(4)
    for i, product in enumerate(products):
        with cols[i % 4]:
            with st.container(border=True):
                try: st.image(product['image'], use_container_width=True)
                except: st.write("No Img")
                
                st.subheader(product['name'])
                # تيم 5 مسمي السعر salary
                st.write(f"**{product['salary']} EGP**")
                
                # إضافة للسلة (الزرار الصغير)
                if st.button("Add 🛒", key=f"add_{product['id']}", use_container_width=True):
                    # ملحوظة: تيم 5 مش بيدعم تسجيل المقاس، فمش هنبعته
                    db.add_to_cart(st.session_state['user_id'], product['id'], 1)
                    st.toast(f"✅ {product['name']} added!")

                # التفاصيل
                if st.button("Details 📄", key=f"view_{product['id']}", use_container_width=True):
                    st.session_state['selected_product'] = product
                    go_to('product')

# === صفحة المنتج (PRODUCT PAGE) ===
def render_product():
    if st.button("⬅️ Back"):
        go_to('category')

    product = st.session_state['selected_product']

    if product:
        c1, c2 = st.columns([1, 1])
        with c1:
            try: st.image(product['image'], use_container_width=True)
            except: st.write("No Img")
        with c2:
            st.title(product['name'])
            st.subheader(f"{product['salary']} EGP")
            
            st.write(f"**Description:**")
            # عشان الداتابيز مفيهاش وصف، هنعرض المعلومات المتاحة
            desc_text = f"""
            هذا منتج رائع من مجموعتنا المتميزة.
            - اللون المتاح: {product['color']}
            - المقاس الافتراضي: {product['size']}
            - الخامة: قطن ممتاز (افتراضي)
            """
            st.info(desc_text)
            st.divider()
            
            # اختيار المقاس (هنخليه شكلي لحد ما تيم 5 يضيفه في الداتابيز)
            size = st.selectbox("Choose Size", ["S", "M", "L", "XL", "XXL"])
            qty = st.number_input("Quantity", 1, 10, 1)
            
            if st.button("Add to Cart 🛒", type="primary"):
                # بنبعت الكمية بس، المقاس مش هيتسجل حالياً عشان قاعدة البيانات ناقصة عمود
                db.add_to_cart(st.session_state['user_id'], product['id'], qty)
                st.success(f"✅ Added to cart! (Size: {size})")

# === صفحة السلة (CART PAGE) ===
def render_cart():
    st.title("🛒 Your Shopping Cart")
    if st.button("⬅️ Back to Shopping"):
        go_to('home')

    items = db.view_cart(st.session_state['user_id'])
    
    if not items:
        st.info("Your cart is empty.")
        return

    total = 0
    st.divider()

    for item in items:
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
            with c1:
                try: st.image(item['image'], width=80)
                except: st.write("Img")
            with c2:
                st.subheader(item['name'])
                # تيم 5 مش بيرجع المقاس، فمش هنعرضه هنا عشان ميضربش Error
                st.caption(f"Qty: {item['quantity']}")
            with c3:
                # حساب السعر (salary * quantity)
                item_total = item['salary'] * item['quantity']
                st.write(f"**{item_total} EGP**")
                total += item_total
            with c4:
                # زر الحذف
                # تيم 5 بيرجع id السطر في السلة باسم id
                if st.button("Remove ❌", key=f"del_{item['id']}"):
                    db.remove_from_cart(item['id'])
                    st.rerun()
    
    st.divider()
    st.subheader(f"Total Amount: {total} EGP")
    
    if st.button("Proceed to Checkout 💳", type="primary", use_container_width=True):
        st.balloons()
        st.success("Redirecting to Payment Page... (Simulation)")

# === صفحة من نحن (ABOUT PAGE) ===
def render_about():
    st.title("ℹ️ About Us")
    st.markdown("### 🌟 Meet The Creators")
    
    st.write("""
    نحن مجموعة من المطورين الشغوفين، قمنا ببناء هذا المشروع لتقديم تجربة تسوق فريدة.
    """)
    st.divider()

    # --- الجزء الأول: معلومات التواصل ---
    col_contact1, col_contact2 = st.columns(2)
    
    with col_contact1:
        st.subheader("📍 Contact Info")
        st.markdown("**📞 Phone:** +20 1022826895") 
        st.markdown("**🏢 Address:** Cairo, Egypt")
        st.markdown("**📧 Email:** team3@example.com")
        
    with col_contact2:
        st.subheader("📱 Social Media")
        st.link_button("📸 Instagram", "https://www.instagram.com/rawnaq_shop28")
        st.link_button("🎵 TikTok", "https://www.tiktok.com/@rawnaq_shop_")
    
    st.divider()
    
    # --- الجزء الثاني: التيمات ---
    main_col1, main_col2 = st.columns(2)
    
    # ==========================
    # بيانات تيمك (Team 3)
    # ==========================
    # لاحظ: السطر ده لازم يكون لازق في اليمين زيه زي main_col1 اللي فوقه
    with main_col1:
        st.warning("💻 Team 3: Frontend & UI") 
        
        # بنقسم منطقة تيم 3 لعمودين (شباب وبنات)
        t3_boys, t3_girls = st.columns(2)
        
        # 1. عمود الشباب
        with t3_boys:
            st.markdown("##### 👨‍💼 الشباب")
            st.markdown("""
           1. [Ahmed helmy ]
           5. [name ]
           5. [name ]
           5. [name ]
           5. [name ]
            """)
            
        # 2. عمود البنات
        with t3_girls:
            st.markdown("##### 👩‍💼 البنات")
            st.markdown("""
           5. [Rokaya Alaa ]
           5. [name ]
           5. [name ]
           5. [name ]
           5. [name ]
            """)
  
    st.divider()
    
    # زرار الرجوع
    if st.button("⬅️ Back to Home"):
        go_to('home')
# --- 4. القائمة الجانبية (Navigation) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=100)
    st.title("Menu")
    
    if st.button("🏠 Home Page"):
        go_to('home')

    # --- التعديل الجديد هنا ---
    # 1. بنجيب الحاجات اللي في السلة عشان نعدها
    cart_items = db.view_cart(st.session_state['user_id'])
    cart_count = len(cart_items)
    
    # 2. بنعرض العدد بين قوسين جمب الاسم
    if st.button(f"🛒 My Cart ({cart_count})"):
        go_to('cart')
    
    st.divider()
    if st.button(f"log out"):
        go_to()

    # --- (جديد) زرار من نحن ---
    if st.button("ℹ️ About Us"):
        go_to('about')
    
    st.divider()    
    st.caption("Team 3 Frontend | Team 5 Database")
# --- 5. الموجه الرئيسي (Router) ---
if st.session_state['page'] == 'home':
    render_home()
elif st.session_state['page'] == 'category':
    render_category()
elif st.session_state['page'] == 'product':
    render_product()
elif st.session_state['page'] == 'cart':
    render_cart()
elif st.session_state['page'] == 'about':  # <-- (جديد) السطرين دول
    render_about()   
else:
    render_home()