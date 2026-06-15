import streamlit as st
import pandas as pd
import os
import base64
import requests  
from datetime import datetime

# 1. ตั้งค่าหน้าจอ (ต้องอยู่บรรทัดแรกสุดเสมอ)
st.set_page_config(page_title="RYTC Infirmary", page_icon="🏥", layout="centered")

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
        requests.post(url, json=payload, timeout=5)
    except:
        pass

# ==========================================
# ฟังก์ชันจัดการภาพพื้นหลังอัจฉริยะ (แก้ไขจุดล็อก CSS ครอบจักรวาล)
# ==========================================
def set_perfect_background():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # รวม Path เพื่อให้ระบบสแกนหาไฟล์รูปภาพได้ง่ายที่สุด
    possible_paths = [
        os.path.join(base_dir, "images", "bg.jpg"),
        os.path.join(base_dir, "RYTC_Infirmary", "images", "bg.jpg"),
        os.path.join(base_dir, "bg.jpg"),
        "images/bg.jpg",
        "bg.jpg"
    ]
    
    encoded_string = ""
    found_path = ""
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode()
                    found_path = path
                    break 
            except Exception as e:
                print(f"❌ เจอไฟล์ภาพแต่ระบบเปิดอ่านไม่ได้: {path} | Error: {e}")
                
    if encoded_string:
        # พิมพ์ล็อกแจ้งเตือนใน Terminal ฝั่ง Server ให้เห็นชัดเจนว่าโหลดภาพสำเร็จจากที่ไหน
        print(f"✅ [SUCCESS] โหลดภาพพื้นหลังสำเร็จจากตำแหน่ง: {found_path}")
        
        bg_css = f"""
        <style>
        /* 🛠️ เจาะลึกถึงคลาสหลักของ Streamlit ทุกเวอร์ชันเพื่อบังคับให้พื้นหลังแสดงผล */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewMain"], .stApp, .main {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                              url("data:image/jpeg;base64,{encoded_string}") !important;
            background-size: cover !important;
            background-position: center center !important;
            background-attachment: fixed !important;
            background-repeat: no-repeat !important;
        }}
        
        /* ปลดล็อกสีพื้นหลังทับซ้อนชั้นใน เพื่อให้มองเห็นทะลุไปถึงภาพพื้นหลัง */
        [data-testid="stAppViewMain"] {{
            background-color: transparent !important;
        }}
        
        /* 🔵 เปลี่ยนแถบ Header บนสุดให้เป็นสีกรมท่าเข้ม (Navy Blue) */
        header[data-testid="stHeader"], [data-testid="stHeader"], div[data-testid="stAppHeader"] {{
            background-color: #0f2547 !important;
        }}
        header[data-testid="stHeader"] a,
        header[data-testid="stHeader"] button, 
        header[data-testid="stHeader"] span,
        header[data-testid="stHeader"] svg,
        div[data-testid="stAppHeader"] svg {{
            color: #ffffff !important;
            fill: #ffffff !important;
        }}
        
        /* ปรับแถบเส้นคั่นแนวนอนด้านบนให้เป็นสีน้ำเงินประกาย */
        hr {{
            border: 0 !important;
            height: 4px !important;
            background: linear-gradient(to right, #0056b3, #00aaff) !important;
            margin-top: 10px !important;
            margin-bottom: 25px !important;
            opacity: 1 !important;
        }}
        
        /* 🎨 ปรับสีเนื้อหาหลักและข้อความหน้าช่องให้เป็นสีกรมท่าเข้ม */
        [data-testid="stMainBlockContainer"] h1, 
        [data-testid="stMainBlockContainer"] h2, 
        [data-testid="stMainBlockContainer"] h3, 
        [data-testid="stMainBlockContainer"] h4, 
        [data-testid="stMainBlockContainer"] h5, 
        [data-testid="stMainBlockContainer"] h6, 
        [data-testid="stMainBlockContainer"] label, 
        [data-testid="stMainBlockContainer"] p {{
            color: #1a365d !important;
            font-family: "Sarabun", sans-serif;
        }}
        
        [data-testid="stMainBlockContainer"] :not(input):not(textarea):not(div[data-baseweb="select"]) > span {{
            color: #1a365d !important;
        }}
        
        /* 📢 ปรับกล่องประชาสัมพันธ์ st.info */
        [data-testid="stNotification"] {{
            background-color: #0b1e36 !important; 
            border-left: 6px solid #0056b3 !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 15px rgba(11, 30, 54, 0.15) !important;
        }}
        [data-testid="stNotification"] div, [data-testid="stNotification"] p {{
            color: #ffffff !important;
            font-size: 15.5px !important;
            font-weight: 500 !important;
        }}
        
        /* ✍️ ตกแต่งฟอร์มกรอกข้อมูล */
        [data-testid="stForm"] {{
            background-color: rgba(255, 255, 255, 0.93) !important;
            border: 1px solid #d1dbed !important;
            border-radius: 12px !important;
            padding: 25px !important;
            box-shadow: 0 8px 24px rgba(26, 54, 93, 0.04) !important;
        }}
        
        .stTextInput input {{
            background-color: #f4f7fc !important; 
            color: #1a365d !important; 
            caret-color: #1a365d !important; 
            border: 1px solid #cedbe7 !important;
            border-radius: 8px !important;
        }}
        
        .stSelectbox div[data-baseweb="select"] {{
            background-color: #1a365d !important; 
            border: 1px solid #142d52 !important;
            border-radius: 8px !important;
        }}
        
        .stSelectbox div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] p,
        .stSelectbox div[data-baseweb="select"] span,
        .stSelectbox div[data-baseweb="select"] svg {{
            color: #ffffff !important;
            fill: #ffffff !important;
        }}
        
        div[data-baseweb="popover"] ul {{
            background-color: #ffffff !important;
        }}
        div[data-baseweb="popover"] li[role="option"] {{
            background-color: #ffffff !important;
            color: #000000 !important; 
        }}
        div[data-baseweb="popover"] li[role="option"]:hover {{
            background-color: #e2e8f0 !important; 
            color: #000000 !important;
        }}
        
        .stTextInput input::placeholder {{
            color: #718096 !important;
            opacity: 1 !important;
        }}
        
        .stTextInput input:focus {{
            border-color: #007bff !important;
            box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.15) !important;
            background-color: #ffffff !important;
            color: #1a365d !important;
            caret-color: #1a365d !important; 
        }}
        .stSelectbox div[data-baseweb="select"]:focus-within {{
            border-color: #007bff !important;
            box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.15) !important;
        }}
        
        /* 🚀 ปุ่มบันทึกข้อมูล */
        .stFormSubmitButton button, 
        button[data-testid="baseButton-primary"] {{
            background-color: #1b4d89 !important;
            border: 1px solid #143a68 !important;
            border-radius: 8px !important;
            width: 100% !important;
            height: 48px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 12px rgba(27, 77, 137, 0.15) !important;
        }}
        
        .stFormSubmitButton button p,
        button[data-testid="baseButton-primary"] p {{
            color: #ffffff !important; 
        }}
        
        .stFormSubmitButton button:hover,
        button[data-testid="baseButton-primary"]:hover {{
            background-color: #12355e !important; 
            box-shadow: 0 6px 16px rgba(18, 53, 94, 0.25) !important;
            transform: translateY(-1px);
        }}
        
        .responsive-h1 {{
            text-align: center; 
            color: #800000 !important; 
            font-family: "Sarabun", sans-serif;
            font-weight: bold; 
            margin-bottom: 0;
            font-size: calc(1.6rem + 1.2vw) !important;
            line-height: 1.3 !important;
        }}
        .responsive-h4 {{
            text-align: center; 
            color: #4a5568 !important; 
            font-family: "Sarabun", sans-serif;
            margin-top: 5px; 
            margin-bottom: 20px;
            font-size: calc(1.0rem + 0.3vw) !important;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: rgba(248, 249, 250, 0.95) !important;
            border-right: 1px solid #dee2e6 !important;
        }}
        [data-testid="stSidebarNavigation"] ul li div span, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebarNavigation"] a span {{
            color: #2d3748 !important; font-weight: 600 !important; font-size: 16px !important;
        }}
        
        input::-ms-reveal, input::-ms-clear {{ display: none !important; }}
        
        [data-testid="stSidebarNavigation"] ul li:first-child div span, [data-testid="stSidebarNavigation"] ul li:first-child a span {{
            visibility: hidden; position: relative;
        }}
        [data-testid="stSidebarNavigation"] ul li:first-child div span::after, [data-testid="stSidebarNavigation"] ul li:first-child a span::after {{
            content: "หน้าหลัก"; visibility: visible; position: absolute; left: 0; top: 0; white-space: nowrap; color: #2d3748 !important; 
        }}

        @media (max-width: 768px) {{
            html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewMain"], .stApp, .main {{
                background-attachment: scroll !important; /* ป้องกันบั๊กบน iOS มือถือ */
            }}
            [data-testid="stMainBlockContainer"] p, 
            [data-testid="stMainBlockContainer"] label, 
            [data-testid="stMainBlockContainer"] span {{
                font-size: 14.5px !important;
            }}
        }}
        </style>
        """
        st.markdown(bg_css, unsafe_allow_html=True)
    else:
        # หากระบบหาไฟล์ภาพในตำแหน่งที่กำหนดไม่เจอเลย จะเปลี่ยนเป็นสีนวลตาแทนแอปพัง
        print("❌ [WARNING] หาไฟล์ชื่อ bg.jpg ไม่พบในระบบ! กำลังเปิดใช้พื้นหลังสีนวลสำรอง")
        st.markdown("<style>html, body, .stApp, [data-testid='stAppViewContainer'] {background-color: #f4f7fc !important;}</style>", unsafe_allow_html=True)

