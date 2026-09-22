import base64
import os
import pandas as pd
import streamlit as st

# إعداد الصفحة لتكون عريضة ودعم اللغة العربية من اليمين لليسار (RTL)
st.set_page_config(
    page_title="الاستعلام عن تجديد الشهادة - فرع الجيزة",
    layout="wide",
    page_icon="🏛️",
)

# تطبيق التنسيق عبر CSS
st.markdown(
    """
    <style>
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
    /* حاوية مخصصة لتوسيط الشعار تماماً في المنتصف */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 15px;
        margin-bottom: 20px;
        width: 100%;
        text-align: center;
    }
    .logo-container img {
        width: 200px;
        height: auto;
        display: block;
        margin: 0 auto;
    }
    /* تصميم رأس الصفحة بلون كحلي داكن فاخر ومتمركز */
    .header-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    .header-box h2 {
        color: #ffffff;
        font-weight: bold;
        margin-bottom: 12px;
    }
    /* تكبير وتنسيق العنوان الرئيسي */
    .header-box .main-title {
        color: #58a6ff;
        font-size: 26px !important;
        font-weight: bold !important;
        margin-bottom: 12px;
        line-height: 1.4;
    }
    .header-box p {
        color: #8b949e;
        font-size: 15px;
        margin: 0;
    }
    /* تنسيق النص الملون والمميز داخل العنوان والبرامج */
    .highlight-yellow {
        color: #ffcc00 !important;
        font-weight: bold;
    }
    .programs-text {
        color: #ffcc00 !important;
        font-weight: bold;
    }
    /* تنسيق مميز بخط أكبر ولون لافت لتعليمات الاستلام */
    .pickup-instructions {
        font-size: 17px !important;
        color: #ffe566 !important;
        font-weight: bold;
        margin-top: 8px;
        display: block;
    }
    .stAlert {
        direction: rtl;
        text-align: right;
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
    /* جعل تسمية خانة الإدخال باللون الأبيض */
    .stTextInput label {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    /* تصميم خانة الإدخال لتتناغم مع التصميم الداكن */
    .stTextInput input {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
    }
    /* تصميم بطاقة بيانات المعلم الداكنة */
    .teacher-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.4);
        text-align: right;
        direction: rtl;
    }
    .card-title {
        color: #58a6ff;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
        border-bottom: 1px solid #30363d;
        padding-bottom: 8px;
        text-align: right;
        direction: rtl;
    }
    .card-row {
        font-size: 16px;
        margin-bottom: 10px;
        color: #c9d1d9;
        text-align: right;
        direction: rtl;
    }
    /* تنسيق صناديق الحالات المخصصة */
    .status-red {
        background-color: rgba(248, 81, 73, 0.15);
        color: #ff7b72;
        padding: 14px;
        border-radius: 8px;
        border-right: 5px solid #f85149;
        margin-top: 15px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        direction: rtl;
        border-top: 1px solid rgba(248, 81, 73, 0.2);
        border-bottom: 1px solid rgba(248, 81, 73, 0.2);
        border-left: 1px solid rgba(248, 81, 73, 0.2);
    }
    .status-green {
        background-color: rgba(46, 160, 67, 0.15);
        color: #3fb950;
        padding: 16px;
        border-radius: 8px;
        border-right: 5px solid #2ea043;
        margin-top: 15px;
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
        margin-top: 15px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        direction: rtl;
        border-top: 1px solid rgba(56, 139, 253, 0.2);
        border-bottom: 1px solid rgba(56, 139, 253, 0.2);
        border-left: 1px solid rgba(56, 139, 253, 0.2);
    }

    /* تأثير الوميض الديناميكي مع تغيير اللون وتكبير الخط */
    @keyframes colorPulseGlow {
        0% {
            color: #3fb950;
            transform: scale(1);
            text-shadow: 0 0 4px rgba(63, 185, 80, 0.4);
        }
        50% {
            color: #ffe566;
            transform: scale(1.08);
            text-shadow: 0 0 12px rgba(255, 229, 102, 0.8);
        }
        100% {
            color: #3fb950;
            transform: scale(1);
            text-shadow: 0 0 4px rgba(63, 185, 80, 0.4);
        }
    }
    .pulse-text {
        display: inline-block;
        animation: colorPulseGlow 1.2s infinite ease-in-out;
        font-size: 22px !important;
        font-weight: 900 !important;
        margin-bottom: 5px;
    }

    /* تنسيق أزرار الواتساب للتواصل والدعم الفني */
    .whatsapp-container {
        display: flex;
        justify-content: center;
        gap: 12px;
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
        transition: background-color 0.2s;
    }
    .whatsapp-btn:hover {
        background-color: #128c7e;
    }
    /* تصميم تذييل الصفحة الفاخر (Footer) */
    .custom-footer {
        margin-top: 50px;
        padding: 25px 20px;
        text-align: center;
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        color: #8b949e;
        font-size: 15px;
        direction: rtl;
        line-height: 1.8;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    .map-container {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #30363d;
        box-shadow: 0 4px 15px rgba(0,0,0,0.6);
        margin-top: 15px;
        margin-bottom: 25px;
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
        transition: background-color 0.2s;
    }
    .map-btn:hover {
        background-color: #2ea043;
    }
    /* تصميم تبويب توقيع الإدارة والمدير */
    .director-badge {
        display: inline-block;
        margin-top: 15px;
        padding: 10px 24px;
        background: linear-gradient(135deg, #21262d 0%, #161b22 100%);
        border: 1px solid #30363d;
        border-right: 4px solid #ffcc00;
        border-radius: 8px;
        color: #e0e0e0;
        font-size: 15px;
        font-weight: bold;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .director-badge b {
        color: #ffcc00;
        font-size: 16px;
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
    for file in os.listdir("."):
        if file.lower().startswith("logo") and file.lower().endswith(
            (".png", ".jpg", ".jpeg")
        ):
            with open(file, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                ext = file.split(".")[-1].lower()
                return f"data:image/{ext};base64,{encoded_string}"
    return "https://cdn-icons-png.flaticon.com/512/3135/3135755.png"


logo_src = get_image_base64("logo.png")

# عرض اللوجو متمركزاً في المنتصف
st.markdown(
    f"""
    <div class="logo-container">
        <img src="{logo_src}" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True,
)

