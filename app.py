import base64
import os
import re
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون متمركزة في المنتصف (Centered Layout)
st.set_page_config(
    page_title="الاستعلام عن الشهادات - فرع الجيزة",
    layout="centered",
    page_icon="🏛️",
)


# دالة حساب وعرض عدد الزوار مع استثناء الآدمن
def get_and_update_visitor_count():
    count_file = "visitors.txt"

    # التحقق من وجود المعاملات في الرابط (Query Params)
    query_params = st.query_params

    # حالة الدخول كآدمن عبر الرابط (?admin=true)
    if query_params.get("admin") == "true":
        st.session_state["is_admin_mode"] = True
        st.session_state["authenticated_admin"] = True

    # إنشاء الملف إن لم يكن موجوداً
    if not os.path.exists(count_file):
        with open(count_file, "w") as f:
            f.write("0")

    # قراءة العدد الحالي
    try:
        with open(count_file, "r") as f:
            content = f.read().strip()
            count = int(content) if content.isdigit() else 0
    except Exception:
        count = 0

    # زيادة العداد فقط إذا لم يكن آدمن ولم تُحتسب الزيارة من قبل في هذه الجلسة
    is_admin = st.session_state.get("authenticated_admin", False) or st.session_state.get("is_admin_mode", False)
    
    if not is_admin and not st.session_state.get("counted_this_session", False):
        count += 1
        st.session_state["counted_this_session"] = True
        try:
            with open(count_file, "w") as f:
                f.write(str(count))
        except Exception:
            pass

    return count


# تسجيل وتنفيذ الزيارة
visitor_count = get_and_update_visitor_count()

# تفعيل تتبع Google Analytics
ga_id = "G-2V7DFZWVXJ"
ga_script = f"""
    
    
"""
components.html(ga_script, height=0, width=0)

# تطبيق التنسيق عبر CSS (تمت إزالة الـ f-string لتجنب أخطاء SyntaxError)
st.markdown(
    """
    
    """,
    unsafe_allow_html=True,
)


# دالة قراءة الشعار وتحويله إلى Base64
def get_image_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    for file in os.listdir("."):
        if file.lower().startswith("logo") and file.lower().endswith(
            (".png", ".jpg", ".jpeg")
        ):
            with open(file, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                ext = file.split(".")[-1].lower()
                return f"data:image/{ext};base64,{encoded_string}"
    return "https://cdn-icons-png.flaticon.com/512/3135/3135755.png"


# دالة قراءة صورة استلام الشهادة وتحويلها إلى Base64
def get_hand_image_base64():
    for filename in ["certificate_hand.png", "hand.png", "hand.jpg", "hand.jpeg"]:
        if os.path.exists(filename):
            with open(filename, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                ext = filename.split(".")[-1].lower()
                return f"data:image/{ext};base64,{encoded_string}"
    return "https://cdn-icons-png.flaticon.com/512/2912/2912761.png"


logo_src = get_image_base64("logo.png")
hand_src = get_hand_image_base64()

# عرض اللوجو متبوعاً باسم الفرع ثم الصورة التعبيرية بمقاس البطاقة
st.markdown(
    f"""
