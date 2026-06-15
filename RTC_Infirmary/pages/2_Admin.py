import streamlit as st
import pandas as pd
import os
import base64
import plotly.express as px
import requests
from datetime import datetime

# 1. ตั้งค่าหน้าจอ (ต้องอยู่บรรทัดแรกสุดเสมอ)
st.set_page_config(page_title="Admin Control", page_icon="🏥", layout="wide")

# ==========================================
# ระบบการแจ้งเตือนส่วนกลาง (Telegram Notification)
# ==========================================
TELEGRAM_TOKEN = "8917128684:AAFK0b951bn1vvUzLdUKjx7xV3NEndYTMts"
TELEGRAM_CHAT_ID = "8578773039"

def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except:
        pass

# ==========================================
# ฟังก์ชันจัดการภาพพื้นหลัง + ปรับแต่งสไตล์ (เอาเส้นขอบและกรอบออก)
# ==========================================
def set_perfect_background():
    possible_paths = [
        "RTC_Infirmary/images/bg.jpg",  
        "images/bg.jpg",                
        "bg.jpg"                        
    ]
    
    encoded_string = ""
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode()
                    break 
            except:
                pass
                
    if encoded_string:
        bg_css = f"""
        <style>
        /* แถบคาดด้านบนสุด (Header Bar) เป็นสีน้ำเงินกรมท่า ไม่มีขอบล่าง */
        header[data-testid="stHeader"] {{
            background-color: #001f3f !important;
            border-bottom: none !important;
        }}
        header[data-testid="stHeader"] button, header[data-testid="stHeader"] a, header[data-testid="stHeader"] span {{
            color: #ffffff !important;
        }}
        
        /* สไตล์พื้นหลังหลัก */
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                              url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        /* ตารางยึดพื้นหลังสีขาวล้วน ไม่มีเส้นขอบกรอบ */
        div[data-testid="stDataFrame"] {{
            background-color: #ffffff !important;
            padding: 10px;
            border-radius: 8px;
            border: none !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}
        
        /* กล่อง Selectbox (Dropdown) ไม่มีเส้นกรอบขอบ */
        div[data-baseweb="select"] {{
            background-color: #ffffff !important;
            border: none !important;
            border-radius: 6px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        }}
        div[data-baseweb="select"] div {{
            color: #1e293b !important;
            background-color: #ffffff !important;
            border: none !important;
        }}
        div[data-baseweb="select"] span {{
            color: #1e293b !important;
        }}
        li[role="option"] {{
            background-color: #ffffff !important;
            color: #1e293b !important;
        }}
        
        /* ปรับช่องกรอก Input ทั้งหมดให้ไม่มีเส้นกรอบขอบ */
        div[data-baseweb="input"] {{
            background-color: #ffffff !important;
            border: none !important;
            border-radius: 6px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        }}
        div[data-baseweb="input"] input {{
            color: #1e293b !important;
            background-color: #ffffff !important;
            border: none !important;
        }}
        div[data-baseweb="input"] input::placeholder {{
            color: #94a3b8 !important;
        }}
        
        /* กล่องยุบขยาย (Expander) ไม่มีเส้นกรอบขอบ */
        div[data-testid="stExpander"] {{
            background-color: #f1f5f9 !important;
            border: none !important;
            border-radius: 8px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        }}
        div[data-testid="stExpander"] details summary {{
            background-color: #f1f5f9 !important;
            color: #001f3f !important;
            border: none !important;
        }}
        div[data-testid="stExpander"] details summary p, 
        div[data-testid="stExpander"] details summary span,
        div[data-testid="stExpander"] details summary div {{
            color: #001f3f !important;
            font-weight: bold !important;
            font-size: 16px !important;
        }}
        
        [data-testid="stMainBlockContainer"] h1, 
        [data-testid="stMainBlockContainer"] h2, 
        [data-testid="stMainBlockContainer"] h3, 
        [data-testid="stMainBlockContainer"] h4, 
        [data-testid="stMainBlockContainer"] h5, 
        [data-testid="stMainBlockContainer"] h6, 
        [data-testid="stMainBlockContainer"] label, 
        [data-testid="stMainBlockContainer"] p,
        [data-testid="stMainBlockContainer"] span {{
            color: #2d3748 !important;
        }}
        
        .responsive-h1 {{
            text-align: center; 
            color: #001f3f !important;
            font-family: "Sarabun", sans-serif;
            font-weight: bold; 
            margin-bottom: 0;
            font-size: calc(1.5rem + 1.2vw) !important;
            line-height: 1.3 !important;
            word-wrap: break-word;
        }}
        .responsive-h4 {{
            text-align: center; 
            color: #4a5568 !important; 
            font-family: "Sarabun", sans-serif;
            margin-top: 5px; 
            margin-bottom: 20px;
            font-size: calc(0.9rem + 0.3vw) !important;
            line-height: 1.4 !important;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: rgba(248, 249, 250, 0.95) !important;
            border-right: none !important;
        }}
        [data-testid="stSidebarNavigation"] ul li div span, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebarNavigation"] a span {{
            color: #2d3748 !important; font-weight: 600 !important; font-size: 16px !important;
        }}
        
        /* ปุ่มทั่วไป ไม่มีขอบ */
        div.stButton > button, button[data-testid="baseButton-secondary"], button[data-testid="baseButton-primary"] {{
            background-color: #001f3f !important;
            border: none !important;
            border-radius: 6px !important;
            transition: 0.2s all ease !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
        }}
        div.stButton > button p,
        div.stButton > button span,
        div.stButton > button div,
        button[data-testid="baseButton-secondary"] p,
        button[data-testid="baseButton-secondary"] span,
        button[data-testid="baseButton-primary"] p,
        button[data-testid="baseButton-primary"] span {{
            color: #ffffff !important;
            font-weight: bold !important;
            font-size: 16px !important;
        }}
        div.stButton > button:hover, button[data-testid="baseButton-secondary"]:hover, button[data-testid="baseButton-primary"]:hover {{
            background-color: #001122 !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
        }}

        /* ปุ่มดาวน์โหลด ไม่มีขอบ */
        div.stDownloadButton > button {{
            background-color: #28a745 !important;
            border: none !important;
            border-radius: 6px !important;
            width: 100% !important;
            min-height: 45px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
            transition: 0.2s all !important;
        }}
        div.stDownloadButton > button p {{
            color: #ffffff !important;
            font-weight: bold !important;
            font-size: 16px !important;
        }}
        div.stDownloadButton > button:hover {{
            background-color: #218838 !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
        }}

        input::-ms-reveal, input::-ms-clear {{ display: none !important; }}
        .stTextInput div[data-baseweb="input"] button + div {{ display: none !important; visibility: hidden !important; }}
        
        [data-testid="stSidebarNavigation"] ul li:first-child div span, [data-testid="stSidebarNavigation"] ul li:first-child a span {{
            visibility: hidden; position: relative;
        }}
        [data-testid="stSidebarNavigation"] ul li:first-child div span::after, [data-testid="stSidebarNavigation"] ul li:first-child a span::after {{
            content: "หน้าหลัก"; visibility: visible; position: absolute; left: 0; top: 0; white-space: nowrap; color: #2d3748 !important; 
        }}

        /* แถบการ์ดสถิติตัวเลข ไม่มีขอบ */
        [data-testid="stMetricValue"] {{
            font-size: 28px !important;
            font-weight: bold !important;
            color: #001f3f !important;
        }}
        [data-testid="stMetricContainer"] {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            padding: 15px 25px !important;
            border-radius: 10px !important;
            border: none !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        }}

        /* แถบ Tab */
        button[data-baseweb="tab"] {{
            font-size: 16px !important;
            font-weight: 600 !important;
            color: #4a5568 !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: #001f3f !important;
            border-bottom-color: #001f3f !important;
        }}

        @media (max-width: 768px) {{
            [data-testid="stMainBlockContainer"] p, 
            [data-testid="stMainBlockContainer"] label, 
            [data-testid="stMainBlockContainer"] span {{
                font-size: 14px !important;
            }}
            .stMarkdown h3 {{
                font-size: 18px !important;
            }}
        }}
        </style>
        """
        st.markdown(bg_css, unsafe_allow_html=True)

