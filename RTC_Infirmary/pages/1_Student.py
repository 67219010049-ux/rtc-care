import streamlit as st
import pandas as pd
import os
import base64
import requests  
from datetime import datetime

# 1. ตั้งค่าหน้าจอ (ต้องอยู่บรรทัดแรกสุดเสมอ) -> เปลี่ยนเป็น RYTC
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
# ฟังก์ชันจัดการภาพพื้นหลังอัจฉริยะ (ปรับแต่ง Layout และ Theme สีใหม่ทั้งหมด)
# ==========================================
def set_perfect_background():
    possible_paths = [
        "RYTC_Infirmary/images/bg.jpg",  # เปลี่ยนเป็น RYTC
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
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                              url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        /* 🔵 เปลี่ยนแถบ Header บนสุดให้เป็นสีกรมท่าเข้ม (Navy Blue) */
        [data-testid="stHeader"] {{
            background-color: #0f2547 !important;
        }}
        /* ปรับสีไอคอนและปุ่ม Deploy บนแถบด้านบนให้เป็นสีขาว จะได้ไม่กลืนกับสีกรมท่า */
        [data-testid="stHeader"] a, 
        [data-testid="stHeader"] button, 
        [data-testid="stHeader"] span,
        [data-testid="stHeader"] svg {{
            color: #ffffff !important;
            fill: #ffffff !important;
        }}
        
        /* ปรับแถบเส้นคั่นแนวนอนด้านบนให้เป็นสีน้ำเงินประกาย ชัดเจน ไม่ดำทึบ */
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
        }}
        
        /* แยกสไตล์ของ span ทั่วไป เพื่อไม่ให้ไปทับตัวหนังสือในช่องกรอก */
        [data-testid="stMainBlockContainer"] :not(input):not(textarea):not(div[data-baseweb="select"]) > span {{
            color: #1a365d !important;
        }}
        
        /* 📢 ปรับกล่องประชาสัมพันธ์ st.info ให้เข้มขรึม ดึงสายตาเด่นชัดระดับพรีเมียม */
        [data-testid="stNotification"] {{
            background-color: #0b1e36 !important; /* น้ำเงินมิดไนท์บลูเข้มพิเศษ */
            border-left: 6px solid #0056b3 !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 15px rgba(11, 30, 54, 0.15) !important;
        }}
        [data-testid="stNotification"] div, [data-testid="stNotification"] p {{
            color: #ffffff !important;
            font-size: 15.5px !important;
            font-weight: 500 !important;
        }}
        
        /* ✍️ ตกแต่งช่องใส่คำตอบ (Inputs) และบล็อกฟอร์มให้โมเดิร์นสวยงาม ไม่ใช่สีดำ */
        [data-testid="stForm"] {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            border: 1px solid #d1dbed !important;
            border-radius: 12px !important;
            padding: 25px !important;
            box-shadow: 0 8px 24px rgba(26, 54, 93, 0.04) !important;
        }}
        
        /* บังคับให้ตัวหนังสือที่พิมพ์ พื้นหลัง และเส้นกะพริบ Caret แสดงผลถูกต้อง */
        .stTextInput input {{
            background-color: #f4f7fc !important; 
            color: #1a365d !important; 
            caret-color: #1a365d !important; 
            border: 1px solid #cedbe7 !important;
            border-radius: 8px !important;
        }}
        
        /* 🛠️ [แก้ไขใหม่] ปรับแต่งกล่อง Selectbox ให้พื้นหลังเข้มและตัวหนังสือเป็น "สีขาว" */
        .stSelectbox div[data-baseweb="select"] {{
            background-color: #1a365d !important; /* เปลี่ยนพื้นหลังตัวกล่องหลักเป็นน้ำเงินเข้ม */
            border: 1px solid #142d52 !important;
            border-radius: 8px !important;
        }}
        
        /* บังคับให้ข้อความตัวเลือกที่โชว์ และไอคอนลูกศรในกล่องกลายเป็นสีขาวล้วน */
        .stSelectbox div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] p,
        .stSelectbox div[data-baseweb="select"] span,
        .stSelectbox div[data-baseweb="select"] svg {{
            color: #ffffff !important;
            fill: #ffffff !important;
        }}
        
        /* 🛠️ บังคับให้หน้าต่างรายการย่อย (Dropdown Popover) ตอนกดคลิกเลือก แสดงผลคลีนๆ */
        div[data-baseweb="popover"] ul {{
            background-color: #ffffff !important;
        }}
        div[data-baseweb="popover"] li[role="option"] {{
            background-color: #ffffff !important;
            color: #000000 !important; /* ชอยส์ด้านในยังคงเป็นตัวเลือกสีดำบนพื้นขาวทำให้อ่านง่าย */
        }}
        div[data-baseweb="popover"] li[role="option"]:hover {{
            background-color: #e2e8f0 !important; /* ไฮไลต์เทาอ่อนเมื่อเมาส์ชี้ */
            color: #000000 !important;
        }}
        
        /* แก้สีของข้อความคำแนะนำ (Placeholder) ในช่องพิมพ์ให้เป็นสีเทาเข้มอ่านง่าย */
        .stTextInput input::placeholder {{
            color: #718096 !important;
            opacity: 1 !important;
        }}
        
        /* เอฟเฟกต์ตอนคลิกพิมพ์ช่องคำตอบ ให้เส้นกะพริบและตัวหนังสือแสดงผลคมชัด */
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
        
        /* 🚀 บังคับให้ตัวหนังสือในปุ่มบันทึกข้อมูลเป็นสีขาวล้วน มองเห็นชัดเจน 100% */
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
        
        /* เจาะจงเปลี่ยนสีข้อความข้างในปุ่มให้เป็นสีขาว */
        .stFormSubmitButton button p,
        button[data-testid="baseButton-primary"] p {{
            color: #ffffff !important; 
        }}
        
        /* เอฟเฟกต์ตอนเมาส์ชี้ปุ่มบันทึกข้อมูล */
        .stFormSubmitButton button:hover,
        button[data-testid="baseButton-primary"]:hover {{
            background-color: #12355e !important; 
            box-shadow: 0 6px 16px rgba(18, 53, 94, 0.25) !important;
            transform: translateY(-1px);
        }}
        .stFormSubmitButton button:hover p,
        button[data-testid="baseButton-primary"]:hover p {{
            color: #ffffff !important;
        }}
        
        .responsive-h1 {{
            text-align: center; 
            color: #800000 !important; 
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
st.markdown("<h4 class='responsive-h4'>วิทยาลัยเทคนิคระยอง (Rayong Technical College / RYTC)</h4>", unsafe_allow_html=True)
st.write("---")

st.info("ประชาสัมพันธ์: ช่วงนี้อากาศเปลี่ยนแปลงบ่อย หากมีอาการไข้หรือไอ ขอความร่วมมือนักศึกษาสวมหน้ากากอนามัยก่อนเข้าใช้บริการห้องพยาบาลทุกครั้ง ขอบคุณค่ะ")

st.markdown("### กรอกข้อมูลเพื่อแจ้งความประสงค์เข้าใช้บริการ")

# 📂 จัดการฐานข้อมูลและเพิ่มหัวข้อคอลลัมน์ "โรคประจำตัว"
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
    
    # 1. กล่องรหัสนักศึกษา
    student_id = st.text_input("#รหัสนักศึกษา (11 หลัก):", placeholder="เช่น 67219010049", max_chars=11)
    
    id_is_valid = True
    if student_id.strip():
        if not student_id.strip().isdigit():
            st.error("#รหัสนักศึกษาต้องเป็นตัวเลขเท่านั้น กรุณาพิมพ์ใหม่")
            id_is_valid = False
        elif len(student_id.strip()) != 11:
            st.warning(f"ปัจจุบันกรอกไปแล้ว {len(student_id.strip())} หลัก (ต้องครบ 11 หลักพอดี)")
            id_is_valid = False

    # 2. กล่องชื่อ-นามสกุล
    student_name = st.text_input("#ชื่อ - นามสกุล:", placeholder="เช่น นายสมชาย ตั้งใจเรียน")
    
    name_is_valid = True
    if student_name.strip():
        if " " not in student_name.strip():
            st.warning("#กรุณากรอกทั้งชื่อและนามสกุล โดยเคาะเว้นวรรคตรงกลางด้วยครับ")
            name_is_valid = False

    # กล่องเขียนโรคประจำตัวด้วยตนเอง
    student_medical_condition = st.text_input("#โรคประจำตัว (ถ้าไม่มีให้เว้นว่างไว้):", placeholder="เช่น หอบหืด, ภูมิแพ้อากาศ, โรคกระเพาะ (หากไม่มีไม่ต้องกรอก)")

    # 3. เลือกแผนกวิชา
    departments = [
        "ช่างยนต์", "ช่างกลโรงงาน", "ช่างเชื่อมโลหะ", "ช่างไฟฟ้ากำลัง", 
        "ช่างอิเล็กทรอนิกส์", "ช่างก่อสร้าง", "สถาปัตยกรรม", "เทคโนโลยีสารสนเทศ (IT)", 
        "การบัญชี", "การตลาด", "การเลขานุการ", "คอมพิวเตอร์ธุรกิจ", "โลจิสติกส์"
    ]
    student_dept = st.selectbox("#แผนกวิชา / สาขางาน:", departments)
    
    # 4. ระบุอาการเบื้องต้น
    symptoms = [
        "ปวดศีรษะ / เป็นไข้", "ปวดท้อง / ท้องเสีย / ท้องอืด", 
        "ทำแผลอุบัติเหตุ / มีบาดแผล", "หน้ามืด / เป็นลม / คลื่นไส้", 
        "อาการแพ้ / ผื่นคัน / แมลงสัตว์กัดต่อย", "กล้ามเนื้ออักเสบ / เคล็ดขัดยอก", "อื่น ๆ (โปรดระบุรายละเอียดข้างล่าง)"
    ]
    selected_symptom = st.selectbox("#อาการป่วยเบื้องต้น:", symptoms)
    additional_detail = st.text_input("#รายละเอียดเพิ่มเติม (ถ้ามี):", placeholder="เช่น ปวดหัวข้างขวา, เผลอโดนมีดบาดที่นิ้วชี้")

    if selected_symptom.startswith("อื่น ๆ") and additional_detail.strip():
        final_symptom = f"อื่น ๆ: {additional_detail.strip()}"
    elif additional_detail.strip():
        final_symptom = f"{selected_symptom} ({additional_detail.strip()})"
    else:
        final_symptom = selected_symptom

    # 5. ปุ่มกดส่งข้อมูล
    submit_btn = st.form_submit_button("บันทึกข้อมูลและส่งคิวเข้าห้องพยาบาล", type="primary")

    if submit_btn:
        if not student_id.strip() or not student_name.strip():
            st.error("ไม่สามารถบันทึกได้: กรุณากรอกรหัสนักศึกษาและชื่อ-นามสกุลให้ครบถ้วนก่อนครับ")
        elif not id_is_valid:
            st.error("ไม่สามารถบันทึกได้: รหัสนักศึกษาไม่ถูกต้อง (ต้องเป็นตัวเลข 11 หลัก)")
        elif not name_is_valid:
            st.error("ไม่สามารถบันทึกได้: กรุณาใส่นามสกุลด้วยครับ")
        else:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            final_medical_condition = student_medical_condition.strip() if student_medical_condition.strip() else "-"
            
            new_record = {
                "วันที่-เวลา": current_time,
                "รหัสนักศึกษา": student_id.strip(),
                "ชื่อ-นามสกุล": student_name.strip(),
                "โรคประจำตัว": final_medical_condition,
                "แผนกวิชา": student_dept,
                "อาการเบื้องต้น": final_symptom,
                "st.info": "รอดำเนินการคัดกรอง",
                "สถานะการรักษา": "รอดำเนินการคัดกรอง",  
                "การจ่ายยา/หมายเหตุ": "-",
                "อาจารย์ผู้บันทึก": "-"  
            }
            
            df = pd.read_csv(DB_FILE)
            
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = "-"
            
            filtered_record = {k: new_record.get(k, "-") for k in COLUMNS}
            df = pd.concat([df, pd.DataFrame([filtered_record])], ignore_index=True)
            df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")
            
            # ยิงแจ้งเตือนเข้า Telegram
            tg_msg = f"รายงานคิวผู้ป่วยใหม่ (RYTC Care)\nชื่อ: {student_name.strip()}\nรหัส: {student_id.strip()}\nแผนก: {student_dept}\nโรคประจำตัว: {final_medical_condition}\nอาการ: {final_symptom}"
            send_telegram_notification(tg_msg)
            
            st.success(f"บันทึกข้อมูลของ {student_name.strip()} สำเร็จ ระบบได้ส่งคิวไปยังคุณครูพยาบาลเรียบร้อยแล้ว กรุณาพักรอเรียกชื่อสักครู่นะครับ")