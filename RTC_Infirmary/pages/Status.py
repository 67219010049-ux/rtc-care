import streamlit as st
import pandas as pd
import os
import base64

# 1. ตั้งค่าหน้าจอ (ต้องอยู่บรรทัดแรกสุดเสมอ)
st.set_page_config(page_title="RYTC Queue Status", page_icon="📋", layout="centered")

# ==========================================
# ฟังก์ชันจัดการภาพพื้นหลังอัจฉริยะ + บังคับใช้ฟอนต์ IBM Plex Sans Thai 100% (ดึงมาจากหน้า Student)
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
        /* ✅ เจาะจงเฉพาะองค์ประกอบข้อความ และเว้นวรรคไม่ให้ทับคลาสไอคอน */
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
        span[data-testid="stIcon"],
        span[data-testid="stSidebarPageLinkChevron"] {{
            font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
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

        /* การตกแต่งสไตล์สำหรับรายการคิว */
        .queue-container {{
            background: #ffffff;
            border-radius: 12px;
            padding: 18px;
            margin-top: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            border: none;
        }}
        .status-badge-pending {{
            background-color: #fef3c7 !important;
            color: #d97706 !important;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 13px;
            display: inline-block;
        }}
        .status-badge-process {{
            background-color: #dbeafe !important;
            color: #2563eb !important;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 13px;
            display: inline-block;
        }}
        .status-badge-done {{
            background-color: #d1fae5 !important;
            color: #059669 !important;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 13px;
            display: inline-block;
        }}
        </style>
        """
        st.markdown(bg_css, unsafe_allow_html=True)

set_perfect_background()

# ==========================================
# หัวข้อหน้าเว็บแบบ Responsive (ถอดแบบดีไซน์จากหน้า Student)
# ==========================================
st.markdown("<h1 class='responsive-h1'>ตารางสถานะคิวล่าสุด</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='responsive-h4'>วิทยาลัยเทคนิคระยอง (Rayong Technical College)</h4>", unsafe_allow_html=True)
st.write("---")

st.info(" ประชาสัมพันธ์ซข้อมูลในหน้านี้จะทำการอัปเดตสถานะล่าสุดให้ท่านโดยอัตโนมัติในทุก ๆ 10 วินาที")

DB_FILE = "infirmary_records.csv"

# ใช้ Streamlit Fragment ในการรีเฟรชตารางแบบ Real-time
@st.fragment(run_every="10s")
def show_live_queues():
    try:
        if os.path.exists(DB_FILE):
            df_queue = pd.read_csv(DB_FILE)
            if not df_queue.empty:
                # แสดงคิวล่าสุด 10 อันดับแรก โดยเอาคิวใหม่ไว้บนสุด
                recent_queues = df_queue.tail(10).iloc[::-1] 
                
                for index, row in recent_queues.iterrows():
                    status_text = str(row["สถานะการรักษา"]).strip()
                    
                    # ตรวจสอบสถานะการรักษาเพื่อแสดงผลป้าย Badge
                    if status_text in ["รอดำเนินการคัดกรอง", "รอดำเนินการ", "-", "กำลังรอเจ้าหน้าที่คัดกรอง", ""]:
                        badge_html = f'<span class="status-badge-pending">⏳ รอดำเนินการ</span>'
                    elif status_text in ["กำลังรักษา", "อยู่ระหว่างรับบริการ", "ให้นอนพักฟื้นที่ห้องพยาบาล", "นอนพักฟื้น"]:
                        badge_html = f'<span class="status-badge-process">🩺 กำลังรักษา</span>'
                    else:
                        badge_html = f'<span class="status-badge-done">✅ เสร็จสิ้น</span>'
                        
                    name_parts = str(row["ชื่อ-นามสกุล"]).strip().split(" ")
                    if len(name_parts) >= 2:
                        masked_name = f"{name_parts[0]} {name_parts[1][0]}..." 
                    else:
                        masked_name = name_parts[0][:5] + "..." if len(name_parts[0]) > 5 else name_parts[0]
                    
                    st.markdown(f"""
                    <div class="queue-container">
                        <table style="width:100%; border:none; border-collapse:collapse; background: transparent;">
                            <tr style="background: transparent;">
                                <td style="width:70%; border:none; vertical-align:middle; background: transparent; padding: 0;">
                                    <strong style="font-size:16px; color:#001f3f;">👤 {masked_name}</strong><br>
                                    <span style="font-size:13px; color:#64748b;"> {row["แผนกวิชา"]} | อาการ: {row["อาการเบื้องต้น"]}</span>
                                </td>
                                <td style="width:30%; text-align:right; border:none; vertical-align:middle; background: transparent; padding: 0;">
                                    {badge_html}
                                </td>
                            </tr>
                        </table>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("🎉 ขณะนี้ไม่มีคิวผู้เข้ารับบริการในระบบ")
        else:
            st.caption("🎉 ขณะนี้ไม่มีคิวผู้เข้ารับบริการในระบบ")
    except Exception as e:
        st.caption("ไม่สามารถโหลดข้อมูลคิวได้ในขณะนี้")

# เรียกทำงานฟังก์ชันแสดงผลคิว
show_live_queues()