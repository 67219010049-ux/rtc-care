import streamlit as st
import base64
import os  # 🛠️ เพิ่มโมดูลจัดการเส้นทางไฟล์
import streamlit.components.v1 as components

# 1. ตั้งค่าหน้าจอ (ปิดแถบข้างไม่ให้เด้งเปิดตอนเข้าเว็บด้วย initial_sidebar_state="collapsed")
st.set_page_config(
    page_title="RYTC Infirmary - Home", 
    page_icon="🏥", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 🎨 ฟังก์ชันจัดการภาพพื้นหลัง และแถบสถานะด้านบน
# ==========================================
def set_perfect_background(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        bg_css = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@300;400;500;600;700&display=swap');

        /* 🎯 การคุม Font */
        .responsive-h1, .responsive-h4, p, label, 
        [data-testid="stMarkdown"] p, 
        [data-testid="stSidebar"] p,
        [data-testid="stSidebarNavigation"] a span {{
            font-family: 'IBM Plex Sans Thai', sans-serif !important;
        }}
        
        /* 1. สีแถบบนสุด (Header Bar) */
        header[data-testid="stHeader"], 
        .stHeader,
        div[data-testid="stAppHeader"],
        header {{
            background-color: #001f3f !important;
            border-bottom: 2px solid #001122 !important;
        }}
        header[data-testid="stHeader"] button, 
        header[data-testid="stHeader"] svg,
        div[data-testid="stAppHeader"] svg,
        header button,
        header svg,
        header span,
        header a {{
            fill: #ffffff !important;
            color: #ffffff !important;
        }}
        
        /* 2. ภาพพื้นหลัง */
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                              url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        /* 📱 3. สีข้อความส่วนหัว */
        .responsive-h1 {{
            text-align: center; 
            color: #001f3f !important;
            font-weight: bold; 
            margin-bottom: 0;
            font-size: calc(1.6rem + 1.2vw) !important;
            line-height: 1.3 !important;
            word-wrap: break-word;
        }}
        .responsive-h4 {{
            text-align: center; 
            color: #4a5568 !important; 
            margin-top: 5px; 
            margin-bottom: 20px;
            font-size: calc(1.0rem + 0.3vw) !important;
            line-height: 1.4 !important;
        }}
        
        /* 🛠️ สี Sidebar */
        [data-testid="stSidebar"] {{
            background-color: rgba(248, 249, 250, 0.95) !important;
            border-right: 1px solid #dee2e6 !important;
        }}
        [data-testid="stSidebarNavigation"] ul li div span, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span, 
        [data-testid="stSidebar"] label,
        [data-testid="stSidebarNavigation"] a span {{
            color: #2d3748 !important; 
            font-weight: 600 !important;
            font-size: 16px !important;
        }}

        /* 🔘 ปรับสไตล์ st.page_link (เปลี่ยนเป็นพื้นสีขาว Hover เป็นสีน้ำเงินกรม) */
        [data-testid="stPageLink-NavLink"] {{
            background-color: #ffffff !important;
            color: #001f3f !important;
            border-radius: 10px !important;
            padding: 12px 20px !important;
            text-align: center !important;
            font-size: 17px !important;
            font-weight: 600 !important;
            border: 2px solid #001f3f !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.25s ease-in-out !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }}

        [data-testid="stPageLink-NavLink"] p {{
            color: #001f3f !important;
            font-size: 17px !important;
            font-weight: 600 !important;
            margin: 0 !important;
            transition: color 0.25s ease-in-out !important;
        }}

        [data-testid="stPageLink-NavLink"]:hover {{
            background-color: #001f3f !important;
            border-color: #001f3f !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 12px rgba(0, 31, 63, 0.25) !important;
        }}

        [data-testid="stPageLink-NavLink"]:hover p {{
            color: #ffffff !important;
        }}
        </style>
        """
        st.markdown(bg_css, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ ไม่พบไฟล์ภาพพื้นหลังในโฟลเดอร์ กรุณาตรวจสอบว่ามีไฟล์ images/bg.jpg อยู่จริงในโปรเจกต์")

# 🛠️ คำนวณตำแหน่งโฟลเดอร์ให้แม่นยำ
current_dir = os.path.dirname(os.path.abspath(__file__))
bg_image_path = os.path.join(current_dir, "images", "bg.jpg")

# เรียกใช้งานภาพพื้นหลังด้วย Path ที่มีความปลอดภัยสูง
set_perfect_background(bg_image_path)

# ==========================================
# 🏛️ ส่วนหัวของเว็บ
# ==========================================
st.markdown("<h1 class='responsive-h1'>ระบบบริหารจัดการงานสถานพยาบาลและอนามัย</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='responsive-h4'>วิทยาลัยเทคนิคระยอง (Rayong Technical College)</h4>", unsafe_allow_html=True)
st.write("---")

# ==========================================
# 🔘 ปุ่มเชื่อมโยงไปยังไฟล์ .py (วางอยู่เหนือส่วนบริการ)
# ==========================================
col1, col2 = st.columns(2)

with col1:
    # 💡 แก้ไข path ไฟล์ .py ปลายทางตรงนี้ตามชื่อไฟล์จริงของคุณในโฟลเดอร์ pages/
    st.page_link(
        "pages/1_Student.py", 
        label="ลงชื่อเข้าใช้บริการ (นักเรียน)", 
        use_container_width=True
    )

with col2:
    # 💡 แก้ไข path ไฟล์ .py ปลายทางตรงนี้ตามชื่อไฟล์จริงของคุณในโฟลเดอร์ pages/
    st.page_link(
        "pages/2_Admin.py", 
        label="ลงชื่อเข้าใช้ระบบ (แอดมิน)", 
        use_container_width=True
    )

st.write("") 

# ==========================================
# 📦 กล่องข้อความ HTML Component
# ==========================================
html_display = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'IBM Plex Sans Thai', sans-serif;
            margin: 0;
            padding: 5px;
            background: transparent;
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }
        .col-left {
            flex: 1.6;
            min-width: 280px;
        }
        .col-right {
            flex: 1;
            min-width: 280px;
        }
        .card-service {
            background-color: rgba(255, 255, 255, 0.96);
            padding: 20px;
            border-radius: 12px;
            border-left: 6px solid #001f3f;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 15px;
        }
        .card-service h3 {
            margin-top: 0;
            color: #001f3f !important;
            font-size: 19px;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .card-service p {
            color: #2d3748 !important;
            font-size: 15.5px;
            line-height: 1.6;
            margin: 0;
        }
        .box-accordion {
            background-color: rgba(255, 255, 255, 0.96);
            border: 1px solid #ced4da;
            border-radius: 8px;
            margin-bottom: 12px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        }
        .box-accordion summary {
            padding: 12px 18px;
            background-color: #f8f9fa;
            color: #001f3f !important;
            font-weight: 600;
            font-size: 16px;
            cursor: pointer;
            outline: none;
            user-select: none;
        }
        .box-accordion summary:hover {
            background-color: #edf2f7;
        }
        .inner-content {
            padding: 15px 18px;
            background-color: #ffffff;
            border-top: 1px solid #edf2f7;
            color: #4a5568 !important;
            font-size: 15px;
            line-height: 1.6;
        }
        .card-announcement {
            background-color: rgba(255, 255, 255, 0.96);
            padding: 20px;
            border-left: 6px solid #800000;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .card-announcement h3 {
            margin-top: 0;
            color: #800000 !important;
            font-size: 19px;
            font-weight: 700;
            margin-bottom: 15px;
        }
        .card-announcement p {
            color: #2d3748 !important;
            font-size: 15.5px;
            margin: 0 0 10px 0;
        }
        .box-emergency {
            color: #ff0000 !important;
            font-size: 16.5px;
            font-weight: 700;
            line-height: 1.5;
            text-align: center;
            background-color: #fff5f5;
            padding: 12px;
            border-radius: 8px;
            border: 1px dashed #ff0000;
            margin-top: 15px;
        }
    </style>
</head>
<body>

    <div class="col-left">
        <div class="card-service">
            <h3>บริการอิเล็กทรอนิกส์สำหรับนักศึกษาและบุคลากร</h3>
            <p>
                ระบบนี้จัดทำขึ้นเพื่อช่วยอำนวยความสะดวกในการจัดเก็บข้อมูลการเข้ารับบริการทางการแพทย์ภายในสถานศึกษาอย่างเป็นระบบและปลอดภัย 
                โปรดเลือกเมนูการทำงานที่แถบควบคุมด้านซ้ายมือเพื่อดำเนินการต่อครับ
            </p>
        </div>

        <details class="box-accordion">
            <summary>สำหรับนักเรียน นักศึกษา (Student Service)</summary>
            <div class="inner-content">
                ใช้สำหรับลงทะเบียน แจ้งอาการป่วย หรืออุบัติเหตุจากการเรียนและการฝึกปฏิบัติงาน เพื่อขอเข้ารับการรักษาพยาบาลเบื้องต้นภายในสถานพยาบาลวิทยาลัย
            </div>
        </details>

        <details class="box-accordion">
            <summary>สำหรับเจ้าหน้าที่และอาจารย์พยาบาล (Administrative Control)</summary>
            <div class="inner-content">
                ส่วนควบคุมสำหรับเจ้าหน้าที่ผู้มีส่วนเกี่ยวข้องในการคัดกรอง วินิจฉัย สั่งการรักษา และจ่ายเวชภัณฑ์ โดยมีระบบรักษาความปลอดภัยของข้อมูลที่เป็นไปตามมาตรฐาน
            </div>
        </details>
    </div>

    <div class="col-right">
        <div class="card-announcement">
            <h3>ประกาศและเวลาทำการ</h3>
            <p><b>วันทำการ:</b> จันทร์ - ศุกร์</p>
            <p><b>เวลาทำการ:</b> 08:30 น. - 16:30 น.</p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;">
            <div class="box-emergency">
                กรณีอุบัติเหตุรุนแรงหรือฉุกเฉิน<br>กรุณาติดต่อเจ้าหน้าที่โดยตรงทันที เบอร์ 080-445-6012
            </div>
        </div>
    </div>

</body>
</html>
"""

components.html(html_display, height=520, scrolling=True)