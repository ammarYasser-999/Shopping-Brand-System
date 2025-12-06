import streamlit as st
import team3  # ده الملف اللي إنت غيرت اسمه
# import team1  # شيل العلامة دي لما تحط ملف تيم 1 وتتأكد من اسمه

# 1. تجهيز الـ Session State (عشان المتصفح يفتكر إحنا في أي صفحة)
if 'page' not in st.session_state:
    st.session_state['page'] = 'home' # أو خليها 'login' لو عايز تبدأ بتيم 1

# 2. القائمة الجانبية (اختياري لو عايز تحكم خارجي)
st.sidebar.title("التنقل الرئيسي")
page = st.sidebar.radio("اختر الصفحة:", ["Home (Team 3)", "Login (Team 1)"])

# 3. توجيه الصفحات
if page == "Home (Team 3)":
    # هنا بننادي على الشغل اللي جوا ملف تيم 3
    # لازم تتأكد إن جوا ملف team3.py فيه دالة اسمها render_home()
    # لو مفيش، ومكتوب الكود سايح، قولي عشان أقولك تظبطه ازاي
    try:
        team3.render_home() 
    except AttributeError:
        st.error("مش لاقي دالة render_home في ملف team3.py")

elif page == "Login (Team 1)":
    st.write("هنا هيظهر شغل تيم 1 لما تجهزه")
    # team1.show_login()