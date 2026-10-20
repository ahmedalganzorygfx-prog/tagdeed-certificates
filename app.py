import base64
import os
import re
from io import BytesIO
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

    # 1. حالة التصفير عبر الرابط (?reset=true)
    if query_params.get("reset") == "true":
        st.toast("🧹 تم تصفير عداد الزيارات بنجاح!")
        return reset_visitor_count()

    # 2. حالة الدخول كآدمن (?admin=true)
    if query_params.get("admin") == "true":
        st.session_state["is_admin_mode"] = True

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

    # زيادة العداد فقط إذا لم تكن هذه الجلسة جلسة آدمن ولم تُحتسب من قبل
    is_admin = st.session_state.get("authenticated_admin", False)
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
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{ga_id}');
    </script>
"""
components.html(ga_script, height=0, width=0)

# تطبيق التنسيق عبر CSS لشاشة العرض
st.markdown(
    """
    <style>
    /* تقليص وتوسيط حاوية المحتوى الرئيسية */
    .block-container {
        max-width: 800px !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        margin: 0 auto !important;
    }

    /* إخفاء زر القلم والتعديل فقط */
    button[title="Edit"], 
    [data-testid="stHeaderEditButton"],
    button[aria-label="Edit"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* تغيير خلفية التطبيق بالكامل لتصبح داكنة */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif, Arial;
        color: #e0e0e0;
    }
    /* حاوية مخصصة لتوسيط الشعار واسم الفرع في المنتصف */
    .logo-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-top: 15px;
        margin-bottom: 10px;
        width: 100%;
        text-align: center;
    }
    .logo-container img {
        width: 180px;
        height: auto;
        display: block;
        margin: 0 auto 10px auto;
    }
    .branch-name-top {
        color: #ffffff;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 15px;
        text-align: center;
    }
    /* ضبط حجم الصورة لتتطابق تماماً مع أبعاد وحجم بطاقات المعلمين */
    .hand-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 5px;
        margin-bottom: 25px;
        width: 100%;
        box-sizing: border-box;
    }
    .hand-container img {
        width: 100%;
        max-width: 100%;
        height: auto;
        border-radius: 12px;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
        border: 1px solid #30363d;
        display: block;
        object-fit: cover;
    }
    /* تصميم رأس الصفحة بلون كحلي داكن فاخر ومتمركز */
    .header-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 22px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    /* تكبير وتنسيق العنوان الرئيسي بالترتيب الجديد */
    .header-box .main-title {
        color: #58a6ff;
        font-size: 24px !important;
        font-weight: bold !important;
        margin-bottom: 12px;
        line-height: 1.4;
    }
    .header-box p {
        color: #8b949e;
        font-size: 14px;
        margin: 0;
    }
    .highlight-red {
        color: #ffc107 !important;
        font-weight: bold;
    }
    .programs-text {
        color: #ffc107 !important;
        font-weight: bold;
    }
    .pickup-instructions {
        font-size: 16px !important;
        color: #ffc107 !important;
        font-weight: bold;
        margin-top: 8px;
        display: block;
    }
    .stAlert {
        direction: rtl;
        text-align: right;
    }

    [data-testid="stAlert"] * {
        color: #ffc107 !important;
        font-weight: bold !important;
        font-size: 17px !important;
    }

    /* زر البحث */
    .stFormSubmitButton > button {
        background-color: #21262d;
        color: white;
        width: 100%;
        border-radius: 6px;
        border: 1px solid #30363d;
        font-weight: bold;
    }
    .stFormSubmitButton > button:hover {
        background-color: #30363d;
        border-color: #8b949e;
    }


    /* زر تنزيل ملف Excel XLSX */
    [data-testid="stDownloadButton"] > button {
        background-color: #238636 !important;
        color: #ffffff !important;
        border: 1px solid #2ea043 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        width: 100% !important;
        min-height: 45px !important;
        opacity: 1 !important;
        text-align: center !important;
    }

    [data-testid="stDownloadButton"] > button:hover {
        background-color: #2ea043 !important;
        color: #ffffff !important;
        border-color: #3fb950 !important;
    }

    [data-testid="stDownloadButton"] > button p,
    [data-testid="stDownloadButton"] > button span,
    [data-testid="stDownloadButton"] > button div {
        color: #ffffff !important;
        font-weight: bold !important;
        opacity: 1 !important;
    }
    .stTextInput label {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    .stTextInput input {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
    }
    
    /* تصميم بطاقة بيانات المعلم الداكنة للشاشة */
    .teacher-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.4);
        text-align: right;
        direction: rtl;
        width: 100%;
        box-sizing: border-box;
    }
    .card-row {
        font-size: 17px;
        margin-bottom: 12px;
        color: #ffffff !important;
        font-weight: 500;
        text-align: right;
        direction: rtl;
    }
    .card-row b {
        color: #ffc107 !important;
        font-weight: bold !important;
    }

    /* ضبط شريط Expander: النص متصل بعلامة الاستفهام العربية والسهم يسار */
    [data-testid="stExpander"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        margin-top: 15px !important;
        margin-bottom: 20px !important;
        direction: rtl !important;
    }
    [data-testid="stExpander"] details {
        background-color: #161b22 !important;
        border-radius: 8px !important;
        direction: rtl !important;
    }
    [data-testid="stExpander"] summary {
        background-color: #161b22 !important;
        color: #58a6ff !important;
        direction: rtl !important;
        text-align: right !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 12px 18px !important;
        border-radius: 8px !important;
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: center !important;
    }
    [data-testid="stExpander"] summary span p {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #58a6ff !important;
        margin: 0 !important;
        direction: rtl !important;
        text-align: right !important;
        unicode-bidi: isolate;
    }
    [data-testid="stExpander"] summary svg {
        fill: #58a6ff !important;
        margin-right: auto !important;
        margin-left: 0 !important;
    }

    .faq-answer-box {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-right: 5px solid #58a6ff;
        padding: 18px;
        border-radius: 8px;
        margin-top: 8px;
        margin-bottom: 15px;
        line-height: 1.9;
        font-size: 17px;
        color: #e0e0e0;
        direction: rtl !important;
        text-align: right !important;
    }
    .faq-highlight-yellow {
        color: #ffc107 !important;
        font-weight: bold !important;
    }
    
    /* تنسيق صناديق الحالات المخصصة */
    .status-red {
        background-color: rgba(255, 193, 7, 0.15);
        color: #ffc107;
        padding: 14px;
        border-radius: 8px;
        border-right: 5px solid #ffc107;
        margin-top: 10px;
        margin-bottom: 15px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        direction: rtl;
        border-top: 1px solid rgba(255, 193, 7, 0.2);
        border-bottom: 1px solid rgba(255, 193, 7, 0.2);
        border-left: 1px solid rgba(255, 193, 7, 0.2);
    }
    .status-green {
        background-color: rgba(46, 160, 67, 0.15);
        color: #3fb950;
        padding: 16px;
        border-radius: 8px;
        border-right: 5px solid #2ea043;
        margin-top: 10px;
        margin-bottom: 15px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        direction: rtl;
        border-top: 1px solid rgba(46, 160, 67, 0.2);
        border-bottom: 1px solid rgba(46, 160, 67, 0.2);
        border-left: 1px solid rgba(46, 160, 67, 0.2);
    }
    .status-blue {
        background-color: rgba(56, 139, 253, 0.15);
        color: #58a6ff;
        padding: 14px;
        border-radius: 8px;
        border-right: 5px solid #388bfd;
        margin-top: 10px;
        margin-bottom: 15px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        direction: rtl;
        border-top: 1px solid rgba(56, 139, 253, 0.2);
        border-bottom: 1px solid rgba(56, 139, 253, 0.2);
        border-left: 1px solid rgba(56, 139, 253, 0.2);
    }

    @keyframes colorPulseGlow {
        0% { color: #3fb950; transform: scale(1); }
        50% { color: #ffc107; transform: scale(1.06); }
        100% { color: #3fb950; transform: scale(1); }
    }
    .pulse-text {
        display: inline-block;
        animation: colorPulseGlow 1.2s infinite ease-in-out;
        font-size: 20px !important;
        font-weight: 900 !important;
        margin-bottom: 5px;
    }

    .action-btn-container {
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .share-whatsapp-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 18px;
        background-color: #238636;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        text-decoration: none;
        font-size: 14px;
        transition: background-color 0.2s;
    }
    .share-whatsapp-btn:hover { background-color: #2ea043; }

    /* صندوق مواعيد استلام الشهادات */
    .working-hours-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-right: 5px solid #58a6ff;
        padding: 18px 22px;
        border-radius: 10px;
        margin-top: 25px;
        margin-bottom: 20px;
        text-align: right;
        color: #ffffff;
        font-size: 16px;
        line-height: 1.8;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .working-hours-title {
        color: #58a6ff;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .working-hours-highlight {
        color: #ffc107 !important;
        font-weight: bold;
        font-size: 17px;
    }

    .whatsapp-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .whatsapp-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        background-color: #25d366;
        color: white !important;
        font-weight: bold;
        border-radius: 20px;
        text-decoration: none;
        font-size: 14px;
    }
    .custom-footer {
        margin-top: 40px;
        padding: 20px;
        text-align: center;
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        color: #8b949e;
        font-size: 14px;
        direction: rtl;
        line-height: 1.8;
    }
    .map-container {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #30363d;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    .map-btn {
        display: inline-block;
        margin-top: 10px;
        padding: 8px 18px;
        background-color: #238636;
        color: white !important;
        font-weight: bold;
        border-radius: 6px;
        text-decoration: none;
    }
    .visitor-badge {
        display: inline-block;
        margin-top: 15px;
        padding: 6px 18px;
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-radius: 20px;
        color: #8b949e;
        font-size: 13px;
        font-weight: bold;
    }
    .director-badge {
        display: inline-block;
        margin-top: 12px;
        padding: 8px 20px;
        background: linear-gradient(135deg, #21262d 0%, #161b22 100%);
        border: 1px solid #30363d;
        border-right: 4px solid #ffc107;
        border-radius: 8px;
        color: #e0e0e0;
        font-size: 14px;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# دالة قراءة الشعار وتحويله إلى Base64
def get_image_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    for file in
