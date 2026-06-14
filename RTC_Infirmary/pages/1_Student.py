import streamlit as st
import pandas as pd
import os
import base64
import requests  # 🚀 สำหรับยิงแจ้งเตือนเข้า Telegram ครูพยาบาล
from datetime import datetime

# 1. ตั้งค่าหน้าจอ (ต้องอยู่บรรทัดแรกสุดเสมอ)
st.set_page_config(page_title="RTC Infirmary", page_icon="🏥", layout="centered")

# ==========================================
# 🚀 ฝังรหัส Telegram สำเร็จรูปของอาจารย์
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
# 🎨 [แก้ไขสำเร็จ] ฟังก์ชันจัดการภาพพื้นหลังอัจฉริยะ ค้นหาเจอทุกที่ทั้งบนเครื่องและ GitHub
# ==========================================
def set_perfect_background():
    # รายการเส้นทางที่ระบบจะลองค้นหาภาพ (ทั้งใน Local และบนโครงสร้าง GitHub /RTC_Infirmary/)
    possible_paths = [
        "RTC_Infirmary/images/bg.png",  # ตำแหน่งจริงบน GitHub ของอาจารย์
        "images/bg.png",                # ตำแหน่งตอนรันในคอมพิวเตอร์ตัวเอง (Local)
        "bg.png"                        # กรณีนำภาพมาวางคู่กับตัวไฟล์โค้ดโดยตรง
    ]
    
    encoded_string = ""
    
    # วนลูปเพื่อพยายามอ่านไฟล์ภาพจากเส้นทางต่างๆ ป้องกันเว็บล่ม
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode()
                    break # เจอไฟล์แล้วให้หยุดวนลูปทันที
            except:
                pass
                
    # หากค้นหาเจอไฟล์ภาพระบบจะทำการแสดงผลพื้นหลัง CSS ทันที
    if encoded_string:
        bg_css = f"""
        <style>
        /* 1. ใส่พื้นหลังห้องพยาบาลตรงกลาง */
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                              url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        /* 2. ล็อกสีข้อความเฉพาะในส่วนเนื้อหาหลัก ไม่ให้ลามไปกวนโครงสร้างระบบปุ่มควบคุมด้านบน */
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
        
        /* 📱 3. บังคับและล็อกสีข้อความส่วนหัวให้ปรับยืดหดตามขนาดมือถืออัตโนมัติ */
        .responsive-h1 {{
            text-align: center; 
            color: #800000 !important; 
            font-family: "Sarabun", sans-serif;
            font-weight: bold; 
            margin-bottom: 0;
            font-size: calc(1.6rem + 1.2vw) !important; /* สูตรคำนวณยืดหดตามความกว้างหน้าจอ */
            line-height: 1.3 !important;
            word-wrap: break-word;
        }}
        .responsive-h4 {{
            text-align: center; 
            color: #4a5568 !important; 
            font-family: "Sarabun", sans-serif;
            margin-top: 5px; 
            margin-bottom: 20px;
            font-size: calc(1.0rem + 0.3vw) !important; /* สูตรคำนวณยืดหดตามความกว้างหน้าจอ */
            line-height: 1.4 !important;
        }}
        
        /* 🛠️ แก้ไขแถบด้านซ้าย (Sidebar) */
        [data-testid="stSidebar"] {{
            background-color: rgba(248, 249, 250, 0.95) !important;
            border-right: 1px solid #dee2e6 !important;
        }}
        [data-testid="stSidebarNavigation"] ul li div span, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebarNavigation"] a span {{
            color: #2d3748 !important; font-weight: 600 !important; font-size: 16px !important;
        }}
        
        /* ตกแต่งปุ่มลงชื่อให้เด่นและสวยงาม */
        button[data-testid="baseButton-primary"] {{
            background-color: #007bff !important; border: none !important; border-radius: 6px !important; width: 100% !important; height: 45px !important;
        }}
        button[data-testid="baseButton-primary"]:hover {{
            background-color: #0056b3 !important; box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
        }}
        
        input::-ms-reveal, input::-ms-clear {{ display: none !important; }}
        
        [data-testid="stSidebarNavigation"] ul li:first-child div span, [data-testid="stSidebarNavigation"] ul li:first-child a span {{
            visibility: hidden; position: relative;
        }}
        [data-testid="stSidebarNavigation"] ul li:first-child div span::after, [data-testid="stSidebarNavigation"] ul li:first-child a span::after {{
            content: "🏠 หน้าหลัก"; visibility: visible; position: absolute; left: 0; top: 0; white-space: nowrap; color: #2d3748 !important; 
        }}

        /* 📱 4. ดักจับหน้าจอมือถือ (กว้างไม่เกิน 768px) เพื่อจัดระเบียบตัวหนังสือทั่วไปให้หดลงมาพอดี */
        @media (max-width: 768px) {{
            [data-testid="stMainBlockContainer"] p, 
            [data-testid="stMainBlockContainer"] label, 
            [data-testid="stMainBlockContainer"] span,
            .stSelectbox label, .stTextInput label {{
                font-size: 14.5px !important; /* ย่อขนาดอักษรในช่องกรอกให้พอดีกับจอมือถือ */
            }}
            .stMarkdown h3 {{
                font-size: 18px !important; /* ย่อหัวข้อฟอร์มกรอกข้อมูล */
            }}
        }}
        </style>
        """
        st.markdown(bg_css, unsafe_allow_html=True)

