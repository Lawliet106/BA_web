import streamlit as st
import os
import random
import string
import base64
# ==========================================
# 1. CẤU HÌNH TRANG & KHỞI TẠO TRẠNG THÁI
# ==========================================
st.set_page_config(
    page_title="Prudential - Cổng thông tin & Quản lý bồi thường",
    page_icon="🔴",
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
                
                # NẾU ĐANG Ở TRANG NHÂN VIÊN -> Hiển thị Dropdown Chọn vai trò thay vì nút Đăng nhập
                if st.session_state.page == 'login_employee':
                    st.session_state.temp_vai_tro = st.selectbox(
                        "Chọn vai trò", 
                        options=["Nhân viên Chăm sóc khách hàng", "Nhân viên Xử lí khiếu nại", "Nhân viên Xử lí bồi thường"],
                        index=None, # Để trống mặc định
                        placeholder="Chọn vai trò", # Hiện chữ mờ giống y hệt ảnh của bạn
                        label_visibility="collapsed"
                    )
                
                # NẾU Ở CÁC TRANG KHÁC -> Hiện nút Popover Đăng nhập bình thường
                elif st.session_state.page not in ['login_customer', 'forgot_password']:
                    with st.popover("👤 Đăng nhập", use_container_width=True):
                        if st.button("Đối với Khách Hàng", use_container_width=True):
                            st.session_state.captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                            navigate_to('login_customer')
                        if st.button("Đối với Nhân Viên", use_container_width=True):
                            st.session_state.captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                            navigate_to('login_employee')
        
        # Menu điều hướng
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
            # Chỉnh lại chia cột để bỏ nút Đăng xuất, chỉ giữ lại chữ và chuông
            cols = st.columns([3, 3, 1])
            if st.session_state.role == 'customer':
                cols[0].markdown("<div style='text-align: right; font-size: 14px; cursor: pointer;'>Thông tin cá nhân</div>", unsafe_allow_html=True)
                cols[1].markdown("<div style='text-align: center; font-size: 14px; cursor: pointer;'>Hợp đồng bảo hiểm</div>", unsafe_allow_html=True)
            else:
                cols[1].markdown("<div style='text-align: right; font-size: 14px; cursor: pointer;'>Thông tin cá nhân</div>", unsafe_allow_html=True)
            
            cols[2].markdown("<div style='text-align: center; font-size: 20px;'>🔔</div>", unsafe_allow_html=True)

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
                    navigate_to('dashboard')
                else:
                    st.error("Mã bảo mật không chính xác. Vui lòng nhập lại!")
        
        # --- LINK ĐĂNG KÍ ---
        st.markdown("""
            <div style='text-align: center; margin-top: 10px; font-size: 15px; margin-bottom: 5px;'>
                <span style='color: #000;'>Chưa có tài khoản? </span>
                <a href='#' style='color: #ed1b2e; text-decoration: underline;'>Đăng kí</a>
            </div>
        """, unsafe_allow_html=True)
        
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
                    if vai_tro == "Nhân viên Chăm sóc khách hàng":
                        st.session_state.role = 'employee_cskh'
                    elif vai_tro == "Nhân viên Xử lí khiếu nại":
                        st.session_state.role = 'employee_xlkn'
                    elif vai_tro == "Nhân viên Xử lí bồi thường":
                        st.session_state.role = 'employee_xlbt'
                        
                    st.session_state.user_name = "Tên nhân viên"
                    navigate_to('dashboard')
                else:
                    st.error("Mã bảo mật không chính xác. Vui lòng nhập lại!")
        
        # --- LINK ĐĂNG KÍ VÀ QUÊN MẬT KHẨU ---
        st.markdown("""
            <div style='text-align: center; margin-top: 10px; font-size: 15px; margin-bottom: 5px;'>
                <span style='color: #000;'>Chưa có tài khoản? </span>
                <a href='#' style='color: #ed1b2e; text-decoration: underline;'>Đăng kí</a>
            </div>
        """, unsafe_allow_html=True)
        
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
    col_sid, col_cnt = st.columns([1, 2.8], gap="medium")
    
    with col_sid:
        # Xác định chức danh hiển thị
        if st.session_state.role == 'customer':
            role_label = "Khách hàng"
        elif st.session_state.role == 'employee_cskh':
            role_label = "Nhân viên Chăm sóc khách hàng"
        elif st.session_state.role == 'employee_xlkn':
            role_label = "Nhân viên Xử lí khiếu nại"
        elif st.session_state.role == 'employee_xlbt':
            role_label = "Nhân viên Xử lí bồi thường"
            
        # Profile Box
        st.markdown(f"""
            <div class="profile-box">
                <div class="profile-icon">👤</div>
                <div class="profile-name">{st.session_state.user_name}</div>
                <div class="profile-title" style="margin-bottom: 15px;">{"" if st.session_state.role == 'customer' else role_label}</div>
            </div>
        """, unsafe_allow_html=True)
        # Nút Đăng xuất 
        if st.button("Đăng xuất", key="logout_sidebar", use_container_width=True, type="primary"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.user_name = ""
            navigate_to('about')
        # Menu Box
        with st.container(border=True):
            st.markdown("<div class='menu-title'>Menu</div>", unsafe_allow_html=True)
            
            # Phân luồng Menu theo đúng 3 loại nhân viên + 1 khách hàng
            if st.session_state.role == 'customer':
                items = [("📁 Hồ sơ khiếu nại", "#"), ("📁 Hồ sơ bồi thường", "#")]
            elif st.session_state.role == 'employee_cskh':
                items = [("📁 Quản lí thư báo", "#"), ("📁 Quản lí tài khoản", "#"), ("📁 Quản lí hợp đồng bảo hiểm", "#")]
            elif st.session_state.role == 'employee_xlkn':
                items = [("📁 Quản lí hồ sơ khiếu nại", "#")]
            elif st.session_state.role == 'employee_xlbt':
                items = [("📁 Quản lí hồ sơ bồi thường", "#")]
            
            for item, link in items:
                st.markdown(f"<a href='{link}' class='menu-item' style='text-decoration: none;'>{item}</a>", unsafe_allow_html=True)

    with col_cnt:
        # Main Dashboard Image
        safe_image("dashboard.jpg")