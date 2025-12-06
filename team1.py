import streamlit as st
from db import register_user, login_check

# TO INSERT BACKGROUND PHOTO

import base64 

def get_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        # لو الصورة مش موجودة، ارجع نص فاضي عشان البرنامج ميكراشش
        return ""

img = get_base64("images/login_bg.jpg.jpg")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img}");
        background-size: 100% 100%;
        background-repeat: no-repeat;
        background-attachment: fixed;
        filter: brightness(0.7);             
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# TO CHANGE THE FONT

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;700&display=swap');

* {
    font-family: 'Lora', serif !important;
}
</style>
""", unsafe_allow_html=True)



# ========================
# STARTING THE ACTUAL CODE 
# ========================

st.title(":orange[*Login & Sign Up*] ")


menu = ["Login", "Sign Up"]
choice = st.radio("Choose Option", menu)


# ========================
# LOGIN FORM
# ========================
if choice == "Login":
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button(":orange[*Login*]"):
        user = login_check(username, password)
        if user:
            st.success(f"Welcome {user['username']}!")

            # -----------------------
            # ROLE CHECK
            # -----------------------
            if user['role'] == "admin":
                st.subheader(" Admin Dashboard")
                st.write("Here you can manage users, products, categories, orders, etc.")
                # ADMIN PAGE
            else:
                st.subheader("User Home Page")
                st.write("Browse products and enjoy shopping!")
                # HOME PAGE
        else:
            st.error("Invalid username or password")


# ========================
# SIGN UP FORM
# ========================
else:
    st.subheader("Create New Account")

    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")

    if st.button(":red[*Sign Up*]"):
        if register_user(username, password):
            st.success("Account created successfully! Now you can login.")
        else:
            st.error("Username already exists. Try another one.")