set_perfect_background()

# 🛠️ ปรับแก้กล่องสีน้ำเงินแถบแจ้งเตือน: เอา border (กรอบ) และ border-left (ขอบซ้าย) ออกทั้งหมด
def custom_blue_box(text):
    html_code = f"""
    <div style="background-color: #e6f2ff; padding: 12px 20px; border-radius: 6px; margin-bottom: 15px;">
        <span style="color: #001f3f; font-weight: 500; font-size: 15px;">{text}</span>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# 🛠️ ปรับแก้กล่องสีแดงแถบแจ้งเตือน: เอา border (กรอบ) และ border-left (ขอบซ้าย) ออกทั้งหมดเช่นกัน
def custom_red_box(text):
    html_code = f"""
    <div style="background-color: #f8d7da; padding: 12px 20px; border-radius: 6px; margin-bottom: 15px;">
        <span style="color: #721c24; font-weight: bold; font-size: 15px;">{text}</span>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# ==========================================
# หัวข้อหน้าเว็บแบบ Responsive
# ==========================================
st.markdown("<h1 class='responsive-h1'>แผงควบคุมสำหรับเจ้าหน้าที่ / อาจารย์ห้องพยาบาล</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='responsive-h4'>วิทยาลัยเทคนิคระยอง (Rayong Technical College)</h4>", unsafe_allow_html=True)
st.write("---")

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if not st.session_state.admin_logged_in:
    col_l, col_m, col_r = st.columns([1, 1.3, 1])
    with col_m:
        st.markdown("<h3 style='text-align: center; color: #2d3748;'>เข้าสู่ระบบเจ้าหน้าที่</h3>", unsafe_allow_html=True)
        username = st.text_input("ชื่อผู้ใช้งาน (Username):", placeholder="พิมพ์ชื่อผู้ใช้งาน เช่น admin / ชื่ออาจารย์")
        password = st.text_input("รหัสผ่าน (Password):", type="password", placeholder="กรอกรหัสผ่าน 4 หลัก")
        
        st.markdown("<div style='padding-top: 10px;'></div>", unsafe_allow_html=True)
        login_btn = st.button("เข้าสู่ระบบ (Login)", use_container_width=True)
        
        if login_btn:
            if not username.strip():
                st.error("กรุณากรอกชื่อผู้ใช้งาน (Username) ด้วยครับ")
            elif password == "1234":
                st.session_state.admin_logged_in = True
                st.session_state.current_user = username.strip()
                st.rerun()
            else:
                st.error("รหัสผ่านไม่ถูกต้อง! ไม่มีสิทธิ์เข้าถึงข้อมูลส่วนนี้")