set_perfect_background()

# ==========================================
# หัวข้อหน้าเว็บแบบ Responsive
# ==========================================
st.markdown("<h1 class='responsive-h1'>ระบบลงทะเบียนผู้เข้ารับบริการห้องพยาบาล</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='responsive-h4'>วิทยาลัยเทคนิคระยอง (Rayong Technical College / RYTC)</h4>", unsafe_allow_html=True)
st.write("---")

st.info("📢 ประชาสัมพันธ์: ช่วงนี้อากาศเปลี่ยนแปลงบ่อย หากมีอาการไข้หรือไอ ขอความร่วมมือนักศึกษาสวมหน้ากากอนามัยก่อนเข้าใช้บริการห้องพยาบาลทุกครั้ง ขอบคุณค่ะ")

st.markdown("### 📝 กรอกข้อมูลเพื่อแจ้งความประสงค์เข้าใช้บริการ")

# 📂 จัดการฐานข้อมูล CSV
DB_FILE = "infirmary_records.csv"
COLUMNS = ["วันที่-เวลา", "รหัสนักศึกษา", "ชื่อ-นามสกุล", "โรคประจำตัว", "แผนกวิชา", "อาการเบื้องต้น", "สถานะการรักษา", "การจ่ายยา/หมายเหตุ", "อาจารย์ผู้บันทึก"]

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=COLUMNS).to_csv(DB_FILE, index=False, encoding="utf-8-sig")
else:
    try:
        existing_df = pd.read_csv(DB_FILE)
        if "โรคประจำตัว" not in existing_df.columns:
            existing_df.insert(3, "โรคประจำตัว", "-")
            existing_df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")
    except:
        pass

