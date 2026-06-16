import streamlit as st
import pandas as pd
import os
import base64
import requests  
from datetime import datetime

# 1. ตั้งค่าหน้าจอ (ต้องอยู่บรรทัดแรกสุดเสมอ)
st.set_page_config(page_title="RTC Infirmary", page_icon="🏥", layout="centered")

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
# ฟังก์ชันจัดการภาพพื้นหลังอัจฉริยะ + ปรับแต่งสไตล์ (เปลี่ยนสี Bar, ช่องข้อความ, และปุ่ม)
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
        /* 1. เปลี่ยนสีแถบ Bar ด้านบนสุดเป็นสีน้ำเงินกรมท่า */
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
        
        /* 2. ปรับแต่งช่องใส่ข้อความ (Input) ทุกจุดให้เป็นสีขาวล้วน และเคลียร์ขอบ */
        div[data-baseweb="input"] {{
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important; 
            border-radius: 6px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        }}
        div[data-baseweb="input"] input {{
            color: #1e293b !important;
            background-color: #ffffff !important;
            border: none !important;
            caret-color: #001f3f !important; 
        }}
        div[data-baseweb="input"] input::placeholder {{
            color: #94a3b8 !important;
        }}
        
        /* ปรับแต่งกล่อง Selectbox (Dropdown) ให้เป็นสีขาวคลีนเข้าชุดกัน */
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
        
        /* ปรับแต่งกรอบฟอร์มสี่เหลี่ยมด้านนอกให้โปร่งใสกลืนกับพื้นหลัง */
        div[data-testid="stForm"] {{
            background-color: rgba(255, 255, 255, 0.6) !important;
            border: 1px solid rgba(226, 232, 240, 0.8) !important;
            border-radius: 12px !important;
            padding: 25px !important;
        }}

        /* 3. ปรับแต่งปุ่มส่งข้อมูลในฟอร์มให้เป็นสีน้ำเงินกรมท่าล้วน */
        div.stFormSubmitButton > button {{
            background-color: #001f3f !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 6px !important;
            width: 100% !important;
            height: 48px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            transition: 0.2s all ease !important;
            box-shadow: 0 4px 6px rgba(0, 31, 63, 0.15) !important;
        }}
        div.stFormSubmitButton > button p {{
            color: #ffffff !important;
            font-weight: bold !important;
        }}
        div.stFormSubmitButton > button:hover {{
            background-color: #001122 !important;
            box-shadow: 0 6px 12px rgba(0, 31, 63, 0.3) !important;
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
            font-size: calc(1.6rem + 1.2vw) !important;
            line-height: 1.3 !important;
            word-wrap: break-word;
        }}
        .responsive-h4 {{
            text-align: center; 
            color: #4a5568 !important; 
            font-family: "Sarabun", sans-serif;
            margin-top: 5px; 
            margin-bottom: 20px;
            font-size: calc(1.0rem + 0.3vw) !important;
            line-height: 1.4 !important;
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
            [data-testid="stMainBlockContainer"] p, 
            [data-testid="stMainBlockContainer"] label, 
            [data-testid="stMainBlockContainer"] span,
            .stSelectbox label, .stTextInput label {{
                font-size: 14.5px !important;
            }}
            .stMarkdown h3 {{
                font-size: 18px !important;
            }}
        }}
        </style>
        """
        st.markdown(bg_css, unsafe_allow_html=True)

set_perfect_background()

# ==========================================
# หัวข้อหน้าเว็บแบบ Responsive
# ==========================================
st.markdown("<h1 class='responsive-h1'>ระบบลงทะเบียนผู้เข้ารับบริการห้องพยาบาล</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='responsive-h4'>วิทยาลัยเทคนิคระยอง (Rayong Technical College)</h4>", unsafe_allow_html=True)
st.write("---")

st.info("ประชาสัมพันธ์: ช่วงนี้อากาศเปลี่ยนแปลงบ่อย หากมีอาการไข้หรือไอ ขอความร่วมมือนักศึกษาสวมหน้ากากอนามัยก่อนเข้าใช้บริการห้องพยาบาลทุกครั้ง ขอบคุณค่ะ")

st.markdown("### กรอกข้อมูลเพื่อแจ้งความประสงค์เข้าใช้บริการ")

DB_FILE = "infirmary_records.csv"
# กำหนดโครงสร้างคอลัมน์มาตรฐาน รวมถึงคอลัมน์ โรคประจำตัว
STANDARD_COLS = ["วันที่-เวลา", "รหัสนักศึกษา", "ชื่อ-นามสกุล", "โรคประจำตัว", "แผนกวิชา", "อาการเบื้องต้น", "สถานะการรักษา", "การจ่ายยา/หมายเหตุ", "อาจารย์ผู้บันทึก"]

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=STANDARD_COLS).to_csv(DB_FILE, index=False, encoding="utf-8-sig")

# 📥 ฟอร์มรับข้อมูลนักเรียน
with st.form(key="student_form", clear_on_submit=True):
    
    # 1. กล่องรหัสนักศึกษา
    student_id = st.text_input("รหัสนักศึกษา (11 หลัก):", placeholder="เช่น 67219010049", max_chars=11)
    
    id_is_valid = True
    if student_id.strip():
        if not student_id.strip().isdigit():
            st.error("รหัสนักศึกษาต้องเป็นตัวเลขเท่านั้น กรุณาพิมพ์ใหม่")
            id_is_valid = False
        elif len(student_id.strip()) != 11:
            st.warning(f"ปัจจุบันกรอกไปแล้ว {len(student_id.strip())} หลัก (ต้องครบ 11 หลักพอดี)")
            id_is_valid = False

    # 2. กล่องชื่อ-นามสกุล
    student_name = st.text_input("ชื่อ - นามสกุล:", placeholder="เช่น นายสมชาย ตั้งใจเรียน")
    
    name_is_valid = True
    if student_name.strip():
        if " " not in student_name.strip():
            st.warning("กรุณากรอกทั้งชื่อและนามสกุล โดยเคาะเว้นวรรคตรงกลางด้วยครับ")
            name_is_valid = False

    # 3. ช่องกรอกโรคประจำตัว (เพิ่มใหม่ตามคำสั่งครับ)
    student_congenital_disease = st.text_input("โรคประจำตัว (ถ้าไม่มีให้เว้นว่างไว้ หรือพิมพ์ -):", placeholder="เช่น หอบหืด, แพ้ยาพารา, ไม่มี")

    # 4. เลือกแผนกวิชา
    departments = [
        "ช่างยนต์", "ช่างกลโรงงาน", "ช่างเชื่อมโลหะ", "ช่างไฟฟ้ากำลัง", 
        "ช่างอิเล็กทรอนิกส์", "ช่างก่อสร้าง", "สถาปัตยกรรม", "เทคโนโลยีสารสนเทศ (IT)", 
        "การบัญชี", "การตลาด", "การเลขานุการ", "คอมพิวเตอร์ธุรกิจ", "โลจิสติกส์"
    ]
    student_dept = st.selectbox("แผนกวิชา / สาขางาน:", departments)
    
    # 5. ระบุอาการเบื้องต้น
    symptoms = [
        "ปวดศีรษะ / เป็นไข้", "ปวดท้อง / ท้องเสีย / ท้องอืด", 
        "ทำแผลอุบัติเหตุ / มีบาดแผล", "หน้ามืด / เป็นลม / คลื่นไส้", 
        "อาการแพ้ / ผื่นคัน / แมลงสัตว์กัดต่อย", "กล้ามเนื้ออักเสบ / เคล็ดขัดยอก", "อื่น ๆ (โปรดระบุรายละเอียดข้างล่าง)"
    ]
    selected_symptom = st.selectbox("อาการป่วยเบื้องต้น:", symptoms)
    additional_detail = st.text_input("รายละเอียดเพิ่มเติม (ถ้ามี):", placeholder="เช่น ปวดหัวข้างขวา, เผลอโดนมีดบาดที่นิ้วชี้")

    if selected_symptom.startswith("อื่น ๆ") and additional_detail.strip():
        final_symptom = f"อื่น ๆ: {additional_detail.strip()}"
    elif additional_detail.strip():
        final_symptom = f"{selected_symptom} ({additional_detail.strip()})"
    else:
        final_symptom = selected_symptom

    # 6. ปุ่มกดส่งข้อมูล
    submit_btn = st.form_submit_button("บันทึกข้อมูลและส่งคิวเข้าห้องพยาบาล")

    if submit_btn:
        if not student_id.strip() or not student_name.strip():
            st.error("ไม่สามารถบันทึกได้: กรุณากรอกรหัสนักศึกษาและชื่อ-นามสกุลให้ครบถ้วนก่อนครับ")
        elif not id_is_valid:
            st.error("ไม่สามารถบันทึกได้: รหัสนักศึกษาไม่ถูกต้อง (ต้องเป็นตัวเลข 11 หลัก)")
        elif not name_is_valid:
            st.error("ไม่สามารถบันทึกได้: กรุณาใส่นามสกุลด้วยครับ")
        else:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            disease_val = student_congenital_disease.strip() if student_congenital_disease.strip() else "-"
            
            new_record = {
                "วันที่-เวลา": current_time,
                "รหัสนักศึกษา": student_id.strip(),
                "ชื่อ-นามสกุล": student_name.strip(),
                "โรคประจำตัว": disease_val,
                "แผนกวิชา": student_dept,
                "อาการเบื้องต้น": final_symptom,
                "สถานะการรักษา": "รอดำเนินการคัดกรอง",  
                "การจ่ายยา/หมายเหตุ": "-",
                "อาจารย์ผู้บันทึก": "-"  
            }
            
            # โหลดไฟล์เก่าขึ้นมาตรวจสอบโครงสร้างคอลัมน์
            df = pd.read_csv(DB_FILE)
            
            # ตรวจสอบเผื่อกรณีก่อนหน้าไม่มีคอลัมน์โรคประจำตัวในไฟล์เก่า จะได้สร้างคอลัมน์รองรับไว้ทันที
            for col in STANDARD_COLS:
                if col not in df.columns:
                    df[col] = "-"
                    
            df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
            # เรียงลำดับคอลัมน์ตามที่ระบุไว้
            df = df[STANDARD_COLS]
            df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")
            
            # ส่งแจ้งเตือนทาง Telegram พร้อมแสดงโรคประจำตัว (ถ้ามี)
            tg_msg = f"รายงานคิวผู้ป่วยใหม่ (RTC Care)\nชื่อ: {student_name.strip()}\nรหัส: {student_id.strip()}\nโรคประจำตัว: {disease_val}\nแผนก: {student_dept}\nอาการ: {final_symptom}"
            send_telegram_notification(tg_msg)
            
            st.success(f"บันทึกข้อมูลของ {student_name.strip()} สำเร็จ ระบบได้ส่งคิวไปยังคุณครูพยาบาลเรียบร้อยแล้ว กรุณานอนพักรอเรียกชื่อสักครู่นะครับ")