# صندوق العنوان الرئيسي
st.markdown(
    """
    <div class="header-box">
        <h2>🏛️ الأكاديمية المهنية للمعلمين - فرع الجيزة</h2>
        <div class="main-title">الاستعلام عن <span class="highlight-yellow">(تجديد - بدل فاقد)</span> شهادة القيادة والإشراف</div>
        <p><b>البرامج التدريبية :</b> <span class="programs-text">مدير ووكيل إدارة تعليمية &nbsp;|&nbsp; مدير ووكيل إدارة مدرسية &nbsp;|&nbsp; أساسيات التوجيه الفني</span></p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")


# دالة قراءة البيانات
@st.cache_data(ttl=600)
def load_data(file_path):
    if not os.path.exists(file_path):
        return None
    df = pd.read_excel(file_path, dtype=str)
    df.columns = df.columns.astype(str).str.strip()
    return df


excel_file = "certificates.xlsx"
df = load_data(excel_file)

if df is not None:
    id_column = None
    for col in df.columns:
        if any(keyword in col for keyword in ["قومي", "الرقم", "ID"]):
            id_column = col
            break
    if id_column is None:
        id_column = df.columns[0]

    status_column = None
    for col in df.columns:
        if any(keyword in col for keyword in ["حالة", "الشهادة"]):
            status_column = col
            break

    st.markdown(
        '<div style="text-align: right; direction: rtl; font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #c9d1d9;">💡 أدخل الرقم القومي الخاص بك (14 رقماً) ثم اضغط على زر بحث:</div>',
        unsafe_allow_html=True,
    )

    with st.form(key="search_form"):
        search_query = st.text_input("الرقم القومي:", max_chars=14).strip()
        submit_button = st.form_submit_button(label="🔍 بحث")

    if submit_button:
        if search_query:
            df[id_column] = (
                df[id_column]
                .astype(str)
                .str.replace(r"\.0$", "", regex=True)
                .str.strip()
            )
            result = df[df[id_column] == search_query]

            if result.empty:
                result = df[df[id_column].str.contains(search_query, na=False)]

            if not result.empty:
                st.success("🎉 تم العثور على بيانات الشهادة بنجاح:")

                for idx, row in result.iterrows():
                    name_val = "غير متوفر"
                    for c in df.columns:
                        if any(
                            k in c for k in ["اسم", "الاسم", "المعلم", "السيد"]
                        ) and not any(
                            k in c for k in ["قومي", "إدارة", "الادارة"]
                        ):
                            name_val = str(row[c]) if pd.notna(row[c]) else "غير متوفر"
                            break

                    admin_val = "غير متوفر"
                    for c in df.columns:
                        if "الادارة" in c or "الإدارة" in c:
                            admin_val = str(row[c]) if pd.notna(row[c]) else "غير متوفر"
                            break

                    prog_val = "غير متوفر"
                    for c in df.columns:
                        if any(k in c for k in ["البرنامج", "الترقي", "التدريب"]):
                            prog_val = str(row[c]) if pd.notna(row[c]) else "غير متوفر"
                            break

                    serial_val = "غير متوفر"
                    for c in df.columns:
                        if "مسلسل" in c or c.strip() == "م":
                            serial_val = str(row[c]) if pd.notna(row[c]) else "غير متوفر"
                            break

                    card_code = f"""
                    <div class="teacher-card">
                        <div class="card-title">👤 بيانات المعلم</div>
                        <div class="card-row"><b>رقم المسلسل:</b> {serial_val}</div>
                        <div class="card-row"><b>اسم المعلم:</b> {name_val}</div>
                        <div class="card-row"><b>الرقم القومي:</b> {row[id_column]}</div>
                        <div class="card-row"><b>الإدارة التعليمية:</b> {admin_val}</div>
                        <div class="card-row"><b>البرنامج التدريبي:</b> {prog_val}</div>
                    </div>
                    """
                    st.markdown(card_code, unsafe_allow_html=True)

                    if status_column and pd.notna(row[status_column]):
                        status_val = str(row[status_column]).strip()
                        if "لم تصل" in status_val:
                            st.markdown(
                                """
                                <div class="status-red">
                                    🔴 لم تصل إلى الفرع حتى الآن<br>
                                    <span style="font-weight: normal; font-size: 14px; color: #8b949e;">يرجى الاستعلام في وقت لاحق.</span>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        elif "موجودة" in status_val:
                            st.markdown(
                                """
                                <div class="status-green">
                                    <span class="pulse-text">🟢 موجودة بالفرع</span><br>
                                    <span class="pickup-instructions">📌 يرجى التوجه لمقر الفرع لاستلامها مع احضار صحيفة أحوال إلكترونية حديثة معتمدة + صورة البطاقة.</span>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        elif "تسليم" in status_val:
                            st.markdown(
                                """
                                <div class="status-blue">
                                    🔵 تم تسليم الشهادة للمعلم
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f'<div class="status-blue">حالة الشهادة: {status_val}</div>',
                                unsafe_allow_html=True,
                            )
            else:
                st.error(
                    "❌ عذراً، لم يتم العثور على بيانات بهذا الرقم القومي. تأكد من صحة الرقم المُدخل."
                )
        else:
            st.warning("⚠️ برجاء كتابة الرقم القومي أولاً قبل الضغط على بحث.")
else:
    st.warning(
        "⚠️ جاري تجهيز قاعدة البيانات أو أن ملف الكشف غير متوفر حالياً. برجاء التأكد من رفع ملف (certificates.xlsx) في مجلد المشروع على GitHub."
    )

# تذييل الصفحة المطور والمجمل بالكامل
st.markdown(
    """
    <div class="custom-footer">
        💬 <b>أرقام الدعم الفني للتواصل عبر واتس آب:</b>
        <div class="whatsapp-container">
            <a href="https://wa.me/201069996245" target="_blank" class="whatsapp-btn">🟢 01069996245</a>
            <a href="https://wa.me/201120807631" target="_blank" class="whatsapp-btn">🟢 01120807631</a>
            <a href="https://wa.me/201201109892" target="_blank" class="whatsapp-btn">🟢 01201109892</a>
        </div>
        <br>
        📍 <b>عنوان الفرع:</b> الأكاديمية المهنية للمعلمين - فرع الجيزة<br>
        🏢 ش المحطة - إمبابة (بجوار مدرسة باحثة البادية التجارية بنات)<br>
        <a href="https://maps.app.goo.gl/akdNyovrEbWLJmBu9" target="_blank" class="map-btn">
            🗺️ فتح الموقع والتوجيه المباشر في تطبيق Google Maps
        </a>
        <div class="map-container">
            <iframe 
                src="https://maps.google.com/maps?q=30.06776,31.20915&hl=ar&z=17&output=embed" 
                width="100%" 
                height="400" 
                style="border:0;" 
                allowfullscreen="" 
                loading="lazy" 
                referrerpolicy="no-referrer-when-downgrade">
            </iframe>
        </div>
        <div class="director-badge">
            👔 تصميم وتنفيذ <b>أحمد الجنزوري</b> - مدير الفرع
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