# 📥 ฟอร์มรับข้อมูลนักเรียน
with st.form(key="student_form", clear_on_submit=True):
    
    # 1. กล่องกรอกข้อมูลหลัก
    student_id = st.text_input("รหัสนักศึกษา (11 หลัก):", placeholder="เช่น 67219010049", max_chars=11)
    student_name = st.text_input("ชื่อ - นามสกุล:", placeholder="เช่น นายสมชาย ตั้งใจเรียน")
    student_medical_condition = st.text_input("โรคประจำตัว (ถ้าไม่มีให้เว้นว่างไว้):", placeholder="เช่น หอบหืด, ภูมิแพ้อากาศ (หากไม่มีไม่ต้องกรอก)")

    # 2. เลือกแผนกวิชา
    departments = [
        "ช่างยนต์", "ช่างกลโรงงาน", "ช่างเชื่อมโลหะ", "ช่างไฟฟ้ากำลัง", 
        "ช่างอิเล็กทรอนิกส์", "ช่างก่อสร้าง", "สถาปัตยกรรม", "เทคโนโลยีสารสนเทศ (IT)", 
        "การบัญชี", "การตลาด", "การเลขานุการ", "คอมพิวเตอร์ธุรกิจ", "โลจิสติกส์"
    ]
    student_dept = st.selectbox("แผนกวิชา / สาขางาน:", departments)
    
    # 3. ระบุอาการป่วย
    symptoms = [
        "ปวดศีรษะ / เป็นไข้", "ปวดท้อง / ท้องเสีย / ท้องอืด", 
        "ทำแผลอุบัติเหตุ / มีบาดแผล", "หน้ามืด / เป็นลม / คลื่นไส้", 
        "อาการแพ้ / ผื่นคัน / แมลงสัตว์กัดต่อย", "กล้ามเนื้ออักเสบ / เคล็ดขัดยอก", "อื่น ๆ (โปรดระบุรายละเอียดข้างล่าง)"
    ]
    selected_symptom = st.selectbox("อาการป่วยเบื้องต้น:", symptoms)
    additional_detail = st.text_input("รายละเอียดเพิ่มเติม (ถ้ามี):", placeholder="เช่น ปวดหัวข้างขวา, เผลอโดนมีดบาดที่นิ้วชี้")

    # 4. ปุ่มกดส่งข้อมูล
    submit_btn = st.form_submit_button("บันทึกข้อมูลและส่งคิวเข้าห้องพยาบาล", type="primary")

    # ==========================================
    # 🔥 จุดแก้ไขหลัก: ย้ายระบบตรวจสอบเงื่อนไขทั้งหมดมารวมไว้หลังการกด Submit ปุ่มฟอร์ม
    # ==========================================
    if submit_btn:
        # ตรวจสอบกรณีไม่ได้กรอกข้อมูลสำคัญ
        if not student_id.strip() or not student_name.strip():
            st.error("ไม่สามารถบันทึกได้: กรุณากรอกรหัสนักศึกษาและชื่อ-นามสกุลให้ครบถ้วนก่อนครับ")
        
        # ตรวจสอบรูปแบบรหัสนักศึกษา
        elif not student_id.strip().isdigit():
            st.error("ไม่สามารถบันทึกได้: รหัสนักศึกษาต้องเป็นตัวเลขเท่านั้น กรุณากรอกใหม่")
        elif len(student_id.strip()) != 11:
            st.error(f"ไม่สามารถบันทึกได้: รหัสนักศึกษาต้องครบ 11 หลักพอดี (ปัจจุบันกรอกไป {len(student_id.strip())} หลัก)")
            
        # ตรวจสอบรูปแบบชื่อและนามสกุล
        elif " " not in student_name.strip():
            st.error("ไม่สามารถบันทึกได้: กรุณากรอกทั้งชื่อและนามสกุล โดยเคาะเว้นวรรคตรงกลางด้วยครับ")
            
        else:
            # รวมข้อมูลอาการป่วยให้ถูกต้อง
            if selected_symptom.startswith("อื่น ๆ") and additional_detail.strip():
                final_symptom = f"อื่น ๆ: {additional_detail.strip()}"
            elif additional_detail.strip():
                final_symptom = f"{selected_symptom} ({additional_detail.strip()})"
            else:
                final_symptom = selected_symptom

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            final_medical_condition = student_medical_condition.strip() if student_medical_condition.strip() else "-"
            
            # เตรียมแพ็กเกจข้อมูลชุดใหม่
            new_record = {
                "วันที่-เวลา": current_time,
                "รหัสนักศึกษา": student_id.strip(),
                "ชื่อ-นามสกุล": student_name.strip(),
                "โรคประจำตัว": final_medical_condition,
                "แผนกวิชา": student_dept,
                "อาการเบื้องต้น": final_symptom,
                "สถานะการรักษา": "รอดำเนินการคัดกรอง",  
                "การจ่ายยา/หมายเหตุ": "-",
                "อาจารย์ผู้บันทึก": "-"  
            }
            
            # บันทึกลงระบบไฟล์ CSV
            df = pd.read_csv(DB_FILE)
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = "-"
            
            filtered_record = {k: new_record.get(k, "-") for k in COLUMNS}
            df = pd.concat([df, pd.DataFrame([filtered_record])], ignore_index=True)
            df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")
            
            # ส่งรายงานด่วนเข้าไปที่กลุ่ม Telegram
            tg_msg = f"🚨 *รายงานคิวผู้ป่วยใหม่ (RYTC Care)*\n👤 *ชื่อ:* {student_name.strip()}\n🆔 *รหัส:* {student_id.strip()}\n🏢 *แผนก:* {student_dept}\n🩺 *โรคประจำตัว:* {final_medical_condition}\n😷 *อาการ:* {final_symptom}"
            send_telegram_notification(tg_msg)
            
            # แสดงความยินดีบนหน้าจอหลัก
            st.success(f"🎉 บันทึกข้อมูลของ {student_name.strip()} สำเร็จ ระบบได้ส่งคิวไปยังคุณครูพยาบาลเรียบร้อยแล้ว กรุณาพักรอเรียกชื่อสักครู่นะครับ")