# เรียกใช้ฟังก์ชันเซ็ตอัพพื้นหลังแบบอัจฉริยะ (ไม่ต้องใส่ path ในวงเล็บแล้วครับ)
set_perfect_background()

# ==========================================
# 🏛️ หัวข้อหน้าเว็บแบบ Responsive (ดึงคลาส CSS มาใช้งาน)
# ==========================================
st.markdown("<h1 class='responsive-h1'>🏥 ระบบลงทะเบียนผู้เข้ารับบริการห้องพยาบาล</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='responsive-h4'>วิทยาลัยเทคนิคระยอง (Rayong Technical College)</h4>", unsafe_allow_html=True)
st.write("---")

# 📢 กล่องประกาศข่าวสารจากห้องพยาบาล (Live Notice Board)
st.info("📢 **ประชาสัมพันธ์:** ช่วงนี้อากาศเปลี่ยนแปลงบ่อย หากมีอาการไข้หรือไอ ขอความร่วมมือนักศึกษาสวมหน้ากากอนามัยก่อนเข้าใช้บริการห้องพยาบาลทุกครั้ง ขอบคุณค่ะ 😷")

st.markdown("### 📝 กรอกข้อมูลเพื่อแจ้งความประสงค์เข้าใช้บริการ")

# เตรียมไฟล์ข้อมูล และล็อกโครงสร้างคอลัมน์ให้สมบูรณ์
DB_FILE = "infirmary_records.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["วันที่-เวลา", "รหัสนักศึกษา", "ชื่อ-นามสกุล", "แผนกวิชา", "อาการเบื้องต้น", "สถานะการรักษา", "การจ่ายยา/หมายเหตุ", "อาจารย์ผู้บันทึก"]).to_csv(DB_FILE, index=False, encoding="utf-8-sig")