if st.session_state.admin_logged_in:
    col_title, col_logout = st.columns([5, 1.5])
    with col_title:
        st.success(f"Status: เจ้าหน้าที่ [{st.session_state.current_user}] เข้าสู่ระบบสำเร็จ")
    with col_logout:
        st.markdown("""
            <style>
            div.element-container:has(button:contains("ออกจากระบบ")) button {
                background-color: #dc3545 !important;
                border: none !important;
            }
            </style>
        """, unsafe_allow_html=True)
        if st.button("ออกจากระบบ", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.session_state.current_user = ""
            st.rerun()

    DB_FILE = "infirmary_records.csv"
    STOCK_FILE = "medicine_stock.csv"
    
    if not os.path.exists(STOCK_FILE):
        pd.DataFrame([
            {"ชื่อยา/เวชภัณฑ์": "พาราเซตามอล (500mg)", "คงเหลือ": 300, "หน่วย": "เม็ด"},
            {"ชื่อยา/เวชภัณฑ์": "ยาแก้แพ้ (คลอเฟน)", "คงเหลือ": 150, "หน่วย": "เม็ด"},
            {"ชื่อยา/เวชภัณฑ์": "ยาธาตุน้ำแดง", "คงเหลือ": 15, "หน่วย": "ขวด"},
            {"ชื่อยา/เวชภัณฑ์": "เบตาดีนทำแผล", "คงเหลือ": 8, "หน่วย": "ขวด"}
        ]).to_csv(STOCK_FILE, index=False, encoding="utf-8-sig")

    def load_data():
        if os.path.exists(DB_FILE): 
            load_df = pd.read_csv(DB_FILE)
            EXCLUDE_MEDICINES = ["ยาขับเลือด", "ยาสตรี", "ยานอนหลับ"]
            has_changed = False
            for med in EXCLUDE_MEDICINES:
                if "การจ่ายยา/หมายเหตุ" in load_df.columns:
                    before_count = len(load_df)
                    load_df = load_df[~load_df["การจ่ายยา/หมายเหตุ"].astype(str).str.contains(med, na=False)]
                    if len(load_df) != before_count:
                        has_changed = True
            if has_changed:
                load_df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")
            bad_cols = [c for c in load_df.columns if "暗" in c or c == "Unnamed: 0"]
            bad_cols += [c for c in load_df.columns if "สถานะการรักษา." in c]
            if bad_cols:
                load_df = load_df.drop(columns=bad_cols)
            if "สถานะการรักษา" in load_df.columns:
                load_df["Sample_Status"] = load_df["สถานะการรักษา"].fillna("กำลังรอเจ้าหน้าที่คัดกรอง")
                load_df["สถานะการรักษา"] = load_df["สถานะการรักษา"].replace("รอดำเนินการคัดกรอง", "กำลังรอเจ้าหน้าที่คัดกรอง")
            else:
                load_df["Keep_Status"] = "กำลังรอเจ้าหน้าที่คัดกรอง"
            if "อาจารย์ผู้บันทึก" not in load_df.columns:
                load_df["อาจารย์ผู้บันทึก"] = "-"
            standard_cols = ["วันที่-เวลา", "รหัสนักศึกษา", "ชื่อ-นามสกุล", "โรคประจำตัว", "แผนกวิชา", "อาการเบื้องต้น", "สถานะการรักษา", "การจ่ายยา/หมายเหตุ", "อาจารย์ผู้บันทึก"]
            for col in standard_cols:
                if col not in load_df.columns:
                    load_df[col] = "-"
            return load_df[standard_cols]
        return pd.DataFrame(columns=["วันที่-เวลา", "รหัสนักศึกษา", "ชื่อ-นามสกุล", "โรคประจำตัว", "แผนกวิชา", "อาการเบื้องต้น", "สถานะการรักษา", "การจ่ายยา/หมายเหตุ", "อาจารย์ผู้บันทึก"])

    def save_data(df):
        df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")

    df = load_data()
    df_stock = pd.read_csv(STOCK_FILE)
    df_stock = df_stock[~df_stock["ชื่อยา/เวชภัณฑ์"].isin(["ยาขับเลือด", "ยาสตรี", "ยานอนหลับ"])]
    
    if not df.empty:
        st.markdown("### รายงานสถิติภาพรวม")
        m1, m2 = st.columns(2)
        with m1:
            st.metric("จำนวนนักเรียนที่ใช้บริการรวม", f"{len(df)} เคส")
        with m2:
            waiting_count = len(df[df['สถานะการรักษา'].astype(str).str.contains('รอ|กำลัง', na=False)])
            st.metric("เคสที่ยังค้างอยู่ในระบบ (รอตรวจ)", f"{waiting_count} เคส")
        
        st.markdown("<div style='padding-top: 15px;'></div>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["สถิติแยกตามแผนกวิชา", "แนวโน้มผู้ป่วยรายเดือน"])
        with tab1:
            dept_counts = df["แผนกวิชา"].value_counts().reset_index()
            dept_counts.columns = ["แผนกวิชา", "จำนวนนักเรียน (คน)"]
            fig_bar = px.bar(dept_counts, x="แผนกวิชา", y="จำนวนนักเรียน (คน)", color="แผนกวิชา", color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_bar.update_layout(yaxis=dict(tickformat='d'))
            st.plotly_chart(fig_bar, use_container_width=True)
        with tab2:
            try:
                df_time = df.copy()
                df_time["datetime"] = pd.to_datetime(df_time["วันที่-เวลา"], errors='coerce')
                df_time["เดือน"] = df_time["datetime"].dt.strftime('%Y-%m (เดือน %m)')
                monthly_counts = df_time["เดือน"].value_counts().reset_index()
                monthly_counts.columns = ["เดือน", "จำนวนผู้ใช้บริการ (ครั้ง)"]
                monthly_counts = monthly_counts.sort_values(by="เดือน")
                fig_line = px.line(monthly_counts, x="เดือน", y="จำนวนผู้ใช้บริการ (ครั้ง)", markers=True)
                fig_line.update_traces(line=dict(width=3, color='#001f3f'))
                fig_line.update_layout(yaxis=dict(tickformat='d'))
                st.plotly_chart(fig_line, use_container_width=True)
            except:
                custom_blue_box("ข้อมูลวันที่ยังไม่สมบูรณ์สำหรับการพล็อตเส้นเวลา")
        st.write("---")

    st.markdown("### ค้นหาและตรวจสอบประวัติการรับยาย้อนหลังรายบุคคล")
    search_col1, search_col2 = st.columns([1.5, 2])
    with search_col1:
        search_id = st.text_input("กรอกรหัสนักศึกษา 11 หลักเพื่อเช็กสถิติการรับยา:", placeholder="พิมพ์รหัส เช่น 67219010049")
    if search_id.strip():
        student_history = df[df["รหัสนักศึกษา"].astype(str) == search_id.strip()]
        if not student_history.empty:
            total_records = len(student_history)
            found_user_name = student_history.iloc[-1]["ชื่อ-นามสกุล"]
            with search_col2:
                if total_records >= 4:
                    custom_blue_box("⚠️ คำเตือน: นักศึกษาคนนี้มารับบริการค่อนข้างบ่อยผิดปกติ")
                st.metric(label="จำนวนครั้งที่เข้าใช้บริการห้องพยาบาลรวม", value=f"{total_records} ครั้ง")
            st.markdown(f"##### ตารางประวัติของ: <span style='color:#001f3f; font-weight:bold;'>{found_user_name}</span> [รหัส: {search_id}]", unsafe_allow_html=True)
            st.dataframe(student_history[["วันที่-เวลา", "โรคประจำตัว", "อาการเบื้องต้น", "สถานะการรักษา", "การจ่ายยา/หมายเหตุ", "อาจารย์ผู้บันทึก"]], use_container_width=True)
        else:
            with search_col2:
                custom_blue_box("ℹ️ ไม่พบประวัติเก่าในระบบ (นักศึกษาคนนี้เพิ่งเคยมาเป็นครั้งแรก)")
    st.write("---")

    if df.empty:
        custom_blue_box("ℹ️ ปัจจุบันยังไม่มีข้อมูลนักเรียนมาลงชื่อเข้ารับบริการ")
    else:
        st.subheader("รายชื่อนักเรียนคิวเข้ารับบริการทั้งหมด")
        st.dataframe(df, use_container_width=True)
        
        with st.expander("แผงควบคุมเจ้าหน้าที่: ลบประวัตินักเรียนออกจากฐานข้อมูล"):
            st.markdown("<p style='color:#dc3545;'>อาจารย์สามารถเลือกลบรายชื่อนักเรียนที่คีย์ซ้ำ พิมพ์ข้อมูลผิด หรือต้องการตัดประวัติออกได้จากตรงนี้ครับ</p>", unsafe_allow_html=True)
            delete_options = [f"{row['วันที่-เวลา']} | {row['ชื่อ-นามสกุล']} ({row['รหัสนักศึกษา']}) - {row['อาการเบื้องต้น']}" for idx, row in df.iterrows()]
            selected_student_to_delete = st.selectbox("เลือกแถวประวัตินักเรียนที่ต้องการลบถาวร:", delete_options, key="admin_delete_student_selectbox")
            del_time = selected_student_to_delete.split(" | ")[0]
            del_name = selected_student_to_delete.split(" | ")[1].split(" (")[0]
            
            # ปรับแต่งปุ่มลบ ไม่มีขอบขีดแดงรอบปุ่ม
            st.markdown("""
                <style>
                div[data-testid="stExpander"] button {{
                    background-color: #dc3545 !important; 
                    border: none !important;
                }}
                div[data-testid="stExpander"] button p, div[data-testid="stExpander"] button span {{
                    color: #ffffff !important;
                    font-weight: bold !important;
                }}
                div[data-testid="stExpander"] button:hover {{
                    background-color: #c82333 !important;
                }}
                </style>
            """, unsafe_allow_html=True)
            
            admin_delete_confirm = st.button("ยืนยันลบประวัตินักเรียนรายนี้ออกถาวร", use_container_width=True)
            if admin_delete_confirm:
                df = df[~((df["วันที่-เวลา"] == del_time) & (df["ชื่อ-นามสกุล"] == del_name))]
                save_data(df)
                st.success(f"ลบประวัติข้อมูลคิวของ {del_name} ออกจากระบบ CSV เรียบร้อยแล้ว")
                st.rerun()

        st.write("---")
        st.subheader("บันทึกผลการคัดกรองและรักษา")
        waiting_df = df[df["สถานะการรักษา"].astype(str).str.contains("รอ|กำลัง", na=False)]
        if waiting_df.empty:
            waiting_options = []
        else:
            waiting_options = [f"{row['ชื่อ-นามสกุล']} ({row['รหัสนักศึกษา']})" for idx, row in waiting_df.iterrows()]
        
        if not waiting_options:
            st.success("ตรวจรักษาเสร็จสิ้นครบทุกเคสเรียบร้อยแล้ว")
        else:
            selected_option = st.selectbox("เลือกชื่อนักเรียนที่ต้องการวินิจฉัย:", waiting_options)
            selected_student_name = selected_option.split(" (")[0]
            student_info = waiting_df[waiting_df["ชื่อ-นามสกุล"] == selected_student_name].iloc[-1]
            custom_blue_box(f"📋 เคสของ: {selected_student_name} | โรคประจำตัว: {student_info.get('โรคประจำตัว', '-')} | แผนก: {student_info['แผนกวิชา']} | อาการ: {student_info['อาการเบื้องต้น']}")
            treatment_status = st.radio("สั่งการรักษาทางแพทย์:", ["จ่ายยาและให้กลับไปเรียนต่อ", "ให้นอนพักฟื้นที่ห้องพยาบาล", "ส่งต่อโรงพยาบาลภายนอก (เคสฉุกเฉิน)"])
            st.markdown("##### สั่งจ่ายยาตัดสต็อกคลังหลังบ้าน:")
            med_col1, med_col2 = st.columns([2, 1])
            with med_col1:
                selected_med = st.selectbox("เลือกตัวยาที่จ่ายให้เด็ก:", df_stock["ชื่อยา/เวชภัณฑ์"].tolist())
            with med_col2:
                selected_qty = st.number_input("จำนวนที่จ่าย (หน่วยตามชนิดยา):", min_value=0, max_value=50, value=2)
            treatment_detail = st.text_input("ระบุรายละเอียดตัวยาที่จ่าย / อาการเพิ่มเติม:")
            
            update_btn = st.button("บันทึกและอัปเดตสถานะ", type="primary")
            if update_btn:
                stock_idx = df_stock[df_stock["ชื่อยา/เวชภัณฑ์"] == selected_med].index[0]
                current_stock_qty = df_stock.at[stock_idx, "คงเหลือ"]
                if selected_qty > current_stock_qty:
                    st.error(f"ไม่สามารถบันทึกได้! ยาในคลังมีไม่พอจ่าย (ในคลังเหลืออยู่เพียง {current_stock_qty} หน่วย)")
                else:
                    idx = df[df["ชื่อ-นามสกุล"] == selected_student_name].index[-1]
                    df.at[idx, "สถานะการรักษา"] = treatment_status
                    final_note = f"จ่าย: {selected_med} ({selected_qty} หน่วย) | หมายเหตุ: {treatment_detail}"
                    df.at[idx, "การจ่ายยา/หมายเหตุ"] = final_note
                    df.at[idx, "อาจารย์ผู้บันทึก"] = st.session_state.current_user
                    save_data(df)
                    if selected_qty > 0:
                        df_stock.at[stock_idx, "คงเหลือ"] -= selected_qty
                        df_stock.to_csv(STOCK_FILE, index=False, encoding="utf-8-sig")
                        if df_stock.at[stock_idx, "คงเหลือ"] <= 20:
                            send_telegram_notification(f"แจ้งเตือนด่วน (RTC คลังยา)\nเวชภัณฑ์: {selected_med}\nสถานะ: ใกล้หมดแล้ว! คงเหลือเพียง {df_stock.at[stock_idx, 'คงเหลือ']} {df_stock.at[stock_idx, 'หน่วย']}")
                    send_telegram_notification(f"ตรวจรักษาสำเร็จ (RTC Care)\nผู้ป่วย: {selected_student_name}\nผลวินิจฉัย: {treatment_status}\nการจ่ายยา: {selected_med} จำนวน {selected_qty} หน่วย\nผู้บันทึก: {st.session_state.current_user}")
                    st.success(f"บันทึกผลการรักษาและหักยอดคลังยาของ {selected_student_name} สำเร็จแล้ว")
                    st.rerun()

    st.write("---")
    st.markdown("### ตรวจสอบคลังยาห้องพยาบาล (Real-time Inventory)")
    stock_cols = st.columns(len(df_stock))
    for s_idx, s_row in df_stock.iterrows():
        with stock_cols[s_idx]:
            if s_row["คงเหลือ"] <= 20:
                custom_red_box(f"🚨 **{s_row['ชื่อยา/เวชภัณฑ์']}**<br>ใกล้หมด! เหลือเพียง: {s_row['คงเหลือ']} {s_row['หน่วย']}")
            else:
                st.success(f"**{s_row['ชื่อยา/เวชภัณฑ์']}** \n\n คงเหลือ: {s_row['คงเหลือ']} {s_row['หน่วย']}")

    st.write("---")
    st.markdown("### แผงบริหารและจัดการคลังยา (Inventory Management Control)")
    stock_tab1, stock_tab2, stock_tab3 = st.tabs(["เติมยา / แก้ไขยอดคงเหลือด่วน", "ลงทะเบียนเพิ่มยาชนิดใหม่เข้าคลัง", "ลบรายชื่อยาและล้างประวัติขยะ"])
    
    with stock_tab1:
        st.markdown("##### ระบบเติมยาเข้าคลัง หรือ พิมพ์ยอดแก้ไขสต็อกที่ผิดพลาด")
        add_col1, add_col2, add_col3, add_col4 = st.columns([1.5, 1.2, 1.3, 1.2], gap="small")
        with add_col1:
            restock_med = st.selectbox("เลือกรายการยาที่ต้องการจัดการ:", df_stock["ชื่อยา/เวชภัณฑ์"].tolist(), key="restock_select")
        with add_col2:
            manage_mode = st.radio("เลือกการทำงาน:", ["เติมเพิ่มเข้าคลัง", "พิมพ์แก้ตัวเลขโดยตรง"], key="manage_mode_radio")
        with add_col3:
            r_idx_check = df_stock[df_stock["ชื่อยา/เวชภัณฑ์"] == restock_med].index[0]
            unit_label = df_stock.at[r_idx_check, "หน่วย"]
            if manage_mode == "เติมเพิ่มเข้าคลัง":
                input_qty = st.number_input(f"ระบุจำนวนที่เติมเพิ่ม ({unit_label}):", min_value=1, max_value=2000, value=100, key="restock_num")
            else:
                input_qty = st.number_input(f"ยอดคงเหลือที่ถูกต้อง ({unit_label}):", min_value=0, max_value=5000, value=int(df_stock.at[r_idx_check, "คงเหลือ"]), key="rewrite_num")
        with add_col4:
            st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
            restock_btn = st.button("แท็บยืนยันบันทึกยอดคลังยา", type="primary", key="confirm_restock_btn", use_container_width=True)
        if restock_btn:
            r_idx = df_stock[df_stock["ชื่อยา/เวชภัณฑ์"] == restock_med].index[0]
            if manage_mode == "เติมเพิ่มเข้าคลัง":
                df_stock.at[r_idx, "คงเหลือ"] += input_qty
                st.success(f"เพิ่มยอด {restock_med} สำเร็จจำนวน +{input_qty} {df_stock.at[r_idx, 'หน่วย']} เรียบร้อยแล้ว")
            else:
                df_stock.at[r_idx, "คงเหลือ"] = input_qty
                st.success(f"รีเซ็ตยอด {restock_med} เป็น {input_qty} {df_stock.at[r_idx, 'หน่วย']} ตามที่แก้ไขเรียบร้อยแล้ว")
            df_stock.to_csv(STOCK_FILE, index=False, encoding="utf-8-sig")
            st.rerun()

    with stock_tab2:
        st.markdown("##### ลงทะเบียนยา / เวชภัณฑ์ ชนิดใหม่แกะกล่องเข้าสู่ระบบ")
        new_col1, new_col2, new_col3, new_col4 = st.columns([1.8, 1.0, 1.2, 1.2], gap="small")
        with new_col1:
            new_med_name = st.text_input("ชื่อยา/เวชภัณฑ์ใหม่ที่ต้องการเพิ่ม:", placeholder="เช่น ยาแก้ไอขับเสมหะ, ผ้าก๊อซพันแผล")
        with new_col2:
            new_med_unit = st.text_input("หน่วยนับ:", placeholder="เช่น เม็ด", value="เม็ด")
        with new_col3:
            new_med_qty = st.number_input("ยอดสต็อกเริ่มต้นที่มีอยู่:", min_value=0, max_value=5000, value=100)
        with new_col4:
            st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
            add_new_med_btn = st.button("ยืนยันลงทะเบียนยาใหม่", type="primary", key="add_new_med_btn", use_container_width=True)
        if add_new_med_btn:
            if not new_med_name.strip():
                st.error("กรุณากรอกชื่อยาด้วยครับ")
            elif new_med_name.strip() in df_stock["ชื่อยา/เวชภัณฑ์"].tolist():
                st.error("ยาตัวนี้มีอยู่ในระบบแล้วครับ! หากต้องการเพิ่มยอดให้ไปใช้แท็บแรก")
            else:
                df_stock = pd.concat([df_stock, pd.DataFrame([{"ชื่อยา/เวชภัณฑ์": new_med_name.strip(), "คงเหลือ": new_med_qty, "หน่วย": new_med_unit.strip()}])], ignore_index=True)
                df_stock.to_csv(STOCK_FILE, index=False, encoding="utf-8-sig")
                st.success(f"สำเร็จ! ลงทะเบียน '{new_med_name.strip()}' เข้าสู่ระบบห้องพยาบาลเรียบร้อยแล้ว")
                st.rerun()

    with stock_tab3:
        st.markdown("##### ระบบลบรายชื่อยาและกวาดล้างประวัติขยะถาว")
        delete_med_target = st.selectbox("เลือกชื่อยาที่ต้องการ ลบทำลายทิ้ง ออกจากฐานข้อมูลงาน:", df_stock["ชื่อยา/เวชภัณฑ์"].tolist(), key="delete_med_target_select")
        st.markdown("<p style='color:#dc3545; font-size:13px;'>หมายเหตุ: การกดปุ่มนี้จะลบตัวยาออกจากคลัง และกวาดล้างประวัติเก่าทั้งหมดที่มีชื่อยานี้อยู่ทิ้งทันที เพื่อไม่ให้มีคำนี้ติดไปในไฟล์รายงาน CSV ตอนส่งออกครับ</p>", unsafe_allow_html=True)
        
        st.markdown("""
            <style>
            button[key="execute_delete_btn"] {{ 
                background-color: #dc3545 !important; 
                border: none !important; 
            }}
            button[key="execute_delete_btn"] p {{
                color: #ffffff !important;
                font-weight: bold !important;
            }}
            </style>
        """, unsafe_allow_html=True)
        
        execute_delete_btn = st.button("ยืนยันลบยาและล้างประวัติ", use_container_width=True, key="execute_delete_btn")
        if execute_delete_btn:
            df_stock = df_stock[df_stock["ชื่อยา/เวชภัณฑ์"] != delete_med_target]
            df_stock.to_csv(STOCK_FILE, index=False, encoding="utf-8-sig")
            if os.path.exists(DB_FILE):
                raw_df = pd.read_csv(DB_FILE)
                if "การจ่ายยา/หมายเหตุ" in raw_df.columns:
                    raw_df = raw_df[~raw_df["การจ่ายยา/หมายเหตุ"].astype(str).str.contains(delete_med_target, na=False)]
                raw_df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")
            st.success(f"ลบ '{delete_med_target}' และกวาดล้างข้อมูลขยะออกจากไฟล์ CSV เรียบร้อยแล้วครับ")
            st.rerun()

    if not df.empty:
        st.write("---")
        st.markdown("### ส่งออกข้อมูลรายงานสถานพยาบาล")
        st.download_button(
            label="ดาวน์โหลดรายงานประวัติการรักษาทั้งหมด (.CSV)",
            data=df.to_csv(index=False).encode('utf-8-sig'),
            file_name=f"RTC_Care_Report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="download_report_btn"
        )