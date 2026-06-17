import streamlit as st
import os
import random
import string
import base64
from PIL import Image
# ==========================================
# 1. CẤU HÌNH TRANG & KHỞI TẠO TRẠNG THÁI
# ==========================================
icon_image = Image.open("favicon.png") 

st.set_page_config(
    page_title="Trang chủ | Prudential Việt Nam", 
    page_icon=icon_image,  
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Khởi tạo các biến session_state
if 'page' not in st.session_state:
    st.session_state.page = 'about'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'captcha_code' not in st.session_state:
    st.session_state.captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
# ==========================================
# 2. CSS TÙY CHỈNH (TOÀN CỤC)
# ==========================================
st.markdown("""
    <style>
    /* Ẩn các thành phần mặc định của Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    
    /* Font và màu sắc chủ đạo */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Đường kẻ đỏ thương hiệu */
    .red-line {
        height: 4px;
        background-color: #ed1b2e;
        width: 100%;
        margin: 10px 0 25px 0;
    }
    
    /* Tùy chỉnh nút Primary */
    div.stButton > button:first-child, .st-emotion-cache-19rxjzo {
        background-color: #ed1b2e;
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #c91626 !important;
        color: white !important;
        border: none;
    }
    
    /* Tùy chỉnh CSS cho Dashboard Sidebar */
    .profile-box {
        border: 1px solid #eee;
        border-radius: 8px;
        padding: 25px;
        text-align: center;
        background-color: #fcfcfc;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .profile-icon {
        font-size: 48px;
        color: #ed1b2e;
        margin-bottom: 10px;
    }
    .profile-name {
        font-size: 20px;
        font-weight: 700;
        color: #333;
    }
    .profile-title {
        font-size: 14px;
        color: #666;
        margin-top: 5px;
    }
    
    .menu-box {
        border: 1px solid #eee;
        border-radius: 8px;
        padding: 15px;
        background-color: #fff;
    }
    .menu-title {
        font-size: 16px;
        font-weight: 700;
        text-transform: uppercase;
        color: #888;
        margin-bottom: 15px;
        padding-left: 10px;
        border-left: 3px solid #ed1b2e;
    }
    .menu-item {
        padding: 12px 15px;
        border-radius: 6px;
        color: #444;
        cursor: pointer;
        transition: background 0.2s;
        display: flex;
        align-items: center;
        gap: 12px;
        text-decoration: none;
        margin-bottom: 5px;
    }
    .menu-item:hover {
        background-color: #fff1f2;
        color: #ed1b2e;
    }
    
    /* Banner CTA Đỏ */
    .cta-banner {
        background-color: #ed1b2e;
        color: white;
        padding: 40px;
        border-radius: 0;
        text-align: center;
        margin: 40px -100px;
    }
    
    /* Footer pháp lý */
    .legal-footer {
        font-size: 12px;
        color: #777;
        margin-top: 50px;
        padding: 20px 0;
        border-top: 1px solid #eee;
    }
    
    /* Popover Styling */
    .stPopover > button {
        border: 1px solid #ddd !important;
        background-color: white !important;
        color: #333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HÀM TIỆN ÍCH
# ==========================================
def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

def safe_image(path, width=None, use_container_width=True, caption=None):
    try:
        # Đọc trực tiếp file ảnh từ máy tính
        if os.path.exists(path):
            if width:
                st.image(path, width=width, use_container_width=False)
            else:
                st.image(path, use_container_width=use_container_width)
        else:
            raise FileNotFoundError
    except:
        # Nếu không tìm thấy file ảnh, sẽ hiển thị cái này để thay thế tạm
        if "logo.png" in path:
            st.markdown('<h2 style="color: #ed1b2e; font-weight: 900; margin: 0; font-family: sans-serif;">PRUDENTIAL</h2>', unsafe_allow_html=True)
        else:
            st.warning(f"Chưa tìm thấy file ảnh: {path}")

# ==========================================
# 4. HEADER TỔNG (Xuyên suốt)
# ==========================================
header_container = st.container()
with header_container:
    if not st.session_state.logged_in:
        # Header Chưa đăng nhập
        c1, c2, c3 = st.columns([3, 5, 2])
        with c1:
            safe_image("logo.png", width=250)
        with c3:
                st.write("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                
                if st.session_state.page == 'login_employee':
                    if 'temp_vai_tro' not in st.session_state:
                        st.session_state.temp_vai_tro = None
                    st.session_state.temp_vai_tro = st.selectbox(
                        "Chọn vai trò", 
                        options=["Nhân viên Dịch vụ khách hàng", "Nhân viên Xử lí khiếu nại", "Nhân viên Xử lí bồi thường"],
                        index=None,
                        placeholder="Chọn vai trò",
                        label_visibility="collapsed"
                    )
                elif st.session_state.page not in ['login_customer', 'forgot_password']:
                    with st.popover("👤 Đăng nhập", use_container_width=True):
                        if st.button("Đối với Khách Hàng", use_container_width=True):
                            st.session_state.captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                            navigate_to('login_customer')
                        if st.button("Đối với Nhân Viên", use_container_width=True):
                            st.session_state.captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                            navigate_to('login_employee')
        
        m1, m2, m_empty = st.columns([1.5, 1.5, 7])
        with m1:
            if st.button("Về chúng tôi", use_container_width=True, type="secondary" if st.session_state.page != 'about' else "primary"):
                navigate_to('about')
        with m2:
            if st.button("Dịch vụ", use_container_width=True, type="secondary" if st.session_state.page != 'services' else "primary"):
                navigate_to('services')
    else:
        # Header Đã đăng nhập
        c1, c2, c3 = st.columns([2.5, 4, 3.5])
        with c1:
            safe_image("logo.png", width=220)
        with c3:
            st.write("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            
            # --- CSS biến nút trên Header thành chữ link tàng hình ---
            st.markdown("""
                <style>
                div[data-testid="stVerticalBlock"] div:has(button[title="header-profile"]) button {
                    background: transparent !important; border: none !important; color: #333 !important;
                    font-size: 14px !important; box-shadow: none !important; justify-content: flex-end !important;
                    padding: 0 !important; font-weight: normal !important; height: auto !important; min-height: auto !important; margin-top: 2px !important;
                }
                div[data-testid="stVerticalBlock"] div:has(button[title="header-profile"]) button:hover {
                    color: #ed1b2e !important; text-decoration: underline !important;
                }
                </style>
            """, unsafe_allow_html=True)
            
            cols = st.columns([3, 3, 1])
            if st.session_state.role == 'customer':
                with cols[0]:
                    if st.button("Thông tin cá nhân", key="head_prof_cus", help="header-profile", use_container_width=True):
                        st.session_state.dashboard_tab = 'profile'
                        st.session_state.action_mode = 'view'
                        st.rerun()
                with cols[1]:
                    # Biến Hợp đồng bảo hiểm thành nút bấm cho Khách hàng
                    if st.button("Hợp đồng bảo hiểm", key="head_hd_cus", help="header-profile", use_container_width=True):
                        st.session_state.dashboard_tab = 'cus_hopdong'
                        st.session_state.action_mode = 'view_ds_hd'
                        st.rerun()
            else:
                with cols[1]:
                    if st.button("Thông tin cá nhân", key="head_prof_emp", help="header-profile", use_container_width=True):
                        st.session_state.dashboard_tab = 'profile'
                        st.session_state.action_mode = 'view'
                        st.rerun()
            
            with cols[2]:
                st.markdown("""
    <style>
    /* Ép cột chứa nút chuông phải nhảy lên */
    div[data-testid="column"]:has(button[title="header-bell"]) {
        position: relative !important;
        top: -10px !important; /* Thử thay đổi số -10 thành -12, -15 để thấy nó nhích lên */
    }

    /* Ép nút chuông bên trong */
    button[title="header-bell"] {
        background-color: #ffffff !important; 
        border: 1px solid #ddd !important;
        box-shadow: none !important;
        width: 42px !important;
        height: 42px !important;
        font-size: 20px !important;
        padding: 0 !important;
        border-radius: 8px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    button[title="header-bell"]:hover {
        background-color: #f9f9f9 !important;
        border-color: #ed1b2e !important;
    }
    </style>
""", unsafe_allow_html=True)
                
                # Thêm help="header-bell" để CSS nhận diện
                if st.button("🔔", key="btn_chuong_header", help="header-bell"):
                    st.session_state.dashboard_tab = 'thong_bao'
                    st.rerun()
            
st.markdown('<div class="red-line"></div>', unsafe_allow_html=True)
# ==========================================
# 5. ĐIỀU HƯỚNG TRANG (SPA Logic)
# ==========================================

# ------------------------------------------
# TRANG 'ABOUT'
# ------------------------------------------
if st.session_state.page == 'about' and not st.session_state.logged_in:
    # 1. Hero Section (Phần đầu trang có nền xám)
    about_img_base64 = ""
    if os.path.exists("about.jpg"):
        with open("about.jpg", "rb") as img_file:
            about_img_base64 = base64.b64encode(img_file.read()).decode()
            
    about_img_tag = f'<img src="data:image/jpeg;base64,{about_img_base64}" style="width: 100%; height: auto; border-radius: 8px; display: block;" alt="Prudential Việt Nam">' if about_img_base64 else ""

    st.markdown(f"""<div style="background-color: #eef0f2; border-radius: 12px; padding: 45px; display: flex; align-items: center; justify-content: space-between; gap: 40px;">
<div style="flex: 1.2;">
<h2 style="color: #111; font-weight: 800; font-size: 42px; margin-top: 0; margin-bottom: 25px;">Prudential Việt Nam</h2>
<p style="font-size: 20px; line-height: 1.6; color: #333; margin: 0;">
Prudential Việt Nam tự hào là thành viên của Tập đoàn Prudential, tập đoàn tài chính hàng đầu thế giới được thành lập từ năm 1848, có trụ sở chính tại Vương quốc Anh với bề dày lịch sử kinh doanh, phát triển bền vững, cam kết đầu tư lâu dài, an toàn và hiệu quả.
</p>
</div>
<div style="flex: 1;">
{about_img_tag}
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<hr style='margin: 40px 0; border: none; border-top: 1px solid #eee;'>", unsafe_allow_html=True)

    # 2. Về tập đoàn Prudential
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown("<h3 style='color: #222; font-weight: 400; font-size: 36px; margin-bottom: 20px;'>Về tập đoàn <span style='font-weight: 700;'>Prudential</span></h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 18px; color: #333; line-height: 1.6;'>Thành lập năm 1848 tại Luân Đôn, Tập đoàn Prudential là một trong những tập đoàn tài chính hàng đầu thế giới cung cấp các giải pháp bảo hiểm nhân thọ, sức khỏe và quản lý tài sản tại 24 thị trường trên khắp Châu Á và Châu Phi.</p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#ed1b2e; font-weight:bold; cursor:pointer; font-size: 16px; margin-top: 15px;'>Xem thêm →</p>", unsafe_allow_html=True)
    with c2:
        safe_image("about1.jpg")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3. Thành tích và giải thưởng
    c3, c4 = st.columns([1, 1], gap="large")
    with c3:
        safe_image("about3.jpg")
    with c4:
        st.markdown("<h3 style='color: #222; font-weight: 400; font-size: 36px; margin-bottom: 20px;'>Thành tích và <span style='font-weight: 700;'>Giải thưởng</span></h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 18px; color: #333; line-height: 1.6;'>Với những nỗ lực và đóng góp tích cực tại Việt Nam, Prudential vinh dự được trao tặng nhiều giải thưởng và danh hiệu cao quý.</p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#ed1b2e; font-weight:bold; cursor:pointer; font-size: 16px; margin-top: 15px;'>Xem thêm →</p>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 4. CTA Banner (Khối liên hệ đỏ ở cuối trang)
    img_base64 = ""
    if os.path.exists("about2.jpg"):
        with open("about2.jpg", "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
            
    img_tag = f'<img src="data:image/jpeg;base64,{img_base64}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 4px; display: block;" alt="Tòa nhà Prudential">' if img_base64 else ""

    st.markdown(f"""<div style="background-color: #cb333b; border-radius: 8px; padding: 35px; display: flex; align-items: stretch; justify-content: space-between; gap: 40px;">
<div style="flex: 1.2; display: flex; flex-direction: column; justify-content: center;">
<h3 style="color: white; margin-top: 0; margin-bottom: 10px; font-weight: 400; font-size: 32px;">Bạn cần <span style="font-weight: 700;">tư vấn thêm thông tin?</span></h3>
<p style="color: white; font-size: 18px; margin-bottom: 35px; opacity: 0.9;">Liên hệ với chúng tôi tại:</p>
<div style="display: flex; align-items: center; margin-bottom: 30px;">
<div style="background: white; border-radius: 50%; min-width: 44px; height: 44px; display: flex; justify-content: center; align-items: center; margin-right: 20px;">
<span style="color: #cb333b; font-size: 22px;">📍</span>
</div>
<div>
<h4 style="color: white; margin: 0; font-size: 18px; font-weight: bold; text-transform: uppercase;">Trụ sở</h4>
<p style="color: white; margin: 0; font-size: 16px; opacity: 0.9;">Số 123, đường ABC, Quận D, TP HCM</p>
</div>
</div>
<div style="display: flex; align-items: center;">
<div style="background: white; border-radius: 50%; min-width: 44px; height: 44px; display: flex; justify-content: center; align-items: center; margin-right: 20px;">
<span style="color: #cb333b; font-size: 22px;">📞</span>
</div>
<div>
<h4 style="color: white; margin: 0; font-size: 18px; font-weight: bold; text-transform: uppercase;">Số điện thoại</h4>
<p style="color: white; margin: 0; font-size: 16px; opacity: 0.9;">(012).345.6789</p>
</div>
</div>
</div>
<div style="flex: 1;">
{img_tag}
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 5. Footer Pháp lý
    st.markdown("""
        <div class="legal-footer">
            <p>Công ty TNHH Bảo hiểm nhân thọ Prudential Việt Nam ("Prudential") được thành lập và hoạt động theo Giấy phép số 15 GP/KDBH cấp lại ngày 08/09/2011 và các giấy phép điều chỉnh mới nhất năm 2024.<br>
            <b>Người đại diện:</b> Ông Kevin Joong Kwon – Tổng Giám đốc.<br>
            <b>Lĩnh vực:</b> Bảo hiểm nhân thọ (trọn đời, tử kỳ, hỗn hợp...) và đầu tư tài chính.</p>
        </div>
    """, unsafe_allow_html=True)

# ------------------------------------------
# TRANG 'SERVICES' 
# ------------------------------------------
elif st.session_state.page == 'services' and not st.session_state.logged_in:
    st.markdown("<h2 style='color: #222; margin-bottom: 25px; font-weight: 400;'>Chúng tôi <span style='font-weight: 800;'>giúp gì cho bạn?</span></h2>", unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3, gap="medium")
    
    with p1:
        with st.container(border=True): # Dùng container tạo viền xám xung quanh thẻ
            safe_image("s1.jpg")
            st.markdown("<h4 style='text-align: center; color: #111; margin-top: 15px;'>Sản phẩm bảo hiểm</h4>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 14px; color: #333; height: 80px;'>Vững tâm tận hưởng cuộc sống với các kế hoạch bảo vệ tài chính toàn diện trước những rủi ro tai nạn, bệnh hiểm nghèo.</p>", unsafe_allow_html=True)
            st.button("Tại đây →", key="btn_s1", use_container_width=True, type="primary")

    with p2:
        with st.container(border=True):
            safe_image("s2.jpg")
            st.markdown("<h4 style='text-align: center; color: #111; margin-top: 15px;'>Khiếu nại hồ sơ bảo hiểm</h4>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 14px; color: #333; height: 80px;'>Khiếu nại các thắc mắc liên quan đến Quyền lợi Bảo hiểm nhanh chóng</p>", unsafe_allow_html=True)
            st.button("Tại đây →", key="btn_s2", use_container_width=True, type="primary")

    with p3:
        with st.container(border=True):
            safe_image("s3.jpg")
            st.markdown("<h4 style='text-align: center; color: #111; margin-top: 15px;'>Giải quyết Quyền lợi bảo hiểm</h4>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 14px; color: #333; height: 80px;'>Hướng dẫn chi tiết quy trình Yêu cầu Giải quyết Quyền lợi bảo hiểm nhanh chóng, đơn giản</p>", unsafe_allow_html=True)
            st.button("Tại đây →", key="btn_s3", use_container_width=True, type="primary")


# ------------------------------------------
# TRANG 'LOGIN_CUSTOMER'
# ------------------------------------------
elif st.session_state.page == 'login_customer':
    l_c, m_c, r_c = st.columns([1, 1.2, 1])
    with m_c:
        st.markdown("<p style='text-align: center; font-weight: bold; font-size: 18px; margin-bottom: 0;'>Chào mừng anh/chị đến với<br>cổng thông tin</p>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #ed1b2e; margin-top: 5px; margin-bottom: 25px;'>PRU<span style='color:#555'>connect</span></h1>", unsafe_allow_html=True)
        
        with st.form("login_customer_form", border=False):
            st.text_input("Tên đăng nhập", placeholder="")
            st.text_input("Mật khẩu", placeholder="", type="password")
            
            # --- HIỂN THỊ CAPTCHA RANDOM ---
            cap_col1, cap_col2 = st.columns([1, 1])
            with cap_col1:
                st.markdown(f"<div style='background-color: #fcfcfc; border: 1px solid #ccc; padding: 7px; text-align: center; font-size: 24px; font-family: monospace; letter-spacing: 2px; height: 100%; display: flex; align-items: center; justify-content: center;'>{st.session_state.captcha_code}</div>", unsafe_allow_html=True)
            with cap_col2:
                entered_captcha = st.text_input("Mã bảo mật", placeholder="Nhập mã bảo mật", label_visibility="collapsed")
            
            st.write("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            
            if st.form_submit_button("Đăng nhập", use_container_width=True, type="primary"):
                if entered_captcha.upper() == st.session_state.captcha_code:
                    st.session_state.logged_in = True
                    st.session_state.role = 'customer'
                    st.session_state.user_name = "Tên khách hàng"
                    st.session_state.dashboard_tab = 'home'
                    navigate_to('dashboard')
                else:
                    st.error("Mã bảo mật không chính xác. Vui lòng nhập lại!")
        
        # --- LINK ĐĂNG KÍ ---
        _, col_reg, _ = st.columns([1, 2, 1])
        with col_reg:
            st.markdown("""
                <style>
                .element-container:has(#btn-register-cus) + div button {
                    background: transparent !important;
                    border: none !important;
                    color: #ed1b2e !important;
                    text-decoration: underline !important;
                    font-weight: normal !important;
                    box-shadow: none !important;
                    padding: 0 !important;
                }
                .element-container:has(#btn-register-cus) + div button:hover {
                    color: #c91626 !important;
                }
                </style>
                <div style='text-align: center; margin-top: 10px; font-size: 15px; margin-bottom: 2px;'>
                    <span style='color: #000;'>Chưa có tài khoản? </span>
                </div>
                <div id="btn-register-cus"></div>
            """, unsafe_allow_html=True)
            if st.button("Đăng kí", key="register_from_customer", use_container_width=True):
                st.session_state.captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                navigate_to('register')
        
        # --- NÚT QUÊN MẬT KHẨU (Ép kiểu thành Text gạch chân) ---
        _, col_btn, _ = st.columns([1, 2, 1])
        with col_btn:
            st.markdown("""
                <style>
                /* Mẹo CSS lột bỏ nền đỏ của nút bấm ngay phía dưới */
                .element-container:has(#btn-forgot) + div button {
                    background: transparent !important;
                    border: none !important;
                    color: #000 !important;
                    text-decoration: underline !important;
                    font-weight: normal !important;
                    box-shadow: none !important;
                    padding: 0 !important;
                }
                .element-container:has(#btn-forgot) + div button:hover {
                    color: #ed1b2e !important;
                }
                </style>
                <div id="btn-forgot"></div>
            """, unsafe_allow_html=True)
            
            if st.button("Quên mật khẩu", use_container_width=True):
                # Tạo mã captcha mới trước khi sang trang Quên mật khẩu
                st.session_state.captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                navigate_to('forgot_password')

# ------------------------------------------
# TRANG 'FORGOT_PASSWORD' (Quên mật khẩu)
# ------------------------------------------
elif st.session_state.page == 'forgot_password':
    l_c, m_c, r_c = st.columns([1, 1.2, 1])
    with m_c:
        st.markdown("<h3 style='text-align: center; font-weight: bold; margin-bottom: 25px;'>Quên mật khẩu đăng nhập</h3>", unsafe_allow_html=True)
        
        with st.form("forgot_password_form", border=False):
            st.text_input("Tên đăng nhập", placeholder="")
            st.text_input("Mật khẩu mới", placeholder="", type="password")
            st.text_input("Xác nhận mật khẩu", placeholder="", type="password")
            
            # --- HIỂN THỊ CAPTCHA RANDOM ---
            cap_col1, cap_col2 = st.columns([1, 1])
            with cap_col1:
                st.markdown(f"<div style='background-color: #fcfcfc; border: 1px solid #ccc; padding: 7px; text-align: center; font-size: 24px; font-family: monospace; letter-spacing: 2px; height: 100%; display: flex; align-items: center; justify-content: center;'>{st.session_state.captcha_code}</div>", unsafe_allow_html=True)
            with cap_col2:
                entered_captcha = st.text_input("Mã bảo mật", placeholder="Nhập mã bảo mật", label_visibility="collapsed")
            
            st.write("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            
            if st.form_submit_button("Đổi mật khẩu", use_container_width=True, type="primary"):
                if entered_captcha.upper() == st.session_state.captcha_code:
                    st.success("Đổi mật khẩu thành công! Vui lòng đăng nhập lại.")
                    # Reset lại captcha và cho quay về trang đăng nhập
                    st.session_state.captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                else:
                    st.error("Mã bảo mật không chính xác. Vui lòng nhập lại!")
        
        # --- NÚT QUAY LẠI TRANG ĐĂNG NHẬP (Ép kiểu thành Text gạch chân) ---
        _, col_back, _ = st.columns([1, 2, 1])
        with col_back:
            st.markdown("""
                <style>
                .element-container:has(#btn-back) + div button {
                    background: transparent !important;
                    border: none !important;
                    color: #000 !important;
                    text-decoration: underline !important;
                    font-weight: normal !important;
                    box-shadow: none !important;
                    padding: 0 !important;
                }
                .element-container:has(#btn-back) + div button:hover {
                    color: #ed1b2e !important;
                }
                </style>
                <div id="btn-back"></div>
            """, unsafe_allow_html=True)
            
            if st.button("Quay lại Đăng nhập", use_container_width=True):
                navigate_to('login_customer')
# ------------------------------------------
# TRANG 'REGISTER' (Đăng kí tài khoản)
# ------------------------------------------
elif st.session_state.page == 'register':
    l_c, m_c, r_c = st.columns([1, 1.5, 1])
    with m_c:
        st.markdown("<h1 style='text-align: center; color: #ed1b2e; margin-top: 5px; margin-bottom: 0;'>PRU<span style='color:#555'>connect</span></h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; font-weight: bold; font-size: 18px; margin-bottom: 25px; color: #000;'>Đăng kí tài khoản mới</h3>", unsafe_allow_html=True)
        
        with st.form("register_form", border=False):
            # Sử dụng cột để ép nhãn (label) và ô nhập (input) nằm ngang hàng nhau giống ảnh thiết kế
            
            c1, c2 = st.columns([1, 2])
            c1.markdown("<p style='margin-top: 7px; text-align: right; font-size: 15px;'>Tên đăng nhập</p>", unsafe_allow_html=True)
            username = c2.text_input("Tên đăng nhập", label_visibility="collapsed")
            
            c1, c2 = st.columns([1, 2])
            c1.markdown("<p style='margin-top: 7px; text-align: right; font-size: 15px;'>Mật khẩu</p>", unsafe_allow_html=True)
            password = c2.text_input("Mật khẩu", type="password", label_visibility="collapsed")
            
            c1, c2 = st.columns([1, 2])
            c1.markdown("<p style='margin-top: 7px; text-align: right; font-size: 15px;'>Xác nhận mật khẩu</p>", unsafe_allow_html=True)
            confirm_password = c2.text_input("Xác nhận mật khẩu", type="password", label_visibility="collapsed")
            
            c1, c2 = st.columns([1, 2])
            c1.markdown("<p style='margin-top: 7px; text-align: right; font-size: 15px;'>Họ và tên</p>", unsafe_allow_html=True)
            fullname = c2.text_input("Họ và tên", label_visibility="collapsed")
            
            c1, c2, c3 = st.columns([1, 1.3, 0.7])
            c1.markdown("<p style='margin-top: 7px; text-align: right; font-size: 15px;'>Email</p>", unsafe_allow_html=True)
            email = c2.text_input("Email", label_visibility="collapsed")
            c3.markdown("<p style='margin-top: 7px; font-size: 14px;'>@gmail.com</p>", unsafe_allow_html=True)
            
            c1, c2 = st.columns([1, 2])
            c1.markdown("<p style='margin-top: 7px; text-align: right; font-size: 15px;'>Số điện thoại</p>", unsafe_allow_html=True)
            phone = c2.text_input("Số điện thoại", label_visibility="collapsed")
            
            st.write("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            
            # --- HIỂN THỊ CAPTCHA RANDOM ---
            cap_col1, cap_col2 = st.columns([1, 1])
            with cap_col1:
                st.markdown(f"<div style='background-color: #fcfcfc; border: 1px solid #ccc; padding: 7px; text-align: center; font-size: 24px; font-family: monospace; letter-spacing: 2px; height: 100%; display: flex; align-items: center; justify-content: center;'>{st.session_state.captcha_code}</div>", unsafe_allow_html=True)
            with cap_col2:
                entered_captcha = st.text_input("Mã bảo mật", placeholder="Nhập mã bảo mật", label_visibility="collapsed")
            
            st.write("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            
            if st.form_submit_button("Đăng kí", use_container_width=True, type="primary"):
                if entered_captcha.upper() == st.session_state.captcha_code:
                    if password == confirm_password and password != "":
                        st.success("Đăng kí thành công! Vui lòng quay lại trang Đăng nhập.")
                        st.session_state.captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                    else:
                        st.error("Mật khẩu xác nhận không khớp hoặc bị trống!")
                else:
                    st.error("Mã bảo mật không chính xác. Vui lòng nhập lại!")
        
        # --- NÚT QUAY LẠI TRANG ĐĂNG NHẬP ---
        _, col_back, _ = st.columns([1, 2, 1])
        with col_back:
            st.markdown("""
                <style>
                .element-container:has(#btn-back-login) + div button {
                    background: transparent !important;
                    border: none !important;
                    color: #000 !important;
                    text-decoration: underline !important;
                    font-weight: normal !important;
                    box-shadow: none !important;
                    padding: 0 !important;
                }
                .element-container:has(#btn-back-login) + div button:hover {
                    color: #ed1b2e !important;
                }
                </style>
                <div id="btn-back-login"></div>
            """, unsafe_allow_html=True)
            
            if st.button("Quay lại Đăng nhập", key="back_to_login", use_container_width=True):
                st.session_state.captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                navigate_to('login_customer')

# ------------------------------------------
# TRANG 'LOGIN_EMPLOYEE'
# ------------------------------------------
elif st.session_state.page == 'login_employee':
    l_c, m_c, r_c = st.columns([1, 1.2, 1])
    
    with m_c:
        st.markdown("<p style='text-align: center; font-weight: bold; font-size: 18px; margin-bottom: 0;'>Chào mừng anh/chị đến với<br>cổng thông tin</p>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #ed1b2e; margin-top: 5px; margin-bottom: 25px;'>PRU<span style='color:#555'>connect</span></h1>", unsafe_allow_html=True)
        
        with st.form("login_employee_form", border=False):
            st.text_input("Tên đăng nhập", placeholder="")
            st.text_input("Mật khẩu", placeholder="", type="password")
            
            # --- HIỂN THỊ CAPTCHA RANDOM ---
            cap_col1, cap_col2 = st.columns([1, 1])
            with cap_col1:
                st.markdown(f"<div style='background-color: #fcfcfc; border: 1px solid #ccc; padding: 7px; text-align: center; font-size: 24px; font-family: monospace; letter-spacing: 2px; height: 100%; display: flex; align-items: center; justify-content: center;'>{st.session_state.captcha_code}</div>", unsafe_allow_html=True)
            with cap_col2:
                entered_captcha = st.text_input("Mã bảo mật", placeholder="Nhập mã bảo mật", label_visibility="collapsed")
            
            st.write("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            
            if st.form_submit_button("Đăng nhập", use_container_width=True, type="primary"):
                # Bắt buộc người dùng phải chọn vai trò ở Header trước khi đăng nhập
                if not st.session_state.temp_vai_tro:
                    st.error("Vui lòng chọn vai trò ở góc trên cùng bên phải trước khi đăng nhập!")
                elif entered_captcha.upper() == st.session_state.captcha_code:
                    st.session_state.logged_in = True
                    
                    # Lấy dữ liệu vai trò từ thanh Header xuống để xử lý
                    vai_tro = st.session_state.temp_vai_tro
                    if vai_tro == "Nhân viên Dịch vụ khách hàng":
                        st.session_state.role = 'employee_cskh'
                    elif vai_tro == "Nhân viên Xử lí khiếu nại":
                        st.session_state.role = 'employee_xlkn'
                    elif vai_tro == "Nhân viên Xử lí bồi thường":
                        st.session_state.role = 'employee_xlbt'
                        
                    st.session_state.user_name = "Tên nhân viên"
                    st.session_state.dashboard_tab = 'home'
                    navigate_to('dashboard')
                else:
                    st.error("Mã bảo mật không chính xác. Vui lòng nhập lại!")
        
        # --- LINK ĐĂNG KÍ VÀ QUÊN MẬT KHẨU ---
        _, col_reg, _ = st.columns([1, 2, 1])
        with col_reg:
            st.markdown("""
                <style>
                .element-container:has(#btn-register-emp) + div button {
                    background: transparent !important;
                    border: none !important;
                    color: #ed1b2e !important;
                    text-decoration: underline !important;
                    font-weight: normal !important;
                    box-shadow: none !important;
                    padding: 0 !important;
                }
                .element-container:has(#btn-register-emp) + div button:hover {
                    color: #c91626 !important;
                }
                </style>
                <div style='text-align: center; margin-top: 10px; font-size: 15px; margin-bottom: 2px;'>
                    <span style='color: #000;'>Chưa có tài khoản? </span>
                </div>
                <div id="btn-register-emp"></div>
            """, unsafe_allow_html=True)
            if st.button("Đăng kí", key="register_from_employee", use_container_width=True):
                st.session_state.captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                navigate_to('register')

        _, col_btn, _ = st.columns([1, 2, 1])
        with col_btn:
            st.markdown("""
                <style>
                .element-container:has(#btn-forgot-emp) + div button {
                    background: transparent !important;
                    border: none !important;
                    color: #000 !important;
                    text-decoration: underline !important;
                    font-weight: normal !important;
                    box-shadow: none !important;
                    padding: 0 !important;
                }
                .element-container:has(#btn-forgot-emp) + div button:hover {
                    color: #ed1b2e !important;
                }
                </style>
                <div id="btn-forgot-emp"></div>
            """, unsafe_allow_html=True)
            
            if st.button("Quên mật khẩu", key="forgot_emp", use_container_width=True):
                st.session_state.captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                navigate_to('forgot_password')
# ------------------------------------------
# TRANG 'DASHBOARD' (Sau đăng nhập)
# ------------------------------------------
elif st.session_state.logged_in and st.session_state.page == 'dashboard':
    
    # Xác định chức danh hiển thị chung cho toàn bộ Dashboard
    if st.session_state.role == 'customer':
        role_label = "Khách hàng"
    elif st.session_state.role == 'employee_cskh':
        role_label = "Nhân viên Dịch vụ khách hàng"
    elif st.session_state.role == 'employee_xlkn':
        role_label = "Nhân viên Xử lí khiếu nại"
    elif st.session_state.role == 'employee_xlbt':
        role_label = "Nhân viên Xử lí bồi thường"
    else:
        role_label = "Nhân viên"

    if 'dashboard_tab' not in st.session_state:
        st.session_state.dashboard_tab = 'home'
    if 'action_mode' not in st.session_state:
        st.session_state.action_mode = 'view'

    col_sid, col_cnt = st.columns([1, 2.8], gap="large")
    
    # ==========================================
    # CỘT TRÁI: SIDEBAR MENU
    # ==========================================
    with col_sid:
        st.markdown(f"""
            <div class="profile-box" style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; text-align: center; margin-bottom: 15px;">
                <div style="font-size: 50px; color: #333; margin-bottom: 10px;">👤</div>
                <div style="font-weight: 800; font-size: 20px; color: #111;">{st.session_state.user_name if st.session_state.user_name else "Mỹ Hảo"}</div>
                <div style="color: #555; font-size: 14px; margin-bottom: 10px;">{"" if st.session_state.role == 'customer' else role_label}</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Đăng xuất", key="logout_sidebar", use_container_width=True, type="primary"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.user_name = ""
            navigate_to('about')
        
        with st.container(border=True):
            st.markdown("<div style='font-size: 22px; font-weight: bold; margin-bottom: 15px;'>Menu</div>", unsafe_allow_html=True)
            
            st.markdown("""
                <style>
                div[data-testid="stVerticalBlock"] div:has(button[title="menu-btn"]) button {
                    border: none !important; background-color: transparent !important; color: #333 !important;
                    text-align: left !important; padding: 8px 10px !important; font-size: 16px !important;
                    box-shadow: none !important; justify-content: flex-start !important; border-radius: 6px !important;
                }
                div[data-testid="stVerticalBlock"] div:has(button[title="menu-btn"]) button:hover { color: #ed1b2e !important; background-color: #f9f9f9 !important; }
                div[data-testid="stVerticalBlock"] div:has(button[title="active-menu"]) button {
                    border: none !important; background-color: #fbe6e8 !important; color: #ed1b2e !important; 
                    font-weight: bold !important; text-align: left !important; padding: 8px 10px !important;
                    font-size: 16px !important; box-shadow: none !important; justify-content: flex-start !important; border-radius: 6px !important;
                }
                div[data-testid="stVerticalBlock"] div:has(button[title="link-btn"]) button {
                    background: transparent !important; border: none !important; color: #111 !important;
                    font-weight: bold !important; padding: 0 !important; box-shadow: none !important;
                    justify-content: flex-start !important; min-height: auto !important; height: auto !important; line-height: normal !important;
                }
                div[data-testid="stVerticalBlock"] div:has(button[title="link-btn"]) button:hover {
                    color: #ed1b2e !important; text-decoration: underline !important;
                }
                </style>
            """, unsafe_allow_html=True)
            
            if st.session_state.role == 'customer':
                help_c1 = "active-menu" if st.session_state.dashboard_tab == 'cus_khieunai' else "menu-btn"
                if st.button("📁 Hồ sơ khiếu nại", key="menu_c1", help=help_c1, use_container_width=True):
                    st.session_state.dashboard_tab = 'cus_khieunai'
                    st.session_state.action_mode = 'view'
                    st.rerun()
                    
                help_c2 = "active-menu" if st.session_state.dashboard_tab == 'cus_boithuong' else "menu-btn"
                if st.button("📁 Hồ sơ bồi thường", key="menu_c2", help=help_c2, use_container_width=True):
                    st.session_state.dashboard_tab = 'cus_boithuong'
                    st.session_state.action_mode = 'view'
                    st.rerun()
                
            elif st.session_state.role == 'employee_cskh':
                help_tb = "active-menu" if st.session_state.dashboard_tab == 'ql_thubao' else "menu-btn"
                if st.button("📁 Quản lí thư báo", key="menu_e1", help=help_tb, use_container_width=True):
                    st.session_state.dashboard_tab = 'ql_thubao'
                    st.session_state.action_mode = 'view' 
                    st.rerun() 
                    
                help_tk = "active-menu" if st.session_state.dashboard_tab == 'ql_taikhoan' else "menu-btn"
                if st.button("📁 Quản lí tài khoản", key="menu_e2", help=help_tk, use_container_width=True):
                    st.session_state.dashboard_tab = 'ql_taikhoan'
                    st.session_state.action_mode = 'view'
                    st.rerun()
                    
                help_hd = "active-menu" if st.session_state.dashboard_tab == 'ql_hopdong' else "menu-btn"
                if st.button("📁 Quản lí hợp đồng bảo hiểm", key="menu_e3", help=help_hd, use_container_width=True):
                    st.session_state.dashboard_tab = 'ql_hopdong'
                    st.session_state.action_mode = 'view'
                    st.rerun()
                    
            elif st.session_state.role == 'employee_xlkn':
                help_kn = "active-menu" if st.session_state.dashboard_tab == 'ql_khieunai' else "menu-btn"
                if st.button("📁 Quản lí hồ sơ khiếu nại", key="menu_kn", help=help_kn, use_container_width=True):
                    st.session_state.dashboard_tab = 'ql_khieunai'
                    st.session_state.action_mode = 'view'
                    st.rerun()
                    
            elif st.session_state.role == 'employee_xlbt':
                help_bt = "active-menu" if st.session_state.dashboard_tab == 'ql_boithuong' else "menu-btn"
                if st.button("📁 Quản lí hồ sơ bồi thường", key="menu_bt", help=help_bt, use_container_width=True):
                    st.session_state.dashboard_tab = 'ql_boithuong'
                    st.session_state.action_mode = 'view'
                    st.rerun()

    # ==========================================
    # CỘT PHẢI: NỘI DUNG CHÍNH (CONTENT)
    # ==========================================
    with col_cnt:
        # --- 1. TAB HỒ SƠ CÁ NHÂN ---
        if st.session_state.dashboard_tab == 'profile':
            display_name = st.session_state.user_name if st.session_state.user_name else "Mỹ Hảo"
            
            # A. GIAO DIỆN HỒ SƠ: KHÁCH HÀNG
            if st.session_state.role == 'customer':
                c_h1, c_b1 = st.columns([8, 2])
                c_h1.markdown("<h3 style='margin:0; color: #111;'>Thông tin khách hàng</h3>", unsafe_allow_html=True)
                with c_b1:
                    if st.button("📝 Chỉnh sửa", key="edit_cus_info", help="link-btn"): pass
                st.markdown("<hr style='margin-top: 5px; margin-bottom: 15px; border-top: 1px solid #ccc;'>", unsafe_allow_html=True)
                
                st.markdown(f"""
                    <table style='width: 100%; border: none; font-size: 16px; line-height: 2.2;'>
                        <tr><td style='width: 32%; color: #333;'>Họ và tên:</td><td style='color: #111; font-weight: 500;'>{display_name}</td></tr>
                        <tr><td style='color: #333;'>Số căn cước công dân (9 số):</td><td style='color: #111; font-weight: 500;'>234567890</td></tr>
                        <tr>
                            <td style='color: #333;'>Ngày sinh:</td>
                            <td style='color: #111; font-weight: 500;'>
                                <span style="display: inline-block; width: 45%;">20/10/2000</span>
                                <span style="color: #333; font-weight: normal;">Tỉnh thành:</span> &nbsp;&nbsp;&nbsp; TP. Hồ Chí Minh
                            </td>
                        </tr>
                        <tr><td style='color: #333;'>Địa chỉ nơi cư trú:</td><td style='color: #111; font-weight: 500;'>TP. Hồ Chí Minh</td></tr>
                        <tr><td style='color: #333;'>Số điện thoại đăng kí:</td><td style='color: #111; font-weight: 500;'>0909 123 456</td></tr>
                        <tr><td style='color: #333;'>Email:</td><td style='color: #111; font-weight: 500;'>khachhang@gmail.com</td></tr>
                    </table>
                """, unsafe_allow_html=True)

                st.write("<br><br>", unsafe_allow_html=True)

                c_h2, c_b2 = st.columns([8, 2])
                c_h2.markdown("<h3 style='margin:0; color: #111;'>Thông tin tài khoản</h3>", unsafe_allow_html=True)
                with c_b2:
                    if st.button("📝 Chỉnh sửa", key="edit_cus_acc", help="link-btn"): pass
                st.markdown("<hr style='margin-top: 5px; margin-bottom: 15px; border-top: 1px solid #ccc;'>", unsafe_allow_html=True)
                st.markdown(f"""
                    <table style='width: 100%; border: none; font-size: 16px; line-height: 2.2;'>
                        <tr><td style='width: 32%; color: #333;'>Mã tài khoản:</td><td style='color: #111; font-weight: 500;'>KH0001</td></tr>
                        <tr><td style='color: #333;'>Tên đăng nhập:</td><td style='color: #111; font-weight: 500;'>myhao_001</td></tr>
                        <tr><td style='color: #333;'>Mật khẩu:</td><td style='color: #111; font-weight: 500;'>************* &nbsp; 👁️‍🗨️</td></tr>
                    </table>
                """, unsafe_allow_html=True)

            # B. GIAO DIỆN HỒ SƠ: NHÂN VIÊN
            else:
                c_h1, c_b1 = st.columns([8, 2])
                c_h1.markdown("<h3 style='margin:0; color: #111;'>Thông tin nhân viên</h3>", unsafe_allow_html=True)
                with c_b1:
                    if st.button("📝 Chỉnh sửa", key="edit_emp_info", help="link-btn"): pass
                st.markdown("<hr style='margin-top: 5px; margin-bottom: 15px; border-top: 1px solid #ccc;'>", unsafe_allow_html=True)
                
                if st.session_state.role == 'employee_cskh':
                    phong_ban = "Phòng Dịch vụ khách hàng"
                    ma_tk = "NV_CSKH_001"
                    ten_dn = "cskh_001"
                elif st.session_state.role == 'employee_xlkn':
                    phong_ban = "Phòng Xử lí Khiếu nại"
                    ma_tk = "NV_XLKN_001"
                    ten_dn = "xlkn_001"
                elif st.session_state.role == 'employee_xlbt':
                    phong_ban = "Phòng Xử lí Bồi thường"
                    ma_tk = "NV_XLBT_001"
                    ten_dn = "xlbt_001"
                else:
                    phong_ban = "Khác"
                    ma_tk = "NV_001"
                    ten_dn = "nhanvien_001"

                st.markdown(f"""
                    <table style='width: 100%; border: none; font-size: 16px; line-height: 2.2;'>
                        <tr><td style='width: 32%; color: #333;'>Họ và tên:</td><td style='color: #111; font-weight: 500;'>{display_name}</td></tr>
                        <tr><td style='color: #333;'>Vai trò:</td><td style='color: #111; font-weight: 500;'>{role_label}</td></tr>
                        <tr><td style='color: #333;'>Phòng ban:</td><td style='color: #111; font-weight: 500;'>{phong_ban}</td></tr>
                        <tr><td style='color: #333;'>Địa chỉ nơi cư trú:</td><td style='color: #111; font-weight: 500;'>TP. Hồ Chí Minh</td></tr>
                        <tr><td style='color: #333;'>Số điện thoại đăng kí:</td><td style='color: #111; font-weight: 500;'>0909 123 456</td></tr>
                        <tr><td style='color: #333;'>Email:</td><td style='color: #111; font-weight: 500;'>nhanvien@prudential.com.vn</td></tr>
                    </table>
                """, unsafe_allow_html=True)

                st.write("<br><br>", unsafe_allow_html=True)

                c_h2, c_b2 = st.columns([8, 2])
                c_h2.markdown("<h3 style='margin:0; color: #111;'>Thông tin tài khoản</h3>", unsafe_allow_html=True)
                with c_b2:
                    if st.button("📝 Chỉnh sửa", key="edit_acc_info", help="link-btn"): pass
                st.markdown("<hr style='margin-top: 5px; margin-bottom: 15px; border-top: 1px solid #ccc;'>", unsafe_allow_html=True)
                st.markdown(f"""
                    <table style='width: 100%; border: none; font-size: 16px; line-height: 2.2;'>
                        <tr><td style='width: 32%; color: #333;'>Mã tài khoản:</td><td style='color: #111; font-weight: 500;'>{ma_tk}</td></tr>
                        <tr><td style='color: #333;'>Tên đăng nhập:</td><td style='color: #111; font-weight: 500;'>{ten_dn}</td></tr>
                        <tr><td style='color: #333;'>Mật khẩu:</td><td style='color: #111; font-weight: 500;'>************* &nbsp; 👁️‍🗨️</td></tr>
                    </table>
                """, unsafe_allow_html=True)

        # --- 2. TRANG CHỦ CHÀO MỪNG (HOME) ---
        elif st.session_state.dashboard_tab == 'home':
            safe_image("dashboard.jpg")
        # --- 2.5. CÁC TAB QUẢN LÝ CỦA KHÁCH HÀNG ---
        elif st.session_state.role == 'customer' and st.session_state.dashboard_tab == 'cus_khieunai':
            st.markdown("""
                <style>
                .header-col { border-bottom: 1px solid #ddd; padding-bottom: 10px; color: #555; font-size: 14px; }
                .row-col { border-bottom: 1px solid #f0f0f0; padding-top: 15px; padding-bottom: 15px; font-size: 15px; }
                .pill-yellow { background-color: #fceea7; color: #b08110; padding: 6px 15px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; width: 100%; text-align: center;}
                .pill-green { background-color: #4df0a9; color: #0a7346; padding: 6px 15px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; width: 100%; text-align: center;}
                .pill-red { background-color: #ffbaba; color: #a11414; padding: 6px 15px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; width: 100%; text-align: center;}
                
                div[data-testid="stVerticalBlock"] div:has(button[title="text-btn"]) button { background: transparent !important; border: none !important; color: #111 !important; font-size: 15px !important; padding: 0 !important; box-shadow: none !important; font-weight: normal !important; height: auto !important; min-height: auto !important; justify-content: flex-start !important; }
                div[data-testid="stVerticalBlock"] div:has(button[title="text-btn"]) button:hover { color: #ed1b2e !important; text-decoration: underline !important; }
                
                /* Tùy chỉnh Expander sổ xuống */
                .streamlit-expanderHeader { font-size: 16px !important; font-weight: bold !important; color: #111 !important; background-color: #f2f2f5 !important; border-radius: 8px !important; }
                </style>
            """, unsafe_allow_html=True)
            
            # 2.5.1 MÀN HÌNH XEM BẢNG HỒ SƠ
            if st.session_state.action_mode == 'view':
                st.markdown("<h3 style='margin-bottom: 20px;'>Hồ sơ khiếu nại</h3>", unsafe_allow_html=True)

                # --- THANH TÌM KIẾM ---
                st.text_input("Tìm kiếm hồ sơ", placeholder="🔍 Tìm kiếm...", label_visibility="collapsed")
                
                # --- CSS CHO NÚT BỘ LỌC & SẮP XẾP ---
                st.markdown("""
                    <style>
                    [data-testid="stHorizontalBlock"]:has(#filter-sort-row-kn) div[data-testid="stPopover"] button {
                        width: 40px !important; height: 40px !important;
                        border-radius: 50% !important; background-color: #f2f2f5 !important;
                        border: 1px solid #ddd !important; padding: 0 !important;
                        display: inline-flex !important; align-items: center !important;
                        justify-content: center !important; font-size: 18px !important;
                        color: #444 !important; line-height: 1 !important;
                    }
                    [data-testid="stHorizontalBlock"]:has(#filter-sort-row-kn) div[data-testid="stPopover"] button svg { display: none !important; }
                    [data-testid="stHorizontalBlock"]:has(#filter-sort-row-kn) div[data-testid="stPopover"] button:hover {
                        background-color: #e5e5e5 !important; border-color: #ed1b2e !important; color: #ed1b2e !important;
                    }
                    </style>
                """, unsafe_allow_html=True)

                # --- CẤU TRÚC NÚT ---
                _, col_filter, col_space, col_sort = st.columns([10, 0.4, 0.2, 0.4], gap="small")
                _.markdown('<span id="filter-sort-row-kn"></span>', unsafe_allow_html=True)

                with col_filter:
                    with st.popover("▽"):
                        st.markdown("<p style='font-weight: bold; color: #ed1b2e; margin-bottom: 10px;'>BỘ LỌC DỮ LIỆU</p>", unsafe_allow_html=True)
                        st.selectbox("Trạng thái", ["Tất cả", "Đã duyệt", "Đang duyệt", "Đang kiểm tra"], key="kn_loc_1")
                        st.selectbox("Kết quả khiếu nại", ["Tất cả", "Đủ điều kiện bồi thường", "Chưa có kết quả", "Không đủ điều kiện bồi thường"], key="kn_loc_2")

                with col_sort:
                    with st.popover("⇅"):
                        st.markdown("<p style='font-weight: bold; color: #111; margin-bottom: 15px; font-size: 16px;'>Sắp xếp theo</p>", unsafe_allow_html=True)
                        s1, s2 = st.columns([1, 4], gap="small")
                        with s1: 
                            if os.path.exists("new.png"): st.image("new.png", width=30)
                        with s2:
                            if st.button("Mới nhất", key="kn_sort_new", help="link-btn"): pass
                        
                        s3, s4 = st.columns([1, 4], gap="small")
                        with s3:
                            if os.path.exists("old.png"): st.image("old.png", width=30)
                        with s4:
                            if st.button("Trễ nhất", key="kn_sort_old", help="link-btn"): pass
                
                h1, h2, h3, h4, h5 = st.columns([1.5, 2, 2, 2.5, 1.5])
                h1.markdown("<div class='header-col'>Mã HS Khiếu nại</div>", unsafe_allow_html=True)
                h2.markdown("<div class='header-col'>Hợp đồng bảo hiểm</div>", unsafe_allow_html=True)
                h3.markdown("<div class='header-col'>Trạng thái hồ sơ</div>", unsafe_allow_html=True)
                h4.markdown("<div class='header-col' style='text-align: center;'>Kết quả</div>", unsafe_allow_html=True)
                h5.markdown("<div class='header-col'>Ngày tạo</div>", unsafe_allow_html=True)
                
                # Dòng 1 (Đủ điều kiện + Nút Bổ sung)
                r1, r2, r3, r4, r5 = st.columns([1.5, 2, 2, 2.5, 1.5], vertical_alignment="center")
                with r1:
                    if st.button("KN0001", key="cus_kn1_detail", help="text-btn", use_container_width=True):
                        st.session_state.action_mode = 'view_kn_detail_1'
                        st.rerun()
                r2.markdown("<div class='row-col'>HD0001</div>", unsafe_allow_html=True)
                r3.markdown("<div class='row-col'>Đã duyệt</div>", unsafe_allow_html=True)
                with r4:
                    st.markdown("""
                        <style>
                        .element-container:has(#btn-bosung) + div button { background-color: #4df0a9 !important; border: none !important; border-radius: 20px !important; padding: 8px 10px !important; box-shadow: none !important; width: 100% !important; height: auto !important; min-height: auto !important; display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; margin-top: 5px !important; }
                        .element-container:has(#btn-bosung) + div button:hover { background-color: #3ce098 !important; }
                        .element-container:has(#btn-bosung) + div button p { color: #0a7346 !important; font-weight: bold !important; font-size: 12px !important; margin: 0 !important; text-align: center !important; }
                        .element-container:has(#btn-bosung) + div button p::after { content: 'Bổ sung hồ sơ'; display: block; color: #ed1b2e !important; text-decoration: underline !important; font-weight: normal !important; font-size: 11px !important; margin-top: 3px; }
                        </style><div id="btn-bosung"></div>
                    """, unsafe_allow_html=True)
                    if st.button("Đủ điều kiện bồi thường", key="bs_kn1", use_container_width=True):
                        st.session_state.action_mode = 'bosung_hoso'
                        st.rerun()
                r5.markdown("<div class='row-col'>7/6/2026</div>", unsafe_allow_html=True)

                # Dòng 2 (Chưa có kết quả)
                r1, r2, r3, r4, r5 = st.columns([1.5, 2, 2, 2.5, 1.5], vertical_alignment="center")
                with r1:
                    if st.button("KN0002", key="cus_kn2_detail", help="text-btn", use_container_width=True):
                        st.session_state.action_mode = 'view_kn_detail_2'
                        st.rerun()
                r2.markdown("<div class='row-col'>HD0002</div>", unsafe_allow_html=True)
                r3.markdown("<div class='row-col'>Đang duyệt</div>", unsafe_allow_html=True)
                r4.markdown("<div style='margin-top: 15px; margin-bottom: 15px;'><span class='pill-yellow'>Chưa có kết quả</span></div>", unsafe_allow_html=True)
                r5.markdown("<div class='row-col'>7/6/2026</div>", unsafe_allow_html=True)

                # Dòng 3 (Đang kiểm tra)
                r1, r2, r3, r4, r5 = st.columns([1.5, 2, 2, 2.5, 1.5], vertical_alignment="center")
                with r1:
                    if st.button("KN0003", key="cus_kn3_detail", help="text-btn", use_container_width=True):
                        st.session_state.action_mode = 'view_kn_detail_2'
                        st.rerun()
                r2.markdown("<div class='row-col'>HD0003</div>", unsafe_allow_html=True)
                r3.markdown("<div class='row-col'>Đang kiểm tra</div>", unsafe_allow_html=True)
                r4.markdown("<div style='margin-top: 15px; margin-bottom: 15px;'><span class='pill-yellow'>Chưa có kết quả</span></div>", unsafe_allow_html=True)
                r5.markdown("<div class='row-col'>7/6/2026</div>", unsafe_allow_html=True)

                # Dòng 4 (Không đủ điều kiện)
                r1, r2, r3, r4, r5 = st.columns([1.5, 2, 2, 2.5, 1.5], vertical_alignment="center")
                with r1:
                    if st.button("KN0004", key="cus_kn4_detail", help="text-btn", use_container_width=True):
                        st.session_state.action_mode = 'view_kn_detail_3'
                        st.rerun()
                r2.markdown("<div class='row-col'>HD0004</div>", unsafe_allow_html=True)
                r3.markdown("<div class='row-col'>Đã duyệt</div>", unsafe_allow_html=True)
                r4.markdown("<div style='margin-top: 15px; margin-bottom: 15px;'><span class='pill-red' style='line-height: 1.4;'>Không đủ điều kiện<br>bồi thường</span></div>", unsafe_allow_html=True)
                r5.markdown("<div class='row-col'>7/6/2026</div>", unsafe_allow_html=True)
                
                # ---- NÚT TẠO HỒ SƠ KHIẾU NẠI ĐÃ ĐƯỢC PHỤC HỒI ----
                st.write("<br>", unsafe_allow_html=True)
                _, _, c3 = st.columns([5, 1, 3])
                with c3:
                    if st.button("➕ Tạo hồ sơ khiếu nại", use_container_width=True):
                        st.session_state.action_mode = 'create_khieunai'
                        st.rerun()

            # 2.5.2 MÀN HÌNH TẠO HỒ SƠ KHIẾU NẠI MỚI (ĐÃ ĐƯỢC PHỤC HỒI)
            elif st.session_state.action_mode == 'create_khieunai':
                col_tt, col_cl = st.columns([9, 1])
                col_tt.markdown("<h3 style='margin-bottom: 0;'>Hồ sơ khiếu nại</h3>", unsafe_allow_html=True)
                if col_cl.button("✖", key="close_kn"):
                    st.session_state.action_mode = 'view'
                    st.rerun()
                st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border: none; border-top: 2px solid #ed1b2e;'>", unsafe_allow_html=True)
                
                with st.form("form_create_kn", border=False):
                    c1, c2 = st.columns(2, gap="large")
                    with c1:
                        st.text_input("Hợp đồng bảo hiểm số:")
                        st.text_input("Ngày xảy ra sự kiện:", placeholder="dd/mm/yyyy")
                    with c2:
                        st.text_input("Người được bảo hiểm:", value="Nguyễn Văn A")
                        st.selectbox(
                            "Sản phẩm:", 
                            ["PRU-ĐẦU TƯ VỮNG TIẾN", "PRU-BẢO VỆ TỐI ĐA", "PRU-Yên Tâm Vui Khỏe", "PRU-Hành Trang Vui Khỏe", "PRU-Bảo vệ 24/7", "PRU-Easy365", "PRU-Nhiệt đới"]
                        )
                        st.text_input("Hiệu lực:", value="01/01/2025 - 01/01/2045")
                    
                    st.markdown("<hr style='margin-top: 10px; margin-bottom: 15px; border-top: 1px solid #ccc;'>", unsafe_allow_html=True)
                    st.markdown("<h4 style='margin-bottom: 10px;'>Mô tả:</h4>", unsafe_allow_html=True)
                    st.text_area("Mô tả", placeholder="| Mô tả sự kiện xảy ra, thời gian xảy ra và yêu cầu xem xét bồi thường.", label_visibility="collapsed", height=150)
                    
                    st.markdown("<hr style='margin-top: 15px; margin-bottom: 15px; border-top: 1px solid #ccc;'>", unsafe_allow_html=True)
                    
                    c3, c4 = st.columns([6, 4], gap="large")
                    with c3:
                        st.markdown("<h4 style='margin-bottom: 0px;'>Tài liệu chứng minh sự kiện xảy ra:</h4>", unsafe_allow_html=True)
                        st.markdown("<p style='color: #ed1b2e; font-size: 14px; font-style: italic; margin-bottom: 15px;'>* Lưu ý: Chọn ít nhất 1 chứng từ</p>", unsafe_allow_html=True)
                        
                        cb1, cb2 = st.columns(2)
                        with cb1:
                            st.checkbox("Hình ảnh hoặc video chứng minh sự kiện")
                            st.checkbox("Biên bản tai nạn/Xác nhận cơ quan chức năng")
                            st.checkbox("Tài liệu xác nhận từ tổ chức liên quan")
                        with cb2:
                            st.checkbox("Hồ sơ y tế")
                            st.checkbox("Giấy chứng tử")
                            st.checkbox("Tài liệu khác")
                    with c4:
                        st.write("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
                        st.file_uploader("🔗 Đính kèm tài liệu", accept_multiple_files=True, label_visibility="collapsed")
                        st.write("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                        _, btn_col = st.columns([1, 1.5])
                        if btn_col.form_submit_button("Gửi ngay ✈", type="primary", use_container_width=True):
                            st.success("Gửi hồ sơ khiếu nại thành công!")

            # 2.5.3 MÀN HÌNH BỔ SUNG HỒ SƠ BỒI THƯỜNG (Có thanh Expanders)
            elif st.session_state.action_mode == 'bosung_hoso':
                col_tt, col_cl = st.columns([9, 1])
                col_tt.markdown("<h3 style='margin-bottom: 0;'>Hồ sơ bồi thường</h3>", unsafe_allow_html=True)
                if col_cl.button("✖", key="close_bs"):
                    st.session_state.action_mode = 'view'
                    st.rerun()
                st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border: none; border-top: 2px solid #ed1b2e;'>", unsafe_allow_html=True)
                
                c1, c2 = st.columns(2, gap="large")
                c1.markdown("<p style='font-size: 16px; line-height: 2;'><b>Mã hồ sơ khiếu nại:</b> KN0001<br><b>Hợp đồng bảo hiểm số:</b> HD0001</p>", unsafe_allow_html=True)
                with c2:
                    st.markdown("<p style='font-size: 16px; line-height: 2; margin: 0;'><b>Người được bảo hiểm:</b> Nguyễn Văn A<br><b>Sản phẩm:</b> PRU-Bảo vệ tối ưu<br><b>Hiệu lực:</b> 01/01/2025 - 01/01/2045</p>", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 10px 0 20px 0; border-top: 1px solid #ccc;'>", unsafe_allow_html=True)
                
                c_title, c_note = st.columns([3, 7])
                c_title.markdown("<h3 style='margin:0;'>Tài liệu đính kèm</h3>", unsafe_allow_html=True)
                c_note.markdown("<p style='color: #ed1b2e; font-size: 14px; font-style: italic; margin:0;'>* Lưu ý:<br>- Chỉ chọn các nhóm tài liệu được yêu cầu trong thư thông báo kết quả khiếu nại.<br>- Hồ sơ bồi thường chỉ được tiếp nhận khi các tài liệu bắt buộc trong từng nhóm đã được cung cấp đầy đủ.</p>", unsafe_allow_html=True)
                
                st.write("<br>", unsafe_allow_html=True)
                
                # --- CÁC MỤC MỞ RỘNG (EXPANDER) ---
                with st.expander("▶ Hồ sơ bệnh án", expanded=False):
                    st.markdown("<p style='color: #333; font-weight: bold;'>Các tài liệu cần có:</p>", unsafe_allow_html=True)
                    e1, e2, e3 = st.columns(3)
                    e1.markdown("✓ Bệnh án <span style='color:red;'>*</span>", unsafe_allow_html=True)
                    e2.markdown("✓ Giấy ra viện <span style='color:red;'>*</span>", unsafe_allow_html=True)
                    e3.markdown("✓ Tóm tắt hồ sơ điều trị <span style='color:red;'>*</span>", unsafe_allow_html=True)
                    st.file_uploader("Tải lên hồ sơ bệnh án", accept_multiple_files=True, key="up_ba")

                with st.expander("▶ Chứng từ chi phí điều trị", expanded=False):
                    st.markdown("<p style='color: #333; font-weight: bold;'>Các tài liệu cần có:</p>", unsafe_allow_html=True)
                    e1, e2, e3 = st.columns(3)
                    e1.markdown("✓ Hóa đơn viện phí <span style='color:red;'>*</span>", unsafe_allow_html=True)
                    e2.markdown("✓ Hóa đơn thuốc <span style='color:red;'>*</span>", unsafe_allow_html=True)
                    e3.markdown("✓ Biên lai thanh toán <span style='color:red;'>*</span>", unsafe_allow_html=True)
                    st.file_uploader("Tải lên chứng từ", accept_multiple_files=True, key="up_ct")
                    
                with st.expander("▶ Kết quả xét nghiệm và chẩn đoán", expanded=False):
                    st.markdown("<p style='color: #333; font-weight: bold;'>Các tài liệu cần có:</p>", unsafe_allow_html=True)
                    e1, e2, e3 = st.columns(3)
                    e1.markdown("✓ Kết quả xét nghiệm <span style='color:red;'>*</span>", unsafe_allow_html=True)
                    e2.markdown("✓ Kết quả MRI/CT/X-Quang <span style='color:red;'>*</span>", unsafe_allow_html=True)
                    e3.markdown("✓ Kết luận chẩn đoán <span style='color:red;'>*</span>", unsafe_allow_html=True)
                    st.file_uploader("Tải lên kết quả xét nghiệm", accept_multiple_files=True, key="up_kq")
                    
                with st.expander("▶ Bảng kê chi phí y tế", expanded=False):
                    st.markdown("<p style='color: #333; font-weight: bold;'>Các tài liệu cần có:</p>", unsafe_allow_html=True)
                    e1, e2 = st.columns(2)
                    e1.markdown("✓ Bảng kê viện phí <span style='color:red;'>*</span>", unsafe_allow_html=True)
                    e2.markdown("✓ Bảng kê dịch vụ y tế <span style='color:red;'>*</span>", unsafe_allow_html=True)
                    st.file_uploader("Tải lên bảng kê", accept_multiple_files=True, key="up_bk")
                    
                with st.expander("▶ Giấy tờ người thụ hưởng/người yêu cầu", expanded=False):
                    st.markdown("<p style='color: #333; font-weight: bold;'>Các tài liệu cần có:</p>", unsafe_allow_html=True)
                    e1, e2, e3 = st.columns(3)
                    e1.markdown("✓ CCCD <span style='color:red;'>*</span>", unsafe_allow_html=True)
                    e2.markdown("✓ Giấy tờ chứng minh quan hệ <span style='color:red;'>*</span>", unsafe_allow_html=True)
                    e3.markdown("✓ Giấy ủy quyền (nếu có)", unsafe_allow_html=True)
                    st.file_uploader("Tải lên giấy tờ", accept_multiple_files=True, key="up_gt")

                st.write("<br>", unsafe_allow_html=True)
                _, btn_col = st.columns([7, 2])
                if btn_col.button("Gửi ngay ✈", type="primary", use_container_width=True):
                    st.success("Đã gửi hồ sơ bổ sung thành công!")
                    
            # 2.5.4 MÀN HÌNH CHI TIẾT HỒ SƠ KHIẾU NẠI (Khi bấm vào mã KN)
            elif st.session_state.action_mode in ['view_kn_detail_1', 'view_kn_detail_2', 'view_kn_detail_3']:
                # Tự động thay đổi kết quả (màu sắc pill) dựa trên mã được click
                if st.session_state.action_mode == 'view_kn_detail_1':
                    pill = "<span class='pill-green' style='font-size: 14px;'>Đủ điều kiện bồi thường</span>"
                elif st.session_state.action_mode == 'view_kn_detail_2':
                    pill = "<span class='pill-yellow' style='font-size: 14px;'>Chưa có kết quả</span>"
                else:
                    pill = "<span class='pill-red' style='font-size: 14px;'>Không đủ điều kiện bồi thường</span>"

                col_tt, col_cl = st.columns([9, 1])
                if col_cl.button("✖", key="close_kn_detail"):
                    st.session_state.action_mode = 'view'
                    st.rerun()
                
                c1, c2 = st.columns(2)
                c1.markdown("<p style='font-size: 16px; line-height: 2;'><b>Mã hồ sơ khiếu nại:</b> KN0001<br><b>Hợp đồng bảo hiểm số:</b> HD0001<br><b>Ngày xảy ra sự kiện:</b> xx/yy/zzzz</p>", unsafe_allow_html=True)
                with c2:
                    st.markdown("<p style='font-size: 16px; margin-bottom: 0;'><b>Người được bảo hiểm:</b> Nguyễn Văn A</p>", unsafe_allow_html=True)
                    st.selectbox(
                        "Sản phẩm:", 
                        ["PRU-ĐẦU TƯ VỮNG TIẾN", "PRU-BẢO VỆ TỐI ĐA", "PRU-Yên Tâm Vui Khỏe", "PRU-Hành Trang Vui Khỏe", "PRU-Bảo vệ 24/7", "PRU-Easy365", "PRU-Nhiệt đới"]
                    )
                    st.markdown("<p style='font-size: 16px; margin-top: 10px;'><b>Hiệu lực:</b> 01/01/2025 - 01/01/2045</p>", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                
                c3, c4 = st.columns(2, gap="large")
                with c3:
                    st.markdown("<h4 style='margin-bottom: 10px;'>Mô tả:</h4>", unsafe_allow_html=True)
                    st.markdown("<div style='border: 1px solid #ddd; padding: 15px; border-radius: 4px; font-size: 15px; color: #333;'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</div>", unsafe_allow_html=True)
                with c4:
                    st.markdown("<h4 style='margin-bottom: 10px; text-align: center;'>Tài liệu đính kèm của hồ sơ</h4>", unsafe_allow_html=True)
                    st.markdown("<div style='font-size: 40px; text-align: center; margin-top: 15px;'>📄 <span style='font-size: 14px; background: #ed1b2e; color: white; padding: 2px 5px; border-radius: 4px; font-weight: bold;'>PDF</span> &nbsp;&nbsp; 📄 <span style='font-size: 14px; background: #ed1b2e; color: white; padding: 2px 5px; border-radius: 4px; font-weight: bold;'>PDF</span></div>", unsafe_allow_html=True)
                
                st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
                
                c5, c6 = st.columns([1, 1])
                with c6:
                    d1, d2 = st.columns([1, 1.5])
                    d1.markdown("<h2 style='text-align: right; margin-top: 15px;'>Kết quả</h2>", unsafe_allow_html=True)
                    d2.markdown(f"<div style='margin-top: 25px;'>{pill}</div>", unsafe_allow_html=True)
        # --- 2.6. TAB HỒ SƠ BỒI THƯỜNG CỦA KHÁCH HÀNG ---
        elif st.session_state.role == 'customer' and st.session_state.dashboard_tab == 'cus_boithuong':
            st.markdown("""
                <style>
                .header-col { border-bottom: 1px solid #ddd; padding-bottom: 10px; color: #555; font-size: 14px; }
                .row-col { border-bottom: 1px solid #f0f0f0; padding-top: 15px; padding-bottom: 15px; font-size: 15px; }
                .pill-yellow { background-color: #fceea7; color: #b08110; padding: 6px 15px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; width: 100%; text-align: center;}
                div[data-testid="stVerticalBlock"] div:has(button[title="text-btn"]) button { background: transparent !important; border: none !important; color: #111 !important; font-size: 15px !important; padding: 0 !important; box-shadow: none !important; font-weight: normal !important; height: auto !important; min-height: auto !important; justify-content: flex-start !important; }
                div[data-testid="stVerticalBlock"] div:has(button[title="text-btn"]) button:hover { color: #ed1b2e !important; text-decoration: underline !important; }
                </style>
            """, unsafe_allow_html=True)
            
            # 2.6.1 Bảng danh sách Bồi thường
            if st.session_state.action_mode == 'view':
                h1, h2, h3, h4, h5 = st.columns([1.5, 2, 2, 2.5, 1.5])
                h1.markdown("<div class='header-col'>Mã HS Bồi thường</div>", unsafe_allow_html=True)
                h2.markdown("<div class='header-col'>Hợp đồng bảo hiểm</div>", unsafe_allow_html=True)
                h3.markdown("<div class='header-col'>Trạng thái hồ sơ</div>", unsafe_allow_html=True)
                h4.markdown("<div class='header-col' style='text-align: center;'>Kết quả</div>", unsafe_allow_html=True)
                h5.markdown("<div class='header-col'>Ngày tạo</div>", unsafe_allow_html=True)
                
                r1, r2, r3, r4, r5 = st.columns([1.5, 2, 2, 2.5, 1.5], vertical_alignment="center")
                with r1:
                    if st.button("BT0001", key="cus_bt1_detail", help="text-btn", use_container_width=True):
                        st.session_state.action_mode = 'view_bt_detail'
                        st.rerun()
                r2.markdown("<div class='row-col'>HD0001</div>", unsafe_allow_html=True)
                r3.markdown("<div class='row-col'>Đang thẩm định</div>", unsafe_allow_html=True)
                r4.markdown("<div style='margin-top: 15px; margin-bottom: 15px;'><span class='pill-yellow'>Chưa có kết quả</span></div>", unsafe_allow_html=True)
                r5.markdown("<div class='row-col'>7/6/2026</div>", unsafe_allow_html=True)

            # 2.6.2 Chi tiết Hồ sơ bồi thường
            elif st.session_state.action_mode == 'view_bt_detail':
                col_tt, col_cl = st.columns([9, 1])
                if col_cl.button("✖", key="close_bt_detail"):
                    st.session_state.action_mode = 'view'
                    st.rerun()
                
                c1, c2 = st.columns(2)
                c1.markdown("<p style='font-size: 16px; line-height: 2; margin:0;'><b>Mã hồ sơ Bồi thường:</b> KN0001<br><b>Hợp đồng bảo hiểm số:</b> HD0001<br><b>Mã hồ sơ bồi thường:</b> BT0001</p>", unsafe_allow_html=True)
                c2.markdown("<p style='font-size: 16px; line-height: 2; margin:0;'><b>Người được bảo hiểm:</b> Nguyễn Văn A<br><b>Sản phẩm:</b> PRU-Bảo vệ tối ưu<br><b>Hiệu lực:</b> 01/01/2025 - 01/01/2045</p>", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 10px 0 20px 0;'>", unsafe_allow_html=True)
                
                st.markdown("<h3 style='margin-bottom: 20px;'>Tài liệu đính kèm của hồ sơ</h3>", unsafe_allow_html=True)
                
                # In ra 7 biểu tượng PDF
                pdf_icons = ""
                for _ in range(7):
                    pdf_icons += "<span style='font-size: 40px; display:inline-block; margin-right: 25px; text-align: center; color: #ccc;'>📄<br><span style='font-size: 12px; background: #ed1b2e; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold;'>PDF</span></span>"
                st.markdown(f"<div>{pdf_icons}</div>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 14px; font-weight: bold; margin-top: 5px; margin-bottom: 30px;'>Bệnh án...</p>", unsafe_allow_html=True)
                
                st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
                d1, d2 = st.columns([1.5, 8.5])
                d1.markdown("<h2>Kết quả</h2>", unsafe_allow_html=True)
                d2.markdown("<div style='margin-top: 25px;'><span class='pill-yellow' style='font-size: 14px; padding: 8px 20px; width: auto;'>Chưa có kết quả</span></div>", unsafe_allow_html=True)


        # --- 2.7. TAB HỢP ĐỒNG BẢO HIỂM (THEO THIẾT KẾ FOLDER) ---
        elif st.session_state.role == 'customer' and st.session_state.dashboard_tab == 'cus_hopdong':
            st.markdown("""
                <style>
                div[data-testid="stVerticalBlock"] div:has(button[title="folder-btn"]) button { background: transparent !important; border: none !important; color: #111 !important; font-size: 16px !important; padding: 0 !important; box-shadow: none !important; font-weight: normal !important; height: auto !important; min-height: auto !important; justify-content: center !important; }
                div[data-testid="stVerticalBlock"] div:has(button[title="folder-btn"]) button:hover { color: #ed1b2e !important; text-decoration: underline !important; }
                </style>
            """, unsafe_allow_html=True)

            # 2.7.1 Danh sách Hợp đồng (Giao diện thư mục)
            if st.session_state.action_mode == 'view_ds_hd':
                st.markdown("<h3 style='margin-bottom: 30px;'>Danh sách hợp đồng bảo hiểm</h3>", unsafe_allow_html=True)
                
                f1, f2, f3, f4 = st.columns(4)
                
                with f1:
                    # Thay file ảnh của bạn vào đây
                    st.image("thumuc.png", use_container_width=True) 
                    if st.button("Hợp đồng số: HD0001", key="fd_1", help="folder-btn", use_container_width=True):
                        st.session_state.action_mode = 'view_hd_detail'
                        st.session_state.current_hd = 'HD0001'
                        st.rerun()
                with f2:
                    # Thay file ảnh của bạn vào đây
                    st.image("thumuc.png", use_container_width=True) 
                    if st.button("Hợp đồng số: HD0002", key="fd_2", help="folder-btn", use_container_width=True):
                        st.session_state.action_mode = 'view_hd_detail'
                        st.session_state.current_hd = 'HD0002'
                        st.rerun()

            # 2.7.2 Chi tiết Hợp đồng
            elif st.session_state.action_mode == 'view_hd_detail':
                hd_id = st.session_state.get('current_hd', 'HD0001')
                
                col_tt, col_cl = st.columns([9, 1])
                col_tt.markdown("<h3 style='margin-bottom: 0;'>Thông tin hợp đồng</h3>", unsafe_allow_html=True)
                if col_cl.button("✖", key="close_hd_detail"):
                    st.session_state.action_mode = 'view_ds_hd'
                    st.rerun()
                st.markdown("<hr style='margin-top: 5px; margin-bottom: 15px; border-top: 1px solid #ccc;'>", unsafe_allow_html=True)
                
                st.markdown(f"""
                    <table style='width: 100%; border: none; font-size: 16px; line-height: 2.2;'>
                        <tr><td style='width: 30%; color: #333;'>Mã hồ sơ:</td><td style='color: #111; font-weight: 500;'>{hd_id}</td></tr>
                        <tr><td style='color: #333;'>Loại bảo hiểm:</td><td style='color: #111; font-weight: 500;'>PRU-Bảo vệ tối ưu</td></tr>
                        <tr><td style='color: #333;'>Bên mua bảo hiểm:</td><td style='color: #111; font-weight: 500;'>Nguyễn Văn A</td></tr>
                        <tr><td style='color: #333;'>Người được bảo hiểm:</td><td style='color: #111; font-weight: 500;'>Nguyễn Văn A</td></tr>
                        <tr><td style='color: #333;'>Địa chỉ nơi cư trú:</td><td style='color: #111; font-weight: 500;'>TP. Hồ Chí Minh</td></tr>
                        <tr><td style='color: #333;'>Số điện thoại đăng kí:</td><td style='color: #111; font-weight: 500;'>0909 123 456</td></tr>
                    </table>
                """, unsafe_allow_html=True)
                
                st.markdown("<hr style='margin: 15px 0 15px 0; border-top: 1px solid #ccc;'>", unsafe_allow_html=True)
                
                c3, c4 = st.columns(2)
                c3.markdown(f"""
                    <table style='width: 100%; border: none; font-size: 16px; line-height: 2.2;'>
                        <tr><td style='width: 50%; color: #333;'>Ngày hiệu lực:</td><td style='color: #111; font-weight: 500;'>01/01/2025</td></tr>
                        <tr><td style='color: #333;'>Phí bảo hiểm định kì:</td><td style='color: #111; font-weight: 500;'>15,000,000 VND</td></tr>
                    </table>
                """, unsafe_allow_html=True)
                c4.markdown(f"""
                    <table style='width: 100%; border: none; font-size: 16px; line-height: 2.2;'>
                        <tr><td style='width: 50%; color: #333;'>Ngày hết hiệu lực:</td><td style='color: #111; font-weight: 500;'>01/01/2045</td></tr>
                        <tr><td style='color: #333;'>Định kì đóng sau:</td><td style='color: #111; font-weight: 500;'>Năm</td></tr>
                    </table>
                """, unsafe_allow_html=True)
                
                st.write("<br>", unsafe_allow_html=True)
                
                # File đính kèm nằm bên dưới (Căn phải)
                _, p1, p2 = st.columns([5, 2.5, 2.5])
                with p1:
                    st.markdown("<div style='font-size: 60px; text-align: center; color: #ccc;'>📄<br><span style='font-size: 14px; background: #ed1b2e; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold;'>PDF</span></div>", unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; font-size: 15px; margin-top: 10px;'>Giấy yêu cầu bảo hiểm</p>", unsafe_allow_html=True)
                with p2:
                    st.markdown("<div style='font-size: 60px; text-align: center; color: #ccc;'>📄<br><span style='font-size: 14px; background: #ed1b2e; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold;'>PDF</span></div>", unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; font-size: 15px; margin-top: 10px;'>Giấy khám sức khỏe</p>", unsafe_allow_html=True)
        # --- 3. CÁC TAB QUẢN LÝ CỦA NHÂN VIÊN CSKH ---
        elif st.session_state.role == 'employee_cskh':
            st.markdown("""
                <style>
                .custom-table { width: 100%; border-collapse: collapse; font-family: sans-serif; }
                .custom-table th { border-bottom: 1px solid #ddd; padding: 12px 10px; text-align: left; color: #555; font-weight: normal; font-size: 14px;}
                .custom-table td { padding: 15px 10px; border-bottom: 1px solid #f0f0f0; color: #111; font-size: 15px;}
                .pill-yellow { background-color: #fceea7; color: #b08110; padding: 6px 15px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; }
                .pill-green { background-color: #4df0a9; color: #0a7346; padding: 6px 15px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; }
                .header-col { border-bottom: 1px solid #ddd; padding-bottom: 10px; color: #555; font-size: 14px; }
                .row-col { border-bottom: 1px solid #f0f0f0; padding-top: 15px; padding-bottom: 15px; font-size: 15px; }
                
                div[data-testid="stPopover"] > button {
                    border-radius: 50% !important; width: 42px !important; height: 42px !important; padding: 0 !important;
                    background-color: #f2f2f5 !important; border: none !important; color: #555 !important;
                    font-size: 18px !important; display: inline-flex !important; align-items: center !important; justify-content: center !important;
                }
                div[data-testid="stPopover"] > button:hover { background-color: #e5e5e5 !important; color: #ed1b2e !important; }
                </style>
            """, unsafe_allow_html=True)

            # TAB 1: QUẢN LÍ THƯ BÁO
            if st.session_state.dashboard_tab == 'ql_thubao':
                if st.session_state.action_mode == 'view':
                    st.text_input("Tìm kiếm thư báo", placeholder="🔍 Tìm kiếm...", label_visibility="collapsed")
                    
                    # ==========================================
                    # NÚT BỘ LỌC & SẮP XẾP
                    # CSS: dùng data-testid="stPopover" trong từng cột, ẩn SVG mũi tên,
                    # để emoji label hiện ra thay thế. Không cần file ảnh bên ngoài.
                    # ==========================================
                    st.markdown("""
                        <style>
                        /* Style chung cho cả 2 nút popover filter/sort */
                        [data-testid="stHorizontalBlock"]:has(#filter-sort-row) div[data-testid="stPopover"] button {
                            width: 40px !important;
                            height: 40px !important;
                            border-radius: 50% !important;
                            background-color: #f2f2f5 !important;
                            border: 1px solid #ddd !important;
                            padding: 0 !important;
                            display: inline-flex !important;
                            align-items: center !important;
                            justify-content: center !important;
                            font-size: 18px !important;
                            color: #444 !important;
                            line-height: 1 !important;
                        }
                        /* Ẩn mũi tên SVG mặc định của Streamlit */
                        [data-testid="stHorizontalBlock"]:has(#filter-sort-row) div[data-testid="stPopover"] button svg {
                            display: none !important;
                        }
                        [data-testid="stHorizontalBlock"]:has(#filter-sort-row) div[data-testid="stPopover"] button:hover {
                            background-color: #e5e5e5 !important;
                            border-color: #ed1b2e !important;
                            color: #ed1b2e !important;
                        }
                        </style>
                    """, unsafe_allow_html=True)

                    _, col_filter, col_space, col_sort = st.columns([10, 0.4, 0.2, 0.4], gap="small")
                    # Đặt anchor ID trong cột đầu tiên để CSS :has() tìm đúng hàng
                    _.markdown('<span id="filter-sort-row"></span>', unsafe_allow_html=True)

                    # ==========================================
                    # NÚT 1: BỘ LỌC DỮ LIỆU (Nằm trong col_filter)
                    # ==========================================
                    with col_filter:
                        with st.popover("▽"):
                            st.markdown("<p style='font-weight: bold; color: #ed1b2e; margin-bottom: 10px;'>BỘ LỌC DỮ LIỆU</p>", unsafe_allow_html=True)
                            c1, c2 = st.columns(2)
                            c1.selectbox("Tình trạng thư báo", ["Tất cả","Đã lên lịch", "Đã gửi"])
                            c2.selectbox("Loại thư báo", ["Tất cả","Yêu cầu chỉnh sửa", "Bổ sung hồ sơ", "Thông báo kết quả khiếu nại", "Thông báo kết quả bồi thường"])
                    
                    # ==========================================
                    # NÚT 2: SẮP XẾP DỮ LIỆU (Nằm trong col_sort)
                    # ==========================================
                    with col_sort:
                        with st.popover("⇅"): # Vẫn để trống vì CSS đã gán ảnh nút chính
                            st.markdown("<p style='font-weight: bold; color: #111; margin-bottom: 15px; font-size: 16px;'>Sắp xếp theo</p>", unsafe_allow_html=True)
                            
                            # Cột 1: Lựa chọn Mới nhất
                            s1, s2 = st.columns([1, 4])
                            with s1:
                                if os.path.exists("new.png"):
                                    st.image("new.png", width=40)
                            with s2:
                                if st.button("Mới nhất", key="sort_new_option", help="link-btn"):
                                    pass
                                    
                            # Cột 2: Lựa chọn Trễ nhất
                            s3, s4 = st.columns([1, 4])
                            with s3:
                                if os.path.exists("old.png"):
                                    st.image("old.png", width=40)
                            with s4:
                                if st.button("Trễ nhất", key="sort_old_option", help="link-btn"):
                                    pass 
                    
                    h1, h2, h3, h4 = st.columns([1.5, 3.5, 2, 1.5])
                    h1.markdown("<div class='header-col'>Mã KH</div>", unsafe_allow_html=True)
                    h2.markdown("<div class='header-col'>Tiêu đề</div>", unsafe_allow_html=True)
                    h3.markdown("<div class='header-col'>Tình trạng thư</div>", unsafe_allow_html=True)
                    h4.markdown("<div class='header-col'>Ngày tạo</div>", unsafe_allow_html=True)
                    
                    r1, r2, r3, r4 = st.columns([1.5, 3.5, 2, 1.5])
                    r1.markdown("<div class='row-col'>KH0001</div>", unsafe_allow_html=True)
                    with r2:
                        st.write("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                        if st.button("THÔNG BÁO KẾT QUẢ KHIẾU NẠI", key="tb_1", help="link-btn"):
                            st.session_state.action_mode = 'view_thubao_1'
                            st.rerun()
                    r3.markdown("<div class='row-col'><span class='pill-yellow'>ĐÃ LÊN LỊCH</span></div>", unsafe_allow_html=True)
                    r4.markdown("<div class='row-col'>5/6/2026</div>", unsafe_allow_html=True)

                    r1, r2, r3, r4 = st.columns([1.5, 3.5, 2, 1.5])
                    r1.markdown("<div class='row-col'>KH0003</div>", unsafe_allow_html=True)
                    with r2:
                        st.write("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                        if st.button("YÊU CẦU ĐIỀU CHỈNH", key="tb_2", help="link-btn"):
                            st.session_state.action_mode = 'view_thubao_2'
                            st.rerun()
                    r3.markdown("<div class='row-col'><span class='pill-green'>ĐÃ GỬI</span></div>", unsafe_allow_html=True)
                    r4.markdown("<div class='row-col'>1/6/2026</div>", unsafe_allow_html=True)
                    
                    st.write("<br>", unsafe_allow_html=True)
                    _, _, c3 = st.columns([5, 1, 2.5])
                    with c3:
                        if st.button("✍️ Tạo thư báo", use_container_width=True):
                            st.session_state.action_mode = 'create_thubao'
                            st.rerun()
                
                elif st.session_state.action_mode in ['view_thubao_1', 'view_thubao_2']:
                    title = "THÔNG BÁO KẾT QUẢ KHIẾU NẠI" if st.session_state.action_mode == 'view_thubao_1' else "YÊU CẦU ĐIỀU CHỈNH"
                    status_pill = "<span class='pill-yellow'>ĐÃ LÊN LỊCH</span>" if st.session_state.action_mode == 'view_thubao_1' else "<span class='pill-green'>ĐÃ GỬI</span>"
                    
                    col_head, col_btn1, col_btn2, col_btn3 = st.columns([7, 0.8, 0.8, 1])
                    with col_head:
                        st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:baseline;'><h2 style='margin:0; text-transform:uppercase; color: #111;'>{title}</h2><span style='color:#111; font-size: 16px;'>5/6/2026</span></div>", unsafe_allow_html=True)
                    if col_btn1.button("🗑️", key="del_tb_view"): pass
                    if col_btn2.button("📝", key="edit_tb_view"): pass
                    if col_btn3.button("⬅", key="back_tb_view"):
                        st.session_state.action_mode = 'view'
                        st.rerun()

                    st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border: none; border-top: 1px solid #ccc;'>", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    c1.markdown(f"<p style='font-size: 18px;'><b>Tình trạng:</b> &nbsp; {status_pill}</p>", unsafe_allow_html=True)
                    c2.markdown("<p style='font-size: 18px;'><b>Loại thư báo:</b> &nbsp; Thư thông báo</p>", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    c1.markdown("<p style='font-size: 18px;'><b>Mã KH:</b> &nbsp; KH0001</p>", unsafe_allow_html=True)
                    c2.markdown("<p style='font-size: 18px;'><b>Ngày gửi:</b> &nbsp; 8/6/2026</p>", unsafe_allow_html=True)
                    st.markdown("<p style='font-size: 18px; font-weight: bold; margin-top: 10px;'>Nội dung:</p>", unsafe_allow_html=True)
                    st.markdown("<div style='border: 1px solid #ccc; padding: 20px; border-radius: 5px; height: 250px; overflow-y: auto; background: #fff;'><p style='font-size: 16px;'>Kính gửi Ông/Bà ABC</p><p style='font-size: 16px; line-height: 1.6;'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...</p></div>", unsafe_allow_html=True)

                elif st.session_state.action_mode == 'create_thubao':
                    col_tt, col_cl = st.columns([9, 1])
                    col_tt.markdown("<h4 style='margin-bottom: 0;'>Thư báo mới</h4>", unsafe_allow_html=True)
                    if col_cl.button("✖", key="close_tb"):
                        st.session_state.action_mode = 'view'
                        st.rerun()
                    st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border: none; border-top: 1px solid #333;'>", unsafe_allow_html=True)
                    with st.form("form_create_tb", border=False):
                        c1, c2 = st.columns([1.5, 5])
                        c1.markdown("<p style='font-size: 18px; margin-top: 5px;'>Người nhận:</p>", unsafe_allow_html=True)
                        c2.text_input("Người nhận", label_visibility="collapsed")
                        c1, c2 = st.columns([1.5, 5])
                        c1.markdown("<p style='font-size: 18px; margin-top: 5px;'>Loại thư báo:</p>", unsafe_allow_html=True)
                        c2.selectbox("Loại thư báo", ["Thư thông báo", "Yêu cầu điều chỉnh"], label_visibility="collapsed")
                        c1, c2 = st.columns([1.5, 5])
                        c1.markdown("<p style='font-size: 18px; font-weight: bold; margin-top: 5px;'>Tiêu đề</p>", unsafe_allow_html=True)
                        c2.text_input("Tiêu đề", label_visibility="collapsed")
                        st.markdown("<hr style='margin-top: 10px; margin-bottom: 10px; border: none; border-top: 1px solid #333;'>", unsafe_allow_html=True)
                        st.text_area("Nội dung", placeholder="| Vị trí nhập nội dung", height=250, label_visibility="collapsed")
                        st.markdown("<hr style='margin-top: 10px; margin-bottom: 20px; border: none; border-top: 1px solid #333;'>", unsafe_allow_html=True)
                        btn1, btn2, _ = st.columns([2, 2, 6])
                        if btn1.form_submit_button("Gửi ngay", type="primary", use_container_width=True):
                            st.success("Đã gửi thư báo thành công!")
                        if btn2.form_submit_button("Lên lịch", use_container_width=True):
                            st.info("Đã lên lịch gửi thư.")
            
            # TAB 2: QUẢN LÍ TÀI KHOẢN
            elif st.session_state.dashboard_tab == 'ql_taikhoan':
                st.text_input("Tìm kiếm tài khoản", placeholder="🔍 Tìm kiếm...", label_visibility="collapsed")
                
                # CSS: Style chung cho các nút popover trong Tab 2
                st.markdown("""
                    <style>
                    [data-testid="stHorizontalBlock"]:has(#filter-sort-row-acc) div[data-testid="stPopover"] button {
                        width: 40px !important;
                        height: 40px !important;
                        border-radius: 50% !important;
                        background-color: #f2f2f5 !important;
                        border: 1px solid #ddd !important;
                        padding: 0 !important;
                        display: inline-flex !important;
                        align-items: center !important;
                        justify-content: center !important;
                        font-size: 18px !important;
                        color: #444 !important;
                        line-height: 1 !important;
                    }
                    [data-testid="stHorizontalBlock"]:has(#filter-sort-row-acc) div[data-testid="stPopover"] button svg {
                        display: none !important;
                    }
                    [data-testid="stHorizontalBlock"]:has(#filter-sort-row-acc) div[data-testid="stPopover"] button:hover {
                        background-color: #e5e5e5 !important;
                        border-color: #ed1b2e !important;
                        color: #ed1b2e !important;
                    }
                    </style>
                """, unsafe_allow_html=True)

                _, col_filter, col_space, col_sort = st.columns([10, 0.4, 0.2, 0.4], gap="small")
                _.markdown('<span id="filter-sort-row-acc"></span>', unsafe_allow_html=True)

                # NÚT 1: BỘ LỌC TÀI KHOẢN
                with col_filter:
                    with st.popover("▽"):
                        st.markdown("<p style='font-weight: bold; color: #ed1b2e; margin-bottom: 10px;'>BỘ LỌC DỮ LIỆU</p>", unsafe_allow_html=True)
                        c1, c2 = st.columns([1, 1.5], gap="large")
                        with c1:
                            st.markdown("<p style='font-size: 16px; font-weight: bold; margin-bottom: 5px;'>Theo tỉnh thành</p>", unsafe_allow_html=True)
                            st.text_input("Tỉnh thành", placeholder="🔍", label_visibility="collapsed")
                        with c2:
                            st.markdown("<p style='font-size: 16px; font-weight: bold; margin-bottom: 5px;'>Thời gian đăng kí</p>", unsafe_allow_html=True)
                            d1, d2, d3 = st.columns(3)
                            d1.text_input("Ngày", placeholder="Ngày", label_visibility="collapsed")
                            d2.text_input("Tháng", placeholder="Tháng", label_visibility="collapsed")
                            d3.text_input("Năm", placeholder="Năm", label_visibility="collapsed")

                # NÚT 2: SẮP XẾP TÀI KHOẢN
                with col_sort:
                    with st.popover("⇅"):
                        st.markdown("<p style='font-weight: bold; color: #111; margin-bottom: 15px; font-size: 16px;'>Sắp xếp theo</p>", unsafe_allow_html=True)
                        
                        s1, s2 = st.columns([1, 4])
                        with s1:
                            if os.path.exists("new.png"): st.image("new.png", width=40)
                        with s2:
                            if st.button("Mới nhất", key="acc_sort_new", help="link-btn"): pass
                        
                        s3, s4 = st.columns([1, 4])
                        with s3:
                            if os.path.exists("old.png"): st.image("old.png", width=40)
                        with s4:
                            if st.button("Trễ nhất", key="acc_sort_old", help="link-btn"): pass
                                
                st.write("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                st.markdown('<table class="custom-table"><tr><th>Mã KH</th><th>Họ và tên</th><th>Tỉnh thành</th><th>Số điện thoại</th><th>Ngày đăng kí</th></tr><tr><td>KH0001</td><td style="font-weight: bold;">Nguyễn Thị A</td><td>Hà Nội</td><td>0123.567.890</td><td>05/06/2025</td></tr><tr><td>KH0003</td><td style="font-weight: bold;">Trần Văn B</td><td>TP.HCM</td><td>0987.654.321</td><td>01/01/2026</td></tr><tr><td>KH0004</td><td style="font-weight: bold;">Trần Hoàng C</td><td>Hà Nội</td><td>0987.123.456</td><td>08/02/2026</td></tr><tr><td>KH0005</td><td style="font-weight: bold;">Hoàng Ngọc D</td><td>Hà Nội</td><td>0912.456.789</td><td>10/02/2026</td></tr></table>', unsafe_allow_html=True)
            # TAB 3: QUẢN LÍ HỢP ĐỒNG BẢO HIỂM
            elif st.session_state.dashboard_tab == 'ql_hopdong':
                if st.session_state.action_mode == 'view':
                    st.text_input("Tìm kiếm hợp đồng", placeholder="🔍 Tìm kiếm...", label_visibility="collapsed")
                    
                    # CSS: Style chung cho các nút popover trong Tab 3 (ID riêng biệt)
                    st.markdown("""
                        <style>
                        [data-testid="stHorizontalBlock"]:has(#filter-sort-row-contract) div[data-testid="stPopover"] button {
                            width: 40px !important;
                            height: 40px !important;
                            border-radius: 50% !important;
                            background-color: #f2f2f5 !important;
                            border: 1px solid #ddd !important;
                            padding: 0 !important;
                            display: inline-flex !important;
                            align-items: center !important;
                            justify-content: center !important;
                            font-size: 18px !important;
                            color: #444 !important;
                            line-height: 1 !important;
                        }
                        [data-testid="stHorizontalBlock"]:has(#filter-sort-row-contract) div[data-testid="stPopover"] button svg {
                            display: none !important;
                        }
                        [data-testid="stHorizontalBlock"]:has(#filter-sort-row-contract) div[data-testid="stPopover"] button:hover {
                            background-color: #e5e5e5 !important;
                            border-color: #ed1b2e !important;
                            color: #ed1b2e !important;
                        }
                        </style>
                    """, unsafe_allow_html=True)

                    _, col_filter, col_space, col_sort = st.columns([10, 0.4, 0.2, 0.4], gap="small")
                    _.markdown('<span id="filter-sort-row-contract"></span>', unsafe_allow_html=True)

                    # NÚT 1: BỘ LỌC HỢP ĐỒNG
                    with col_filter:
                        with st.popover("▽"):
                            st.markdown("<p style='font-weight: bold; color: #ed1b2e; margin-bottom: 10px;'>BỘ LỌC DỮ LIỆU</p>", unsafe_allow_html=True)
                            st.selectbox("Tình trạng hồ sơ", ["Tất cả", "Còn hiệu lực", "Hết hiệu lực"])
                            st.selectbox("Sản phẩm bảo hiểm", ["Tất cả", "PRU-ĐẦU TƯ VỮNG TIẾN", "PRU-BẢO VỆ TỐI ĐA", "PRU-Yên Tâm Vui Khỏe", "PRU-Hành Trang Vui Khỏe", "PRU-Bảo vệ 24/7", "PRU-Easy365", "PRU-Nhiệt đới"])

                    # NÚT 2: SẮP XẾP HỢP ĐỒNG
                    with col_sort:
                        with st.popover("⇅"):
                            st.markdown("<p style='font-weight: bold; color: #111; margin-bottom: 15px; font-size: 16px;'>Sắp xếp theo</p>", unsafe_allow_html=True)
                            
                            s1, s2 = st.columns([1, 4])
                            with s1:
                                if os.path.exists("new.png"): st.image("new.png", width=40)
                            with s2:
                                if st.button("Mới nhất", key="hd_sort_new", help="link-btn"): pass
                            
                            s3, s4 = st.columns([1, 4])
                            with s3:
                                if os.path.exists("old.png"): st.image("old.png", width=40)
                            with s4:
                                if st.button("Trễ nhất", key="hd_sort_old", help="link-btn"): pass
                            
                    st.write("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                    
                    h1, h2, h3, h4, h5 = st.columns([1.5, 3, 2.5, 2.5, 1.5])
                    h1.markdown("<div class='header-col'>Mã Hợp đồng</div>", unsafe_allow_html=True)
                    h2.markdown("<div class='header-col'>Loại bảo hiểm</div>", unsafe_allow_html=True)
                    h3.markdown("<div class='header-col'>Tình trạng bảo hiểm</div>", unsafe_allow_html=True)
                    h4.markdown("<div class='header-col'>Bên mua bảo hiểm</div>", unsafe_allow_html=True)
                    h5.markdown("<div class='header-col'>Ngày hiệu lực</div>", unsafe_allow_html=True)
                    
                    r1, r2, r3, r4, r5 = st.columns([1.5, 3, 2.5, 2.5, 1.5])
                    r1.markdown("<div class='row-col'>HĐ0001</div>", unsafe_allow_html=True)
                    with r2:
                        st.write("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                        if st.button("PRU-BẢO VỆ TỐI ĐA", key="hd_1", help="link-btn"):
                            st.session_state.action_mode = 'view_hopdong_1'
                            st.rerun()
                    r3.markdown("<div class='row-col'><span class='pill-green'>Còn hiệu lực</span></div>", unsafe_allow_html=True)
                    r4.markdown("<div class='row-col'>Nguyễn Văn A</div>", unsafe_allow_html=True)
                    r5.markdown("<div class='row-col'>1/1/2026</div>", unsafe_allow_html=True)

                    r1, r2, r3, r4, r5 = st.columns([1.5, 3, 2.5, 2.5, 1.5])
                    r1.markdown("<div class='row-col'>HĐ0002</div>", unsafe_allow_html=True)
                    with r2:
                        st.write("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                        if st.button("PRU-Yên Tâm Vui Khỏe", key="hd_2", help="link-btn"):
                            st.session_state.action_mode = 'view_hopdong_2'
                            st.rerun()
                    r3.markdown("<div class='row-col'><span class='pill-yellow'>Hết hiệu lực</span></div>", unsafe_allow_html=True)
                    r4.markdown("<div class='row-col'>Nguyễn Thị B</div>", unsafe_allow_html=True)
                    r5.markdown("<div class='row-col'>1/6/2026</div>", unsafe_allow_html=True)
                    
                    st.write("<br>", unsafe_allow_html=True)
                    _, _, c3 = st.columns([5, 1, 2.5])
                    with c3:
                        if st.button("➕ Tạo hợp đồng", use_container_width=True):
                            st.session_state.action_mode = 'create_hopdong'
                            st.rerun()
                            
                elif st.session_state.action_mode in ['view_hopdong_1', 'view_hopdong_2']:
                    product_name = "PRU-BẢO VỆ TỐI ĐA" if st.session_state.action_mode == 'view_hopdong_1' else "PRU-Yên Tâm Vui Khỏe"
                    status_pill = "<span class='pill-green'>Còn hiệu lực</span>" if st.session_state.action_mode == 'view_hopdong_1' else "<span class='pill-yellow'>Hết hiệu lực</span>"
                    
                    c_t1, c_b1, c_back = st.columns([7, 2, 1])
                    c_t1.markdown("<h3 style='margin:0; color: #111;'>Thông tin hợp đồng</h3>", unsafe_allow_html=True)
                    with c_b1:
                        if st.button("📝 Chỉnh sửa", key="edit_hinfo", help="link-btn"): pass
                    if c_back.button("⬅", key="back_hd_view"):
                        st.session_state.action_mode = 'view'
                        st.rerun()
                    st.markdown("<hr style='margin-top: 5px; margin-bottom: 15px; border-top: 1px solid #ccc;'>", unsafe_allow_html=True)
                    st.markdown(f"<table style='width: 100%; border: none; font-size: 18px; line-height: 1.8;'><tr><td style='width: 30%;'>Mã hợp đồng:</td><td>HĐ0001</td></tr><tr><td>Loại sản phẩm:</td><td>{product_name}</td></tr><tr><td>Tình trạng Bảo hiểm:</td><td>{status_pill}</td></tr><tr><td>Ngày hiệu lực:</td><td>1/1/2026</td></tr><tr><td>Phí bảo hiểm định kỳ:</td><td>15,000,000 VND</td></tr><tr><td>Tần suất đóng:</td><td>Năm</td></tr><tr><td>Trạng thái:</td><td>Hoàn tất</td></tr></table>", unsafe_allow_html=True)
                    
                    st.write("<br>", unsafe_allow_html=True)
                    c_t2, c_b2, _ = st.columns([7, 2, 1])
                    c_t2.markdown("<h3 style='margin:0; color: #111;'>Thông tin khách hàng</h3>", unsafe_allow_html=True)
                    with c_b2:
                        if st.button("📝 Chỉnh sửa", key="edit_cinfo", help="link-btn"): pass
                    st.markdown("<hr style='margin-top: 5px; margin-bottom: 15px; border-top: 1px solid #ccc;'>", unsafe_allow_html=True)
                    st.markdown("<table style='width: 100%; border: none; font-size: 18px; line-height: 1.8;'><tr><td style='width: 30%;'>Mã Khách hàng:</td><td>KH0001</td></tr><tr><td>Tên khách hàng:</td><td>Nguyễn Văn A</td></tr><tr><td>Số điện thoại:</td><td>0123.567.890</td></tr><tr><td>Địa chỉ:</td><td>Số 123, đường ABC, Quận D, TP HCM</td></tr></table>", unsafe_allow_html=True)

                elif st.session_state.action_mode == 'create_hopdong':
                    col_tt, col_cl = st.columns([9, 1])
                    col_tt.markdown("<h4 style='margin-bottom: 0;'>Tạo Hồ sơ</h4>", unsafe_allow_html=True)
                    if col_cl.button("✖", key="close_hd"):
                        st.session_state.action_mode = 'view'
                        st.rerun()
                    st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border: none; border-top: 2px solid #ed1b2e;'>", unsafe_allow_html=True)
                    with st.form("form_create_hd", border=False):
                        c_left, c_right = st.columns(2, gap="large")
                        with c_left:
                            st.text_input("Mã Hồ sơ")
                            st.selectbox("Loại Bảo hiểm", ["PRU-ĐẦU TƯ VỮNG TIẾN", "PRU-BẢO VỆ TỐI ĐA", "PRU-Yên Tâm Vui Khỏe", "PRU-Hành Trang Vui Khỏe", "PRU-Bảo vệ 24/7", "PRU-Easy365", "PRU-Nhiệt đới"])
                            st.text_input("Bên mua Bảo hiểm")
                            st.text_input("Số điện thoại")
                            st.text_input("Địa chỉ")
                            st.text_input("Ngày hiệu lực")
                        with c_right:
                            st.text_input("Người được Bảo hiểm")
                            st.text_input("Phí Bảo hiểm Định kỳ")
                            st.markdown("<p style='font-size: 16px; margin-top: 15px; margin-bottom: 5px;'>Tài liệu đính kèm</p>", unsafe_allow_html=True)
                            st.checkbox("Giấy yêu cầu bảo hiểm nhân thọ *")
                            st.checkbox("Các giấy tờ khai báo tình trạng sức khỏe *")
                        st.write("<br>", unsafe_allow_html=True)
                        _, btn_col = st.columns([3, 1])
                        if btn_col.form_submit_button("Tạo Hồ sơ", type="primary", use_container_width=True):
                            st.success("Hồ sơ đã được tạo thành công!")
            # --- TAB 4: GIAO DIỆN THÔNG BÁO (KHI BẤM CHUÔNG) ---
            elif st.session_state.dashboard_tab == 'thong_bao':
                col_title, col_space, col_btn = st.columns([5, 4, 1])
                
                with col_title:
                    st.markdown("<h2 style='color: #ff4b4b; margin-top: 0; padding-top: 0; font-weight: bold;'>Thư Báo</h2>", unsafe_allow_html=True)
                    
                # --- NÚT BỘ LỌC & SẮP XẾP CHO TAB THÔNG BÁO ---
                # CSS: Style chung cho các nút popover hình tròn
                st.markdown("""
                    <style>
                    [data-testid="stHorizontalBlock"]:has(#filter-sort-row-bell) div[data-testid="stPopover"] button {
                        width: 40px !important;
                        height: 40px !important;
                        border-radius: 50% !important;
                        background-color: #f2f2f5 !important;
                        border: 1px solid #ddd !important;
                        padding: 0 !important;
                        display: inline-flex !important;
                        align-items: center !important;
                        justify-content: center !important;
                        font-size: 18px !important;
                        color: #444 !important;
                        line-height: 1 !important;
                    }
                    [data-testid="stHorizontalBlock"]:has(#filter-sort-row-bell) div[data-testid="stPopover"] button svg {
                        display: none !important;
                    }
                    [data-testid="stHorizontalBlock"]:has(#filter-sort-row-bell) div[data-testid="stPopover"] button:hover {
                        background-color: #e5e5e5 !important;
                        border-color: #ed1b2e !important;
                        color: #ed1b2e !important;
                    }
                    </style>
                """, unsafe_allow_html=True)

                # Chia cột: 10 phần trống bên trái, 0.4 cho lọc, 0.2 cho khoảng cách, 0.4 cho sắp xếp
                _, col_filter, col_space, col_sort = st.columns([10, 0.4, 0.2, 0.4], gap="small")
                _.markdown('<span id="filter-sort-row-bell"></span>', unsafe_allow_html=True)

                # ==========================================
                # NÚT 1: BỘ LỌC DỮ LIỆU (Nằm trong col_filter)
                # ==========================================
                with col_filter:
                    with st.popover("▽"):
                        st.markdown("<p style='font-weight: bold; color: #ed1b2e; margin-bottom: 10px;'>BỘ LỌC DỮ LIỆU</p>", unsafe_allow_html=True)
                        c1, c2 = st.columns(2)
                        c1.selectbox("Tình trạng thư báo", ["Tất cả","Đã lên lịch", "Đã gửi"])
                        c2.selectbox("Loại thư báo", ["Tất cả","Yêu cầu chỉnh sửa", "Bổ sung hồ sơ", "Thông báo kết quả khiếu nại", "Thông báo kết quả bồi thường"])
                
                # ==========================================
                # NÚT 2: SẮP XẾP DỮ LIỆU (Nằm trong col_sort)
                # ==========================================
                with col_sort:
                    with st.popover("⇅"): # Vẫn để trống vì CSS đã gán ảnh nút chính
                        st.markdown("<p style='font-weight: bold; color: #111; margin-bottom: 15px; font-size: 16px;'>Sắp xếp theo</p>", unsafe_allow_html=True)
                        
                        # Cột 1: Lựa chọn Mới nhất
                        s1, s2 = st.columns([1, 4])
                        with s1:
                            if os.path.exists("new.png"):
                                st.image("new.png", width=40)
                        with s2:
                            if st.button("Mới nhất", key="sort_new_option", help="link-btn"):
                                pass
                                
                        # Cột 2: Lựa chọn Trễ nhất
                        s3, s4 = st.columns([1, 4])
                        with s3:
                            if os.path.exists("old.png"):
                                st.image("old.png", width=40)
                        with s4:
                            if st.button("Trễ nhất", key="sort_old_option", help="link-btn"):
                                pass
                        
                st.markdown("<hr style='margin-top: 0px; margin-bottom: 15px; border: none; border-top: 2px solid #333;'>", unsafe_allow_html=True)
                
                # Khối thư 1
                c1, c2 = st.columns([8, 2])
                with c1:
                    st.markdown("<p style='font-size: 20px; font-weight: bold; margin-bottom: 5px;'>[Tiêu đề thư]</p><p style='font-size: 16px;'>Lorem ipsum dolor sit amet, consectetur adipiscing elit...</p>", unsafe_allow_html=True)
                with c2:
                    st.markdown("<p style='text-align: right; font-size: 15px;'>15:00 5/6/2025</p>", unsafe_allow_html=True)
                st.markdown("<hr style='margin-top: 15px; margin-bottom: 15px; border: none; border-top: 1px solid #aaa;'>", unsafe_allow_html=True)
                
                # Khối thư 2
                c3, c4 = st.columns([8, 2])
                with c3:
                    st.markdown("<p style='font-size: 20px; font-weight: bold; margin-bottom: 5px;'>[Tiêu đề thư]</p><p style='font-size: 16px;'>Lorem ipsum dolor sit amet, consectetur adipiscing elit...</p>", unsafe_allow_html=True)
                with c4:
                    st.markdown("<p style='text-align: right; font-size: 15px;'>15:00 5/6/2025</p>", unsafe_allow_html=True)
        # --- 4. GIAO DIỆN NHÂN VIÊN XỬ LÍ KHIẾU NẠI ---
        elif st.session_state.role == 'employee_xlkn':
            st.markdown("""
                <style>
                .header-col { border-bottom: 1px solid #ddd; padding-bottom: 10px; color: #555; font-size: 14px; }
                .row-col { border-bottom: 1px solid #f0f0f0; padding-top: 15px; padding-bottom: 15px; font-size: 15px; }
                .pill-yellow { background-color: #fceea7; color: #b08110; padding: 6px 15px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; }
                .pill-green { background-color: #4df0a9; color: #0a7346; padding: 6px 15px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; }
                .pill-red { background-color: #ffbaba; color: #a11414; padding: 6px 15px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; text-align: center;}
                </style>
            """, unsafe_allow_html=True)
            
            if st.session_state.dashboard_tab == 'home':
                st.info("👈 Vui lòng chọn một danh mục quản lý bên thanh Menu để bắt đầu làm việc.")
                safe_image("dashboard.jpg")
                
            elif st.session_state.dashboard_tab == 'ql_khieunai':
                if st.session_state.action_mode == 'view':
                    st.markdown("<h3 style='margin-bottom: 20px;'>Quản lý hồ sơ khiếu nại</h3>", unsafe_allow_html=True)
                    
                    # Bảng dữ liệu
                    h1, h2, h3, h4, h5 = st.columns([1.5, 2, 2, 2.5, 1.5])
                    h1.markdown("<div class='header-col'>Mã HS Khiếu nại</div>", unsafe_allow_html=True)
                    h2.markdown("<div class='header-col'>Hợp đồng bảo hiểm</div>", unsafe_allow_html=True)
                    h3.markdown("<div class='header-col'>Trạng thái hồ sơ</div>", unsafe_allow_html=True)
                    h4.markdown("<div class='header-col'>Kết quả</div>", unsafe_allow_html=True)
                    h5.markdown("<div class='header-col'>Ngày tạo</div>", unsafe_allow_html=True)
                    
                    # Row 1
                    r1, r2, r3, r4, r5 = st.columns([1.5, 2, 2, 2.5, 1.5])
                    with r1:
                        st.write("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                        if st.button("KN0001", key="kn_1", help="link-btn"):
                            st.session_state.action_mode = 'view_kn_1'
                            st.rerun()
                    r2.markdown("<div class='row-col'>HD0001</div>", unsafe_allow_html=True)
                    r3.markdown("<div class='row-col'>Đã duyệt</div>", unsafe_allow_html=True)
                    r4.markdown("<div class='row-col'><span class='pill-green'>Đủ điều kiện bồi thường</span></div>", unsafe_allow_html=True)
                    r5.markdown("<div class='row-col'>7/6/2026</div>", unsafe_allow_html=True)

                    # Row 2
                    r1, r2, r3, r4, r5 = st.columns([1.5, 2, 2, 2.5, 1.5])
                    with r1:
                        st.write("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                        if st.button("KN0002", key="kn_2", help="link-btn"):
                            st.session_state.action_mode = 'view_kn_2'
                            st.rerun()
                    r2.markdown("<div class='row-col'>HD0002</div>", unsafe_allow_html=True)
                    r3.markdown("<div class='row-col'>Đang duyệt</div>", unsafe_allow_html=True)
                    r4.markdown("<div class='row-col'><span class='pill-yellow'>Chưa có kết quả</span></div>", unsafe_allow_html=True)
                    r5.markdown("<div class='row-col'>7/6/2026</div>", unsafe_allow_html=True)
                
                    # Row 3
                    r1, r2, r3, r4, r5 = st.columns([1.5, 2, 2, 2.5, 1.5])
                    with r1:
                        st.write("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                        if st.button("KN0004", key="kn_3", help="link-btn"):
                            st.session_state.action_mode = 'view_kn_3'
                            st.rerun()
                    r2.markdown("<div class='row-col'>HD0004</div>", unsafe_allow_html=True)
                    r3.markdown("<div class='row-col'>Đã duyệt</div>", unsafe_allow_html=True)
                    r4.markdown("<div class='row-col'><span class='pill-red' style='line-height: 1.4;'>Không đủ điều kiện<br>bồi thường</span></div>", unsafe_allow_html=True)
                    r5.markdown("<div class='row-col'>7/6/2026</div>", unsafe_allow_html=True)
                    
                elif st.session_state.action_mode in ['view_kn_1', 'view_kn_2', 'view_kn_3']:
                    # Chi tiết hồ sơ khiếu nại
                    col_tt, col_cl = st.columns([9, 1])
                    if col_cl.button("✖", key="close_kn"):
                        st.session_state.action_mode = 'view'
                        st.rerun()
                        
                    c1, c2 = st.columns(2)
                    c1.markdown("<p style='font-size: 16px; line-height: 2;'><b>Mã hồ sơ khiếu nại:</b> KN0001<br><b>Hợp đồng bảo hiểm số:</b> HD0001<br><b>Ngày xảy ra sự kiện:</b> xx/yy/zzzz</p>", unsafe_allow_html=True)
                    c2.markdown("<p style='font-size: 16px; line-height: 2;'><b>Người được bảo hiểm:</b> Nguyễn Văn A<br><b>Sản phẩm:</b> PRU-Bảo vệ tối ưu<br><b>Hiệu lực:</b> 01/01/2025 - 01/01/2045</p>", unsafe_allow_html=True)
                    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                    
                    c3, c4 = st.columns(2, gap="large")
                    with c3:
                        st.markdown("<h4 style='margin-bottom: 10px;'>Mô tả:</h4>", unsafe_allow_html=True)
                        st.markdown("<div style='border: 1px solid #ddd; padding: 15px; border-radius: 4px; font-size: 15px; color: #333;'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</div>", unsafe_allow_html=True)
                    with c4:
                        st.markdown("<h4 style='margin-bottom: 10px;'>Tài liệu đính kèm của hồ sơ</h4>", unsafe_allow_html=True)
                        st.markdown("<div style='font-size: 40px;'>📄 <span style='font-size: 14px; background: #ed1b2e; color: white; padding: 2px 5px; border-radius: 4px; font-weight: bold;'>PDF</span> &nbsp;&nbsp; 📄 <span style='font-size: 14px; background: #ed1b2e; color: white; padding: 2px 5px; border-radius: 4px; font-weight: bold;'>PDF</span></div>", unsafe_allow_html=True)
                    
                    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
                    
                    c5, c6 = st.columns(2, gap="large")
                    with c5:
                        st.markdown("<h4>Phản hồi:</h4>", unsafe_allow_html=True)
                        st.text_area("Phản hồi", placeholder="Phản hồi cho vấn đề của khách hàng, có khả năng được bồi thường hay không.", label_visibility="collapsed", height=120)
                    with c6:
                        st.markdown("<h4>Kết quả</h4>", unsafe_allow_html=True)
                        st.selectbox("Kết quả", ["Chưa có kết quả", "Đủ điều kiện bồi thường", "Không đủ điều kiện bồi thường"], label_visibility="collapsed")
                        st.write("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
                        _, btn_col = st.columns([2, 1])
                        if btn_col.button("Cập nhật", type="primary", use_container_width=True):
                            st.success("Đã cập nhật hồ sơ!")

        # --- 5. GIAO DIỆN NHÂN VIÊN XỬ LÍ BỒI THƯỜNG ---
        elif st.session_state.role == 'employee_xlbt':
            st.markdown("""
                <style>
                .header-col { border-bottom: 1px solid #ddd; padding-bottom: 10px; color: #555; font-size: 14px; }
                .row-col { border-bottom: 1px solid #f0f0f0; padding-top: 15px; padding-bottom: 15px; font-size: 15px; }
                .pill-yellow { background-color: #fceea7; color: #b08110; padding: 6px 15px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; }
                .pill-green { background-color: #4df0a9; color: #0a7346; padding: 6px 15px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; }
                .pill-red { background-color: #ffbaba; color: #a11414; padding: 6px 15px; border-radius: 20px; font-weight: bold; font-size: 12px; display: inline-block; text-align: center;}
                </style>
            """, unsafe_allow_html=True)
            
            if st.session_state.dashboard_tab == 'home':
                st.info("👈 Vui lòng chọn một danh mục quản lý bên thanh Menu để bắt đầu làm việc.")
                safe_image("dashboard.jpg")
                
            elif st.session_state.dashboard_tab == 'ql_boithuong':
                if st.session_state.action_mode == 'view':
                    st.markdown("<h3 style='margin-bottom: 20px;'>Quản lý hồ sơ bồi thường</h3>", unsafe_allow_html=True)
                    
                    # Bảng dữ liệu
                    h1, h2, h3, h4, h5 = st.columns([1.5, 2, 2, 2.5, 1.5])
                    h1.markdown("<div class='header-col'>Mã HS Bồi thường</div>", unsafe_allow_html=True)
                    h2.markdown("<div class='header-col'>Hợp đồng bảo hiểm</div>", unsafe_allow_html=True)
                    h3.markdown("<div class='header-col'>Trạng thái hồ sơ</div>", unsafe_allow_html=True)
                    h4.markdown("<div class='header-col'>Kết quả</div>", unsafe_allow_html=True)
                    h5.markdown("<div class='header-col'>Ngày tạo</div>", unsafe_allow_html=True)
                    
                    # Row 1
                    r1, r2, r3, r4, r5 = st.columns([1.5, 2, 2, 2.5, 1.5])
                    with r1:
                        st.write("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                        if st.button("BT0001", key="bt_1", help="link-btn"):
                            st.session_state.action_mode = 'view_bt_1'
                            st.rerun()
                    r2.markdown("<div class='row-col'>HD0001</div>", unsafe_allow_html=True)
                    r3.markdown("<div class='row-col'>Đang thẩm định</div>", unsafe_allow_html=True)
                    r4.markdown("<div class='row-col'><span class='pill-yellow'>Chưa có kết quả</span></div>", unsafe_allow_html=True)
                    r5.markdown("<div class='row-col'>7/6/2026</div>", unsafe_allow_html=True)
                    
                elif st.session_state.action_mode == 'view_bt_1':
                    # Chi tiết hồ sơ bồi thường
                    col_tt, col_cl = st.columns([9, 1])
                    if col_cl.button("✖", key="close_bt"):
                        st.session_state.action_mode = 'view'
                        st.rerun()
                        
                    c1, c2 = st.columns(2)
                    c1.markdown("<p style='font-size: 16px; line-height: 2;'><b>Mã hồ sơ Bồi thường:</b> KN0001<br><b>Hợp đồng bảo hiểm số:</b> HD0001<br><b>Mã hồ sơ bồi thường:</b> BT0001</p>", unsafe_allow_html=True)
                    c2.markdown("<p style='font-size: 16px; line-height: 2;'><b>Người được bảo hiểm:</b> Nguyễn Văn A<br><b>Sản phẩm:</b> PRU-Bảo vệ tối ưu<br><b>Hiệu lực:</b> 01/01/2025 - 01/01/2045</p>", unsafe_allow_html=True)
                    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                    
                    st.markdown("<h4 style='margin-bottom: 15px;'>Tài liệu đính kèm của hồ sơ</h4>", unsafe_allow_html=True)
                    docs_html = ""
                    for _ in range(7):
                        docs_html += "<span style='font-size: 40px; display:inline-block; margin-right: 15px; text-align: center;'>📄<br><span style='font-size: 11px; background: #ed1b2e; color: white; padding: 2px 4px; border-radius: 4px; font-weight: bold;'>PDF</span></span>"
                    st.markdown(f"<div>{docs_html}</div><p style='font-size: 14px; font-weight: bold; margin-top: 5px;'>Bệnh án...</p>", unsafe_allow_html=True)
                    
                    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
                    
                    # Cập nhật: Chia thành 3 cột để chứa thêm ô Số tiền được duyệt
                    c5, c6, c7 = st.columns([1.5, 2.5, 3.5])
                    c5.markdown("<h2>Kết quả</h2>", unsafe_allow_html=True)
                    with c6:
                        # Gán selectbox vào biến ket_qua_bt
                        ket_qua_bt = st.selectbox("Kết quả", ["Chưa có kết quả", "Chấp nhận bồi thường", "Từ chối bồi thường"], label_visibility="collapsed")
                    
                    with c7:
                        # Nếu chọn Chấp nhận bồi thường thì mới hiện khu vực nhập tiền
                        if ket_qua_bt == "Chấp nhận bồi thường":
                            c7_1, c7_2 = st.columns([1.2, 2])
                            c7_1.markdown("<p style='font-weight: bold; font-size: 16px; margin-top: 8px;'>Số tiền được duyệt:</p>", unsafe_allow_html=True)
                            c7_2.text_input("Số tiền", label_visibility="collapsed")
                    
                    st.write("<br>", unsafe_allow_html=True)
                    _, btn_col = st.columns([5, 1])
                    if btn_col.button("Cập nhật", type="primary", use_container_width=True):
                        st.success("Đã lưu kết quả bồi thường!")

        # --- 6. PHÒNG HỜ CÁC VAI TRÒ KHÁC CHƯA XÁC ĐỊNH ---
        else:
            # --- TAB THÔNG BÁO DÀNH CHO KHÁCH HÀNG (SỬA LẠI THÀNH IF) ---
            if st.session_state.dashboard_tab == 'thong_bao':
                col_title, col_space, col_btn = st.columns([5, 4, 1])
                
                with col_title:
                    st.markdown("<h2 style='color: #ff4b4b; margin-top: 0; padding-top: 0; font-weight: bold;'>Thư Báo</h2>", unsafe_allow_html=True)
                    
                # --- NÚT BỘ LỌC & SẮP XẾP CHO TAB THÔNG BÁO ---
                # CSS: Style chung cho các nút popover hình tròn
                st.markdown("""
                    <style>
                    [data-testid="stHorizontalBlock"]:has(#filter-sort-row-bell) div[data-testid="stPopover"] button {
                        width: 40px !important;
                        height: 40px !important;
                        border-radius: 50% !important;
                        background-color: #f2f2f5 !important;
                        border: 1px solid #ddd !important;
                        padding: 0 !important;
                        display: inline-flex !important;
                        align-items: center !important;
                        justify-content: center !important;
                        font-size: 18px !important;
                        color: #444 !important;
                        line-height: 1 !important;
                    }
                    [data-testid="stHorizontalBlock"]:has(#filter-sort-row-bell) div[data-testid="stPopover"] button svg {
                        display: none !important;
                    }
                    [data-testid="stHorizontalBlock"]:has(#filter-sort-row-bell) div[data-testid="stPopover"] button:hover {
                        background-color: #e5e5e5 !important;
                        border-color: #ed1b2e !important;
                        color: #ed1b2e !important;
                    }
                    </style>
                """, unsafe_allow_html=True)

                # Chia cột: 10 phần trống bên trái, 0.4 cho lọc, 0.2 cho khoảng cách, 0.4 cho sắp xếp
                _, col_filter, col_space, col_sort = st.columns([10, 0.4, 0.2, 0.4], gap="small")
                _.markdown('<span id="filter-sort-row-bell"></span>', unsafe_allow_html=True)

                # ==========================================
                # NÚT 1: BỘ LỌC DỮ LIỆU (Nằm trong col_filter)
                # ==========================================
                with col_filter:
                    with st.popover("▽"):
                        st.markdown("<p style='font-weight: bold; color: #ed1b2e; margin-bottom: 10px;'>BỘ LỌC DỮ LIỆU</p>", unsafe_allow_html=True)
                        c1, c2 = st.columns(2)
                        c1.selectbox("Tình trạng thư báo", ["Tất cả","Đã lên lịch", "Đã gửi"])
                        c2.selectbox("Loại thư báo", ["Tất cả","Yêu cầu chỉnh sửa", "Bổ sung hồ sơ", "Thông báo kết quả khiếu nại", "Thông báo kết quả bồi thường"])
                
                # ==========================================
                # NÚT 2: SẮP XẾP DỮ LIỆU (Nằm trong col_sort)
                # ==========================================
                with col_sort:
                    with st.popover("⇅"): # Vẫn để trống vì CSS đã gán ảnh nút chính
                        st.markdown("<p style='font-weight: bold; color: #111; margin-bottom: 15px; font-size: 16px;'>Sắp xếp theo</p>", unsafe_allow_html=True)
                        
                        # Cột 1: Lựa chọn Mới nhất
                        s1, s2 = st.columns([1, 4])
                        with s1:
                            if os.path.exists("new.png"):
                                st.image("new.png", width=40)
                        with s2:
                            if st.button("Mới nhất", key="sort_new_option", help="link-btn"):
                                pass
                                
                        # Cột 2: Lựa chọn Trễ nhất
                        s3, s4 = st.columns([1, 4])
                        with s3:
                            if os.path.exists("old.png"):
                                st.image("old.png", width=40)
                        with s4:
                            if st.button("Trễ nhất", key="sort_old_option", help="link-btn"):
                                pass
                        
                st.markdown("<hr style='margin-top: 0px; margin-bottom: 15px; border: none; border-top: 2px solid #333;'>", unsafe_allow_html=True)
                
                c1, c2 = st.columns([8, 2])
                with c1:
                    st.markdown("<p style='font-size: 20px; font-weight: bold; margin-bottom: 5px;'>[Tiêu đề thư]</p><p style='font-size: 16px;'>Nội dung thư báo khách hàng...</p>", unsafe_allow_html=True)
                with c2:
                    st.markdown("<p style='text-align: right; font-size: 15px;'>15:00 5/6/2025</p>", unsafe_allow_html=True)
                st.markdown("<hr style='margin-top: 15px; margin-bottom: 15px; border: none; border-top: 1px solid #aaa;'>", unsafe_allow_html=True)
            
            # --- NẾU KHÔNG BẤM CHUÔNG THÌ HIỆN DÒNG MÀU XANH ---
            else:
                # Dùng luôn biến role_label cho linh hoạt và xóa bớt dòng thừa
                st.info(f"Khu vực làm việc và dữ liệu của {role_label} đang được cập nhật liên kết cơ sở dữ liệu...")