# 📥 สร้างฟอร์มรับข้อมูลนักเรียน
with st.form(key="student_form", clear_on_submit=True):
    
    # 1. กล่องรหัสนักศึกษา + ระบบตรวจสอบตัวเลข 11 หลัก
    student_id = st.text_input("📌 รหัสนักศึกษา (11 หลัก):", placeholder="เช่น 67219010049", max_chars=11)
    
    # เช็กเงื่อนไขรหัสนักศึกษา
    id_is_valid = True
    if student_id.strip():
        if not student_id.strip().isdigit():
            st.error("❌ รหัสนักศึกษาต้องเป็น 'ตัวเลขเท่านั้น' กรุณาพิมพ์ใหม่")
            id_is_valid = False
        elif len(student_id.strip()) != 11:
            st.warning(f"⚠️ ปัจจุบันกรอกไปแล้ว {len(student_id.strip())} หลัก (ต้องครบ 11 หลักพอดี)")
            id_is_valid = False

    # 2. กล่องชื่อ-นามสกุล + เช็กการเว้นวรรค
    student_name = st.text_input("👤 ชื่อ - นามสกุล:", placeholder="เช่น นายสมชาย ตั้งใจเรียน")
    
    name_is_valid = True
    if student_name.strip():
        if " " not in student_name.strip():
            st.warning("⚠️ กรุณากรอกทั้ง 'ชื่อ' และ 'นามสกุล' โดยเคาะเว้นวรรคตรงกลางด้วยครับ")
            name_is_valid = False

    # 3. เลือกแผนกวิชา
    departments = [
        "ช่างยนต์", "ช่างกลโรงงาน", "ช่างเชื่อมโลหะ", "ช่างไฟฟ้ากำลัง", 
        "ช่างอิเล็กทรอนิกส์", "ช่างก่อสร้าง", "สถาปัตยกรรม", "เทคโนโลยีสารสนเทศ (IT)", 
        "การบัญชี", "การตลาด", "การเลขานุการ", "คอมพิวเตอร์ธุรกิจ", "โลจิสติกส์"
    ]
    student_dept = st.selectbox("🏬 แผนกวิชา / สาขางาน:", departments)
    
    # 4. ระบุอาการเบื้องต้น
    symptoms = [
        "ปวดศีรษะ / เป็นไข้", "ปวดท้อง / ท้องเสีย / ท้องอืด", 
        "ทำแผลอุบัติเหตุ / มีบาดแผล", "หน้ามืด / เป็นลม / คลื่นไส้", 
        "อาการแพ้ / ผื่นคัน / แมลงสัตว์กัดต่อย", "กล้ามเนื้ออักเสบ / เคล็ดขัดยอก", "อื่น ๆ (โปรดระบุรายละเอียดข้างล่าง)"
    ]
    selected_symptom = st.selectbox("🩺 อาการป่วยเบื้องต้น:", symptoms)
    additional_detail = st.text_input("✍️ รายละเอียดเพิ่มเติม (ถ้ามี):", placeholder="เช่น ปวดหัวข้างขวา, เผลอโดนมีดบาดที่นิ้วชี้")

    # ประกอบอาการป่วยที่จะบันทึก
    if selected_symptom.startswith("อื่น ๆ") and additional_detail.strip():
        final_symptom = f"อื่น ๆ: {additional_detail.strip()}"
    elif additional_detail.strip():
        final_symptom = f"{selected_symptom} ({additional_detail.strip()})"
    else:
        final_symptom = selected_symptom

    # 5. ปุ่มกดส่งข้อมูล
    submit_btn = st.form_submit_button("🚀 บันทึกข้อมูลและส่งคิวเข้าห้องพยาบาล", type="primary")

    if submit_btn:
        if not student_id.strip() or not student_name.strip():
            st.error("❌ 不กสามารถบันทึกได้: กรุณากรอกรหัสนักศึกษาและชื่อ-นามสกุลให้ครบถ้วนก่อนครับ")
        elif not id_is_valid:
            st.error("❌ ไม่สามารถบันทึกได้: รหัสนักศึกษาไม่ถูกต้อง (ต้องเป็นตัวเลข 11 หลัก)")
        elif not name_is_valid:
            st.error("❌ ไม่สามารถบันทึกได้: กรุณาใส่นามสกุลด้วยครับ")
        else:
            # ผ่านทุกเงื่อนไข บันทึกลง CSV
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_record = {
                "วันที่-เวลา": current_time,
                "รหัสนักศึกษา": student_id.strip(),
                "ชื่อ-นามสกุล": student_name.strip(),
                "แผนกวิชา": student_dept,
                "อาการเบื้องต้น": final_symptom,
                "สถานะการรักษา": "⏳ กำลังรอเจ้าหน้าที่ตรวจ",  # 🛠️ [แก้ไขจุดพังสำเร็จ] เอาตัวอักษรจีน '暗' ออกแล้ว
                "การจ่ายยา/หมายเหตุ": "-",
                "อาจารย์ผู้บันทึก": "-"  # 🛠️ [แก้ไขจุดพังสำเร็จ] เพิ่มคอลัมน์ให้โครงสร้างตรงกับหน้าแอดมินหลังบ้าน
            }
            
            df = pd.read_csv(DB_FILE)
            
            # ตรวจสอบความชัวร์ว่าคอลัมน์ใน DataFrame ปัจจุบันมีครบตามโครงสร้างไหม ป้องกันการ Error
            if "อาจารย์ผู้บันทึก" not in df.columns:
                df["อาจารย์ผู้บันทึก"] = "-"
                
            df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
            df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")
            
            # 🔔 ยิงแจ้งเตือนเข้า Telegram ครูพยาบาลทันทีเมื่อเด็กกดส่งคิว
            tg_msg = f"🔔 *มีคิวผู้ป่วยใหม่ (RTC Care)*\n👤 *ชื่อ:* {student_name.strip()}\n🆔 *รหัส:* {student_id.strip()}\n🏬 *แผนก:* {student_dept}\n🤒 *อาการ:* {final_symptom}"
            send_telegram_notification(tg_msg)
            
            st.success(f"🎯 บันทึกข้อมูลของ {student_name.strip()} สำเร็จ! ระบบได้ส่งคิวไปยังคุณครูพยาบาลเรียบร้อยแล้ว นอนพักรอเรียกชื่อสักครู่นะครับ")
            st.balloons()