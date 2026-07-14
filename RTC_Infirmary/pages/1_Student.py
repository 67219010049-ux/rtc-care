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
        requests.post(url, json=payload)
    except:
        pass

# ==========================================
# ฟังก์ชันจัดการภาพพื้นหลังอัจฉริยะ + บังคับใช้ฟอนต์ IBM Plex Sans Thai 100%
# ==========================================
def set_perfect_background():
    possible_paths = ["RTC_Infirmary/images/bg.jpg", "images/bg.jpg", "bg.jpg"]
    encoded_string = ""
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode()
                    break 
            except:
                pass

    st.markdown(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@300;400;500;600;700&display=swap" rel="stylesheet">',
        unsafe_allow_html=True
    )
                
    if encoded_string:
        bg_css = f"""
        <style>
        /* ✅ แก้ไขจุดนี้: เจาะจงเฉพาะองค์ประกอบข้อความที่เราสร้างขึ้นมา 
           และเว้นวรรคไม่ให้ไปทับคลาสไอคอน (.material-icons, [class*="icon"]) ของระบบ
        */
        p, label, input, select, button, th, td, h1, h2, h3, h4, h5, h6,
        span[data-testid="stWidgetLabel"] p, 
        .stMarkdown p, 
        div[data-baseweb="select"] div,
        div[data-baseweb="input"] input {{
            font-family: 'IBM Plex Sans Thai', sans-serif !important;
        }}

        /* บังคับยกเว้นไอคอนทุกชนิด ไม่ให้โดนเปลี่ยนฟอนต์ */
        .material-icons, 
        .material-symbols-rounded,
        [class*="icon"], 
        [class*="Icon"],
        span[data-testid="stIcon"] {{
            font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        }}

        /* ส่วน CSS อื่นๆ ด้านล่างนี้ปล่อยไว้เหมือนเดิมได้เลยครับ */
        div[data-testid="stWidgetInstructions"], 
        div[data-testid="stInputHelperText"],
        div[class*="stWidgetInstructions"],
        div[class*="stInputHelperText"],
        p[class*="stInputHelperText"],
        .stWidgetInstructions,
        [data-testid="stForm"] div[data-testid="stWidgetInstructions"],
        [data-testid="stForm"] .stWidgetInstructions,
        div[data-testid="stTextInput"] small,
        div[data-testid="stTextInput"] div[data-testid="stWidgetInstructions"],
        div[data-testid="stTextInput"] > div:last-child:not(:has(input)),
        div[data-baseweb="input"] + div {{
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            height: 0px !important;
            max-height: 0px !important;
            font-size: 0px !important;
            padding: 0px !important;
            margin: 0px !important;
            position: absolute !important;
            overflow: hidden !important;
            pointer-events: none !important;
        }}

        header[data-testid="stHeader"] {{
            background-color: #001f3f !important;
            border-bottom: none !important;
        }}
        header[data-testid="stHeader"] button, header[data-testid="stHeader"] a, header[data-testid="stHeader"] span {{
            color: #ffffff !important;
        }}
        
        .stApp {{
            background-image: linear-gradient(rgba(245, 247, 250, 0.92), rgba(245, 247, 250, 0.92)), 
                              url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        div[data-baseweb="input"] {{
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important; 
            border-radius: 10px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
            transition: all 0.3s ease !important;
        }}
        div[data-baseweb="input"]:focus-within {{
            border-color: #001f3f !important;
            box-shadow: 0 0 0 3px rgba(0, 31, 63, 0.12) !important;
        }}
        div[data-baseweb="input"] input {{
            color: #1e293b !important;
            background-color: #ffffff !important;
            border: none !important;
            caret-color: #001f3f !important; 
        }}
        div[data-baseweb="input"] input::placeholder {{
            color: #94a3b8 !important;
            opacity: 1 !important;
            font-family: 'IBM Plex Sans Thai', sans-serif !important;
        }}
        
        div[data-baseweb="select"] {{
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 10px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
            transition: all 0.3s ease !important;
        }}
        div[data-baseweb="select"]:focus-within {{
            border-color: #001f3f !important;
            box-shadow: 0 0 0 3px rgba(0, 31, 63, 0.12) !important;
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
            font-family: 'IBM Plex Sans Thai', sans-serif !important;
        }}
        
        div[data-testid="stForm"] {{
            background-color: #ffffff !important;
            border: none !important;
            border-radius: 16px !important;
            padding: 30px !important;
            box-shadow: 0 10px 25px rgba(0, 31, 63, 0.06) !important;
        }}

        div.stFormSubmitButton > button {{
            background-color: #ffffff !important;
            color: #001f3f !important;
            border: 2px solid #001f3f !important;
            border-radius: 25px !important;
            width: 100% !important;
            height: 48px !important;
            font-weight: bold !important;
            font-size: 16px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 6px rgba(0, 31, 63, 0.05) !important;
        }}
        div.stFormSubmitButton > button p,
        div.stFormSubmitButton > button span {{
            color: #001f3f !important;
            font-weight: bold !important;
            font-size: 16px !important;
        }}
        div.stFormSubmitButton > button:hover {{
            background-color: #001f3f !important;
            color: #ffffff !important;
            box-shadow: 0 6px 12px rgba(0, 31, 63, 0.2) !important;
            transform: translateY(-1px);
        }}
        div.stFormSubmitButton > button:hover p,
        div.stFormSubmitButton > button:hover span {{
            color: #ffffff !important;
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

        [data-testid="stMainBlockContainer"] label {{
            font-weight: 600 !important;
            font-size: 15px !important;
            margin-bottom: 4px !important;
            color: #334155 !important;
        }}
        
        .responsive-h1 {{
            text-align: center; 
            color: #001f3f !important;
            font-weight: 700; 
            margin-bottom: 0;
            font-size: calc(1.5rem + 1.2vw) !important;
            line-height: 1.3 !important;
            word-wrap: break-word;
        }}
        .responsive-h4 {{
            text-align: center; 
            color: #64748b !important; 
            margin-top: 5px; 
            margin-bottom: 20px;
            font-size: calc(0.9rem + 0.3vw) !important;
            line-height: 1.4 !important;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: rgba(248, 249, 250, 0.95) !important;
            border-right: 1px solid #dee2e6 !important;
        }}
        [data-testid="stSidebarNavigation"] ul li div span, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span, 
        [data-testid="stSidebarNavigation"] a span {{
            color: #2d3748 !important; font-weight: 600 !important; font-size: 16px !important;
        }}
        
        input::-ms-reveal, input::-ms-clear {{ display: none !important; }}
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
STANDARD_COLS = ["วันที่-เวลา", "รหัสนักศึกษา", "ชื่อ-นามสกุล", "โรคประจำตัว", "แผนกวิชา", "อาการเบื้องต้น", "สถานะการรักษา", "การจ่ายยา/หมายเหตุ", "อาจารย์ผู้บันทึก"]

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=STANDARD_COLS).to_csv(DB_FILE, index=False, encoding="utf-8-sig")

# ฟอร์มรับข้อมูลนักเรียน
with st.form(key="student_form", clear_on_submit=True):
    student_id = st.text_input("รหัสนักศึกษา:", placeholder="กรอกรหัสนักศึกษา 11 หลัก", max_chars=11)
    
    id_is_valid = True
    if student_id.strip():
        if not student_id.strip().isdigit():
            st.error("รหัสนักศึกษาต้องเป็นตัวเลขเท่านั้น กรุณาพิมพ์ใหม่")
            id_is_valid = False
        elif len(student_id.strip()) != 11:
            st.warning(f"ปัจจุบันกรอกไปแล้ว {len(student_id.strip())} หลัก (ต้องครบ 11 หลัก)")
            id_is_valid = False

    student_name = st.text_input("ชื่อ - นามสกุล:", placeholder="กรอกชื่อและนามสกุล (เช่น นายสมชาย ดีใจ)")
    
    name_is_valid = True
    if student_name.strip():
        if " " not in student_name.strip():
            st.warning("กรุณากรอกทั้งชื่อและนามสกุล โดยเคาะเว้นวรรคตรงกลางด้วยครับ")
            name_is_valid = False

    student_congenital_disease = st.text_input("โรคประจำตัว:", placeholder="ถ้าไม่มีให้เว้นว่างไว้ หรือพิมพ์ -")

    departments = [
        "ช่างยนต์", "ช่างกลโรงงาน", "ช่างเชื่อมโลหะ", "ช่างไฟฟ้ากำลัง", 
        "ช่างอิเล็กทรอนิกส์", "ช่างก่อสร้าง", "สถาปัตยกรรม", "เทคโนโลยีสารสนเทศ (IT)", 
        "การบัญชี", "การตลาด", "การเลขานุการ", "คอมพิวเตอร์ธุรกิจ", "โลจิสติกส์"
    ]
    student_dept = st.selectbox("แผนกวิชา / สาขางาน:", departments)
    
    symptoms = [
        "ปวดศีรษะ / เป็นไข้", "ปวดท้อง / ท้องเสีย / ท้องอืด", 
        "ทำแผลอุบัติเหตุ / มีบาดแผล", "หน้ามืด / เป็นลม / คลื่นไส้", 
        "อาการแพ้ / ผื่นคัน / แมลงสัตว์กัดต่อย", "กล้ามเนื้ออักเสบ / เคล็ดขัดยอก", "อื่น ๆ (โปรดระบุรายละเอียดข้างล่าง)"
    ]
    selected_symptom = st.selectbox("อาการป่วยเบื้องต้น:", symptoms)
    additional_detail = st.text_input("รายละเอียดเพิ่มเติม (ถ้ามี):", placeholder="ระบุรายละเอียดอาการป่วยเพิ่มเติม")

    if selected_symptom.startswith("อื่น ๆ") and additional_detail.strip():
        final_symptom = f"อื่น ๆ: {additional_detail.strip()}"
    elif additional_detail.strip():
        final_symptom = f"{selected_symptom} ({additional_detail.strip()})"
    else:
        final_symptom = selected_symptom

    submit_btn = st.form_submit_button("บันทึกข้อมูลและส่งคิวเข้าห้องพยาบาล")

    if submit_btn:
        if not student_id.strip() or not student_name.strip():
            st.error("ไม่สามารถบันทึกได้: กรุณากรอกรหัสนักศึกษาและชื่อ-นามสกุลให้ครบถ้วนก่อนครับ")
        elif not id_is_valid:
            st.error("ไม่สามารถบันทึกได้: รหัสนักศึกษาไม่ถูกต้อง (ต้องเป็นตัวเลข 11 หลัก)")
        elif not name_is_valid:
            st.error("ไม่สามารถบันทึกได้: กรุณาใส่นามสกุลด้วยครับ")
        else:
            df = pd.read_csv(DB_FILE)
            
            is_duplicate = False
            if not df.empty:
                student_records = df[df["รหัสนักศึกษา"].astype(str) == student_id.strip()]
                if not student_records.empty:
                    last_record = student_records.iloc[-1]
                    try:
                        last_time = datetime.strptime(last_record["วันที่-เวลา"], "%Y-%m-%d %H:%M:%S")
                        time_diff = (datetime.now() - last_time).total_seconds()
                        if time_diff < 30 and last_record["อาการเบื้องต้น"] == final_symptom:
                            is_duplicate = True
                    except:
                        pass
            
            if is_duplicate:
                st.warning("⚠️ ระบบได้รับข้อมูลคิวของคุณเรียบร้อยแล้วครับ ไม่จำเป็นต้องกดส่งซ้ำซ้อน")
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
                    "status": "รอดำเนินการคัดกรอง",  
                    "การจ่ายยา/หมายเหตุ": "-",
                    "อาจารย์ผู้บันทึก": "-"  
                }
                
                final_record = {}
                for col in STANDARD_COLS:
                    if col == "สถานะการรักษา" and "status" in new_record:
                        final_record[col] = new_record["status"]
                    else:
                        final_record[col] = new_record.get(col, "-")
                
                for col in STANDARD_COLS:
                    if col not in df.columns:
                        df[col] = "-"
                        
                df = pd.concat([df, pd.DataFrame([final_record])], ignore_index=True)
                df = df[STANDARD_COLS]
                df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")
                
                tg_msg = f"รายงานคิวผู้ป่วยใหม่ (RTC Care)\nชื่อ: {student_name.strip()}\nรหัส: {student_id.strip()}\nโรคประจำตัว: {disease_val}\nแผนก: {student_dept}\nอาการ: {final_symptom}"
                send_telegram_notification(tg_msg)
                
                st.success(f"บันทึกข้อมูลของ {student_name.strip()} สำเร็จ ระบบได้ส่งคิวไปยังคุณครูพยาบาลเรียบร้อยแล้ว!")
                st.info(" ท่านสามารถคลิกเลือกเมนู **'Status'** ที่แถบเมนูด้านซ้ายมือเพื่อดูสถานะคิวของท่านได้ทันทีครับ")