"""
🌿 Crop Disease & Risk Detection System — Main Streamlit Application

Premium dark-themed UI with glassmorphism, multi-page navigation,
authentication, and full AI-powered disease analysis pipeline.
"""
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import json
import time

# Local modules
import auth
import database
import image_model
import llm_engine
import config

# ─── PAGE CONFIG ───
st.set_page_config(
    page_title="CropGuard AI — Disease Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─── CUSTOM CSS ───
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ── Global ── */
    *, html, body, .stApp, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif !important;
    }
    .stApp {
        background: linear-gradient(145deg, #070B14 0%, #0B1121 40%, #0D1528 100%);
    }
    [data-testid="stHeader"] { background: transparent; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A1628 0%, #0F1D32 50%, #0A1628 100%) !important;
        border-right: 1px solid rgba(16, 185, 129, 0.15);
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #E2E8F0 !important;
    }

    /* ── Headings ── */
    h1, h2, h3 { color: #F0FDF4 !important; letter-spacing: -0.02em; }
    h1 { font-weight: 800 !important; }
    p, li, label, .stMarkdown { color: #CBD5E1 !important; }

    /* ── Glass Cards ── */
    .glass-card {
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 16px;
        transition: all 0.35s cubic-bezier(.4,0,.2,1);
    }
    .glass-card:hover {
        border-color: rgba(16,185,129,0.25);
        box-shadow: 0 8px 32px rgba(16,185,129,0.08);
        transform: translateY(-2px);
    }

    /* ── Stat Cards ── */
    .stat-card {
        background: linear-gradient(135deg, rgba(16,185,129,0.08) 0%, rgba(6,214,160,0.04) 100%);
        border: 1px solid rgba(16,185,129,0.15);
        border-radius: 14px;
        padding: 22px 18px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(16,185,129,0.12);
        border-color: rgba(16,185,129,0.35);
    }
    .stat-number {
        font-size: 2.4em;
        font-weight: 800;
        background: linear-gradient(135deg, #10B981, #06D6A0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }
    .stat-label {
        font-size: 0.85em;
        color: #94A3B8 !important;
        margin-top: 6px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ── Risk Badges ── */
    .risk-badge {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 24px;
        font-weight: 700;
        font-size: 0.85em;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .risk-low { background: rgba(16,185,129,0.15); color: #34D399; border: 1px solid rgba(16,185,129,0.3); }
    .risk-medium { background: rgba(245,158,11,0.15); color: #FBBF24; border: 1px solid rgba(245,158,11,0.3); }
    .risk-high { background: rgba(239,68,68,0.15); color: #F87171; border: 1px solid rgba(239,68,68,0.3); }
    .risk-critical { background: rgba(220,38,38,0.2); color: #FCA5A5; border: 1px solid rgba(220,38,38,0.4); animation: pulse-danger 2s infinite; }
    @keyframes pulse-danger {
        0%, 100% { box-shadow: 0 0 0 0 rgba(220,38,38,0.3); }
        50% { box-shadow: 0 0 16px 4px rgba(220,38,38,0.15); }
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6em 1.6em !important;
        font-weight: 600 !important;
        font-size: 1em !important;
        transition: all 0.3s cubic-bezier(.4,0,.2,1) !important;
        box-shadow: 0 2px 8px rgba(16,185,129,0.2) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(16,185,129,0.3) !important;
        background: linear-gradient(135deg, #34D399 0%, #10B981 100%) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Secondary / danger buttons */
    .logout-btn button {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
        box-shadow: 0 2px 8px rgba(239,68,68,0.2) !important;
    }
    .logout-btn button:hover {
        box-shadow: 0 6px 20px rgba(239,68,68,0.3) !important;
        background: linear-gradient(135deg, #F87171 0%, #EF4444 100%) !important;
    }

    /* ── Form Inputs ── */
    .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox > div > div {
        background-color: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: #E2E8F0 !important;
        transition: border-color 0.3s ease !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: rgba(16,185,129,0.5) !important;
        box-shadow: 0 0 0 2px rgba(16,185,129,0.1) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(16,185,129,0.15) !important;
        color: #10B981 !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* ── Divider ── */
    hr { border-color: rgba(255,255,255,0.06) !important; }

    /* ── File Uploader ── */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.02);
        border: 2px dashed rgba(16,185,129,0.2);
        border-radius: 14px;
        padding: 20px;
        transition: border-color 0.3s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(16,185,129,0.4);
    }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #10B981 !important; }

    /* ── Success / Error / Info boxes ── */
    .stAlert { border-radius: 12px !important; }

    /* ── Auth Page Styles ── */
    .auth-container {
        max-width: 440px;
        margin: 40px auto;
    }
    .auth-header {
        text-align: center;
        margin-bottom: 32px;
    }
    .auth-header h1 {
        font-size: 2.6em;
        margin-bottom: 8px;
    }
    .brand-gradient {
        background: linear-gradient(135deg, #10B981 0%, #06D6A0 50%, #34D399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    .auth-subtitle {
        color: #64748B !important;
        font-size: 1.05em;
    }

    /* ── Results Section ── */
    .result-header {
        font-size: 1.5em;
        font-weight: 700;
        color: #F0FDF4 !important;
        margin-bottom: 4px;
    }
    .remedy-card {
        background: rgba(16,185,129,0.06);
        border: 1px solid rgba(16,185,129,0.12);
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .chemical-card {
        background: rgba(245,158,11,0.06);
        border: 1px solid rgba(245,158,11,0.12);
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .alert-card {
        background: rgba(239,68,68,0.06);
        border: 1px solid rgba(239,68,68,0.15);
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
    }

    /* ── Confidence Meter ── */
    .confidence-bar {
        height: 10px;
        border-radius: 5px;
        background: rgba(255,255,255,0.06);
        overflow: hidden;
        margin: 8px 0;
    }
    .confidence-fill {
        height: 100%;
        border-radius: 5px;
        transition: width 1s ease-in-out;
    }
    .conf-high { background: linear-gradient(90deg, #10B981, #06D6A0); }
    .conf-medium { background: linear-gradient(90deg, #F59E0B, #FBBF24); }
    .conf-low { background: linear-gradient(90deg, #EF4444, #F87171); }

    /* ── History Card ── */
    .history-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 12px;
        transition: all 0.3s;
    }
    .history-card:hover {
        border-color: rgba(16,185,129,0.2);
        background: rgba(255,255,255,0.05);
    }

    /* ── Hide default Streamlit elements ── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


# ─── HELPER FUNCTIONS ───
import textwrap


def render_html(html_str: str):
    """Safely render HTML in Streamlit without indentation causing Markdown code blocks."""
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)


def risk_badge(level: str) -> str:
    css_class = f"risk-{level.lower()}" if level else "risk-medium"
    return f'<span class="risk-badge {css_class}">{level}</span>'


def confidence_bar(value: float) -> str:
    if value >= 75:
        css_class = "conf-high"
    elif value >= 50:
        css_class = "conf-medium"
    else:
        css_class = "conf-low"
    return f'<div class="confidence-bar"><div class="confidence-fill {css_class}" style="width: {value}%;"></div></div>'


def stat_card(number, label, emoji=""):
    return f'<div class="stat-card"><div class="stat-number">{emoji} {number}</div><div class="stat-label">{label}</div></div>'


# ─── AUTH PAGE ───
def auth_page():
    st.markdown("""
    <div class="auth-header">
        <h1>🌿 <span class="brand-gradient">CropGuard AI</span></h1>
        <p class="auth-subtitle">AI-Powered Crop Disease Detection & Risk Assessment</p>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab_login:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Welcome Back")
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email", placeholder="farmer@example.com", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")
            submit = st.form_submit_button("🔓 Log In", use_container_width=True)

            if submit:
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    with st.spinner("Authenticating..."):
                        result = auth.sign_in(email, password)
                    if result["success"]:
                        auth.init_session(result["user"], result["session"], result["profile"])
                        st.success(result["message"])
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(result["message"])
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_signup:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Create Your Account")
        with st.form("signup_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name *", placeholder="Rajesh Kumar", key="signup_name")
                email = st.text_input("Email *", placeholder="farmer@example.com", key="signup_email")
                password = st.text_input("Password *", type="password", placeholder="Min 6 characters", key="signup_pass")
            with col2:
                phone = st.text_input("Phone Number", placeholder="+91 9876543210", key="signup_phone")
                farm_location = st.text_input("Farm Location", placeholder="Nashik, Maharashtra", key="signup_location")
                st.markdown("<br>", unsafe_allow_html=True)
                col_lat, col_lon = st.columns(2)
                with col_lat:
                    latitude = st.number_input("Latitude", value=None, format="%.6f", key="signup_lat", help="Optional — used for nearby alerts")
                with col_lon:
                    longitude = st.number_input("Longitude", value=None, format="%.6f", key="signup_lon", help="Optional — used for nearby alerts")

            submit = st.form_submit_button("🌱 Create Account", use_container_width=True)

            if submit:
                if not full_name or not email or not password:
                    st.error("Please fill in all required fields (*).")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    with st.spinner("Creating your account..."):
                        result = auth.sign_up(
                            email=email, password=password, full_name=full_name,
                            phone=phone, farm_location=farm_location,
                            latitude=latitude, longitude=longitude,
                        )
                    if result["success"]:
                        st.success(result["message"])
                    else:
                        st.error(result["message"])
        st.markdown('</div>', unsafe_allow_html=True)


# ─── DASHBOARD PAGE ───
def dashboard_page():
    user_name = st.session_state.get("user_name", "Farmer")
    st.markdown(f"""
    <h1 style="font-size:2.2em; margin-bottom:4px;">
        👋 Welcome back, <span class="brand-gradient">{user_name}</span>
    </h1>
    <p style="color:#64748B !important; font-size:1.05em;">Here's your farm health overview</p>
    """, unsafe_allow_html=True)

    # Stats
    user_id = auth.get_current_user_id()
    stats = database.get_user_stats(user_id)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(stat_card(stats["total_scans"], "Total Scans", "📊"), unsafe_allow_html=True)
    with col2:
        st.markdown(stat_card(stats["diseases_found"], "Diseases Found", "🦠"), unsafe_allow_html=True)
    with col3:
        st.markdown(stat_card(stats["healthy_scans"], "Healthy Crops", "✅"), unsafe_allow_html=True)
    with col4:
        st.markdown(stat_card(stats["high_risk_alerts"], "High Risk Alerts", "🚨"), unsafe_allow_html=True)

    st.markdown("---")

    # Nearby Alerts Section
    profile = auth.get_current_profile()
    lat = profile.get("latitude")
    lon = profile.get("longitude")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("### 📋 Recent Scans")
        reports = database.get_user_reports(user_id, limit=5)
        if reports:
            for report in reports:
                disease = report.get("predicted_disease", "Unknown")
                risk = report.get("risk_level", "Medium")
                conf = report.get("model_confidence", 0)
                date = report.get("created_at", "")[:10]
                is_healthy = "Healthy" in disease
                icon = "✅" if is_healthy else "⚠️"

                st.markdown(f"""
                <div class="history-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="font-size:1.15em; font-weight:600; color:#F0FDF4 !important;">{icon} {disease}</span>
                            <br><span style="color:#64748B; font-size:0.85em;">📅 {date} &nbsp;|&nbsp; 🎯 {conf:.0f}% confidence</span>
                        </div>
                        <div>{risk_badge(risk) if not is_healthy else risk_badge("Low")}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🌱 No scans yet. Go to **New Scan** to analyze your first crop!")

    with col_right:
        st.markdown("### 🗺️ Nearby Alerts")
        if lat and lon:
            nearby = database.get_nearby_disease_reports(lat, lon)
            if nearby:
                for alert in nearby[:5]:
                    alert_disease = alert.get("predicted_disease", "Unknown")
                    dist = alert.get("distance_km", 0)
                    st.markdown(f"""
                    <div class="alert-card">
                        <span style="font-weight:600; color:#FCA5A5;">⚠️ {alert_disease}</span><br>
                        <span style="color:#94A3B8; font-size:0.85em;">📍 {dist:.1f} km away</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ No disease outbreaks reported nearby. Your area looks safe!")
                if st.button("🧪 Simulate Nearby Outbreak (2.5km away)", key="demo_nearby_alert_btn", use_container_width=True):
                    database.save_disease_report(
                        user_id=user_id,
                        predicted_disease="Tomato - Late Blight",
                        model_confidence=94.2,
                        top3_predictions=[{"class": "Tomato___Late_blight", "probability": 94.2}],
                        latitude=float(lat) + 0.015,
                        longitude=float(lon) + 0.015,
                        region="Adjacent Farm Sector",
                        risk_level="High",
                        llm_diagnosis="Late Blight Outbreak detected in neighboring farm"
                    )
                    st.rerun()
        else:
            st.warning("📍 Add your GPS coordinates in **Profile** to see nearby alerts.")


# ─── NEW SCAN PAGE ───
def new_scan_page():
    st.markdown("""
    <h1 style="font-size:2em;">🔬 New Disease Scan</h1>
    <p style="color:#64748B;">Upload a leaf image and provide details for a comprehensive AI analysis</p>
    """, unsafe_allow_html=True)

    # Load model
    model, class_names = image_model.load_model()
    if model is None:
        st.error("⚠️ Model not found! Please ensure `crop_disease_model.pth` exists.")
        return

    # ── Step 1: Image Upload ──
    st.markdown("### 📸 Step 1: Upload Leaf Image")
    uploaded_file = st.file_uploader(
        "Choose a leaf image...", type=["jpg", "jpeg", "png"],
        help="Upload a clear photo of the affected leaf for best results"
    )

    prediction = None
    if uploaded_file:
        col_img, col_pred = st.columns([1, 1])
        with col_img:
            pil_image = Image.open(uploaded_file)
            st.image(pil_image, caption="Uploaded Leaf Image", use_container_width=True)

        with col_pred:
            with st.spinner("🔍 Analyzing image with AI model..."):
                prediction = image_model.predict(model, class_names, pil_image)

            top3_html_parts = []
            for item in prediction["top3"]:
                prob = item["probability"]
                top3_html_parts.append(
                    f'<div style="margin:6px 0; padding:8px 12px; background:rgba(255,255,255,0.03); border-radius:8px;">'
                    f'<div style="display:flex; justify-content:space-between; margin-bottom:4px;">'
                    f'<span style="color:#CBD5E1; font-size:0.9em;">{item["class"]}</span>'
                    f'<span style="color:#10B981; font-weight:600; font-size:0.9em;">{prob:.1f}%</span>'
                    f'</div>'
                    f'{confidence_bar(prob)}'
                    f'</div>'
                )
            top3_html = "".join(top3_html_parts)

            render_html(f"""
            <div class="glass-card">
                <div class="result-header">🎯 Image Model Prediction</div>
                <p style="font-size:1.3em; font-weight:700; color:#10B981 !important; margin:8px 0;">
                    {prediction['predicted_class']}
                </p>
                <p style="color:#94A3B8; margin-bottom:4px;">Confidence: <strong style="color:#E2E8F0;">{prediction['confidence']:.1f}%</strong></p>
                {confidence_bar(prediction['confidence'])}
                <p style="color:#94A3B8; font-size:0.9em; margin-top:14px; margin-bottom:6px;">Top 3 Predictions:</p>
                {top3_html}
            </div>
            """)

            if st.button("💾 Save Image Scan to History & Dashboard", key="quick_save_btn", use_container_width=True):
                user_id = auth.get_current_user_id()
                lat_val = profile.get("latitude") or 28.7187
                lon_val = profile.get("longitude") or 77.0662
                is_h = "healthy" in prediction["predicted_class"].lower()
                q_res = database.save_disease_report(
                    user_id=user_id,
                    predicted_disease=prediction["predicted_class"],
                    model_confidence=prediction["confidence"],
                    top3_predictions=prediction["top3"],
                    latitude=lat_val,
                    longitude=lon_val,
                    region=profile.get("farm_location", ""),
                    risk_level="Low" if is_h else "Medium",
                    llm_diagnosis=prediction["predicted_class"] + " (Visual Detection)"
                )
                if q_res.get("success"):
                    st.success("✅ Saved to Scan History and Dashboard!")
                else:
                    st.error(f"Failed to save: {q_res.get('error')}")

    if prediction is None:
        return

    st.markdown("---")

    # ── Step 2: Farmer Input ──
    st.markdown("### 🧑‍🌾 Step 2: Farmer Observations")
    st.caption("Fill in as much as you can — more data = better diagnosis")

    with st.expander("🌾 Crop & Symptom Details", expanded=True):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            crop_type = st.selectbox("Crop Type", [
                "", "Apple", "Bell Pepper", "Cherry", "Corn (Maize)",
                "Grape", "Peach", "Potato", "Strawberry", "Tomato", "Other"
            ], help="Select the crop you are growing")
            growth_stage = st.selectbox("Growth Stage", [
                "", "Seedling", "Vegetative", "Flowering", "Fruiting",
                "Mature / Harvest Ready"
            ])
            visible_symptoms = st.text_area(
                "Describe Visible Symptoms",
                placeholder="e.g., Yellow spots on leaves, wilting, fruit rot...",
                height=100
            )
        with f_col2:
            crop_variety = st.text_input("Crop Variety (optional)", placeholder="e.g., Roma tomato, Russet potato")
            pest_presence = st.selectbox("Pest/Insect Presence?", [
                "", "None observed", "Aphids", "Whiteflies", "Caterpillars",
                "Beetles", "Mites", "Fruit flies", "Other insects"
            ])
            pesticide_use = st.text_input("Recent Pesticide Use", placeholder="e.g., Neem oil spray 3 days ago")

    with st.expander("💧 Irrigation & Fertilizer"):
        ir_col1, ir_col2 = st.columns(2)
        with ir_col1:
            irrigation_type = st.selectbox("Irrigation Type", [
                "", "Drip", "Flood/Furrow", "Sprinkler/Overhead",
                "Rainfed", "Manual watering"
            ])
        with ir_col2:
            fertilizer_history = st.text_input(
                "Recent Fertilizer Application",
                placeholder="e.g., DAP applied 2 weeks ago"
            )

    # ── Step 3: Environment & Soil ──
    st.markdown("### 🌡️ Step 3: Environment & Soil Data")
    st.caption("Enter values if known — leave blank if unavailable")

    with st.expander("🌤️ Weather Conditions", expanded=False):
        e_col1, e_col2, e_col3 = st.columns(3)
        with e_col1:
            temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=55.0, value=None, format="%.1f")
        with e_col2:
            humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=None, format="%.1f")
        with e_col3:
            rainfall = st.number_input("Recent Rainfall (mm)", min_value=0.0, max_value=500.0, value=None, format="%.1f")

    with st.expander("🧪 Soil Data", expanded=False):
        s_col1, s_col2, s_col3, s_col4 = st.columns(4)
        with s_col1:
            soil_moisture = st.number_input("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=None, format="%.1f")
        with s_col2:
            soil_ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=None, format="%.1f")
        with s_col3:
            nitrogen = st.number_input("Nitrogen (kg/ha)", min_value=0.0, max_value=500.0, value=None, format="%.1f")
        with s_col4:
            phosphorus = st.number_input("Phosphorus (kg/ha)", min_value=0.0, max_value=500.0, value=None, format="%.1f")
        potassium = st.number_input("Potassium (kg/ha)", min_value=0.0, max_value=500.0, value=None, format="%.1f")

    # ── Step 4: Location ──
    st.markdown("### 📍 Step 4: Location")
    profile = auth.get_current_profile()
    loc_col1, loc_col2, loc_col3 = st.columns([2, 2, 2])
    with loc_col1:
        scan_lat = st.number_input(
            "Latitude", value=profile.get("latitude"),
            format="%.6f", key="scan_lat",
            help="Your GPS latitude (used for nearby disease search)"
        )
    with loc_col2:
        scan_lon = st.number_input(
            "Longitude", value=profile.get("longitude"),
            format="%.6f", key="scan_lon",
            help="Your GPS longitude"
        )
    with loc_col3:
        region = st.text_input("Region / District", value=profile.get("farm_location", ""), key="scan_region")

    st.markdown("---")

    # ── Run Full Analysis ──
    st.markdown("### 🚀 Run Complete AI Analysis")
    st.caption("Combines image prediction + your inputs + nearby alerts + disease knowledge base → LLM diagnosis")

    if st.button("🧠 Analyze with AI", use_container_width=True, type="primary"):
        # Collect all inputs
        farmer_inputs = {
            "crop_type": crop_type,
            "crop_variety": crop_variety,
            "growth_stage": growth_stage,
            "visible_symptoms": visible_symptoms,
            "irrigation_type": irrigation_type,
            "fertilizer_history": fertilizer_history,
            "pesticide_use": pesticide_use,
            "pest_presence": pest_presence,
        }

        environment_data = {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall,
            "soil_moisture": soil_moisture,
            "soil_ph": soil_ph,
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium,
        }

        # Fetch nearby alerts
        nearby_alerts = []
        if scan_lat and scan_lon:
            with st.spinner("🗺️ Searching for nearby disease reports..."):
                nearby_alerts = database.get_nearby_disease_reports(scan_lat, scan_lon)
                if nearby_alerts:
                    st.warning(f"⚠️ Found **{len(nearby_alerts)} disease report(s)** within {config.NEARBY_RADIUS_KM}km!")

        # Run LLM analysis
        with st.spinner("🤖 Running AI analysis — synthesizing all data..."):
            llm_result = llm_engine.analyze_with_llm(
                prediction=prediction,
                farmer_inputs=farmer_inputs,
                environment_data=environment_data,
                nearby_alerts=nearby_alerts,
            )

        # ── Display Results ──
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")

        # Header row: Diagnosis + Risk + Confidence
        res_col1, res_col2, res_col3 = st.columns([3, 1, 1])
        with res_col1:
            diagnosis = llm_result.get("final_diagnosis", prediction["predicted_class"])
            is_healthy = "Healthy" in diagnosis or "healthy" in diagnosis
            icon = "✅" if is_healthy else "🦠"
            st.markdown(f"""
            <div class="glass-card">
                <p style="color:#94A3B8; font-size:0.85em; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.05em;">Final AI Diagnosis</p>
                <p style="font-size:1.8em; font-weight:800; color:{'#34D399' if is_healthy else '#F87171'} !important; margin:0;">
                    {icon} {diagnosis}
                </p>
            </div>
            """, unsafe_allow_html=True)
        with res_col2:
            risk = llm_result.get("risk_level", "Medium")
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <p style="color:#94A3B8; font-size:0.85em; margin-bottom:8px; text-transform:uppercase;">Risk Level</p>
                {risk_badge(risk)}
            </div>
            """, unsafe_allow_html=True)
        with res_col3:
            conf = llm_result.get("confidence", "Medium")
            conf_icon = "🟢" if conf == "High" else ("🟡" if conf == "Medium" else "🔴")
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <p style="color:#94A3B8; font-size:0.85em; margin-bottom:8px; text-transform:uppercase;">Confidence</p>
                <span style="font-size:1.3em; font-weight:700; color:#E2E8F0;">{conf_icon} {conf}</span>
            </div>
            """, unsafe_allow_html=True)

        # Detailed Analysis
        st.markdown(f"""
        <div class="glass-card">
            <p style="font-weight:700; font-size:1.1em; color:#F0FDF4 !important;">🔍 Detailed Analysis</p>
            <p style="color:#CBD5E1; line-height:1.7;">{llm_result.get('detailed_analysis', 'No detailed analysis available.')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Confidence & Risk Explanations
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            st.markdown(f"""
            <div class="glass-card">
                <p style="font-weight:600; color:#34D399 !important;">💡 Confidence Explanation</p>
                <p style="color:#CBD5E1; font-size:0.95em;">{llm_result.get('confidence_explanation', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        with exp_col2:
            st.markdown(f"""
            <div class="glass-card">
                <p style="font-weight:600; color:#FBBF24 !important;">⚡ Risk Explanation</p>
                <p style="color:#CBD5E1; font-size:0.95em;">{llm_result.get('risk_explanation', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)

        # Immediate Actions
        actions = llm_result.get("immediate_actions", [])
        if actions and actions != ["Not available"]:
            st.markdown(f"""
            <div class="alert-card">
                <p style="font-weight:700; color:#FCA5A5 !important; font-size:1.1em;">🚨 Immediate Actions Required</p>
            </div>
            """, unsafe_allow_html=True)
            for i, action in enumerate(actions, 1):
                st.markdown(f"**{i}.** {action}")

        # Remedies Tabs
        st.markdown("### 💊 Remedies & Solutions")
        rem_tab1, rem_tab2, rem_tab3 = st.tabs(["🌿 Organic Remedies", "🧪 Chemical Treatments", "🛡️ Prevention"])

        with rem_tab1:
            organic = llm_result.get("organic_remedies", [])
            if organic:
                for remedy in organic:
                    st.markdown(f"""
                    <div class="remedy-card">
                        <span style="color:#34D399;">🌿</span> <span style="color:#E2E8F0;">{remedy}</span>
                    </div>
                    """, unsafe_allow_html=True)

        with rem_tab2:
            chemical = llm_result.get("chemical_treatments", [])
            if chemical:
                for treatment in chemical:
                    st.markdown(f"""
                    <div class="chemical-card">
                        <span style="color:#FBBF24;">🧪</span> <span style="color:#E2E8F0;">{treatment}</span>
                    </div>
                    """, unsafe_allow_html=True)

        with rem_tab3:
            preventive = llm_result.get("preventive_measures", [])
            if preventive:
                for measure in preventive:
                    st.markdown(f"""
                    <div class="glass-card" style="padding:14px 20px; margin-bottom:8px;">
                        <span style="color:#60A5FA;">🛡️</span> <span style="color:#E2E8F0;">{measure}</span>
                    </div>
                    """, unsafe_allow_html=True)

        # Nearby Alert Assessment
        nearby_assessment = llm_result.get("nearby_alert_assessment", "No nearby alerts")
        if nearby_assessment and nearby_assessment != "Not available" and nearby_assessment != "No nearby alerts":
            st.markdown(f"""
            <div class="alert-card">
                <p style="font-weight:700; color:#FCA5A5 !important;">🗺️ Nearby Outbreak Assessment</p>
                <p style="color:#E2E8F0;">{nearby_assessment}</p>
            </div>
            """, unsafe_allow_html=True)

        # Additional Notes
        notes = llm_result.get("additional_notes", "")
        if notes and notes != "Not available":
            st.info(f"📝 **Additional Notes:** {notes}")

        # ── Automatically Save Report ──
        user_id = auth.get_current_user_id()
        image_url = ""
        if uploaded_file:
            try:
                uploaded_file.seek(0)
                image_url = database.upload_leaf_image(
                    uploaded_file.read(), uploaded_file.name, user_id
                )
            except Exception as e:
                print(f"Image upload note: {e}")

        save_result = database.save_disease_report(
            user_id=user_id,
            predicted_disease=prediction["predicted_class"],
            model_confidence=prediction["confidence"],
            top3_predictions=prediction["top3"],
            crop_type=crop_type, crop_variety=crop_variety,
            growth_stage=growth_stage, visible_symptoms=visible_symptoms,
            irrigation_type=irrigation_type, fertilizer_history=fertilizer_history,
            pesticide_use=pesticide_use, pest_presence=pest_presence,
            temperature=temperature, humidity=humidity, rainfall=rainfall,
            soil_moisture=soil_moisture, soil_ph=soil_ph,
            nitrogen=nitrogen, phosphorus=phosphorus, potassium=potassium,
            latitude=scan_lat, longitude=scan_lon, region=region,
            llm_diagnosis=llm_result.get("final_diagnosis"),
            llm_confidence=llm_result.get("confidence"),
            llm_remedies=json.dumps({
                "organic": llm_result.get("organic_remedies", []),
                "chemical": llm_result.get("chemical_treatments", []),
                "preventive": llm_result.get("preventive_measures", []),
            }),
            risk_level=llm_result.get("risk_level"),
            nearby_alerts=nearby_alerts,
            image_url=image_url,
        )

        st.markdown("---")
        if save_result.get("success"):
            st.success("✅ **Report Automatically Saved!** View it anytime in **Dashboard** or **Scan History**.")
            st.balloons()
        else:
            err = save_result.get("error", "Unknown error")
            st.error(f"⚠️ Could not save to database: {err}")
            if "row-level security" in err.lower() or "42501" in err:
                st.info("💡 **Supabase Fix Needed:** Please run the SQL command in Supabase SQL Editor to allow saving disease reports (see instructions in chat).")


# ─── HISTORY PAGE ───
def history_page():
    st.markdown("""
    <h1 style="font-size:2em;">📋 Scan History</h1>
    <p style="color:#64748B;">All your past disease scans and analyses</p>
    """, unsafe_allow_html=True)

    user_id = auth.get_current_user_id()
    reports = database.get_user_reports(user_id, limit=50)

    if not reports:
        st.info("🌱 No scans yet. Go to **New Scan** to get started!")
        return

    # Filters
    filter_col1, filter_col2 = st.columns([1, 1])
    with filter_col1:
        risk_filter = st.selectbox("Filter by Risk", ["All", "Low", "Medium", "High", "Critical"])
    with filter_col2:
        disease_filter = st.selectbox("Filter by Status", ["All", "Diseased", "Healthy"])

    filtered = reports
    if risk_filter != "All":
        filtered = [r for r in filtered if r.get("risk_level") == risk_filter]
    if disease_filter == "Diseased":
        filtered = [r for r in filtered if "Healthy" not in r.get("predicted_disease", "")]
    elif disease_filter == "Healthy":
        filtered = [r for r in filtered if "Healthy" in r.get("predicted_disease", "")]

    st.markdown(f"**Showing {len(filtered)} report(s)**")

    for report in filtered:
        disease = report.get("predicted_disease", "Unknown")
        risk = report.get("risk_level", "N/A")
        conf = report.get("model_confidence", 0)
        date = report.get("created_at", "")[:16].replace("T", " at ")
        crop = report.get("crop_type", "")
        is_healthy = "Healthy" in disease

        st.markdown(f"""
        <div class="history-card">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                <div>
                    <span style="font-size:1.2em; font-weight:700; color:#F0FDF4 !important;">
                        {"✅" if is_healthy else "⚠️"} {disease}
                    </span>
                    <br>
                    <span style="color:#64748B; font-size:0.85em;">
                        📅 {date} &nbsp;|&nbsp; 🎯 {conf:.0f}% &nbsp;|&nbsp; 🌾 {crop or 'N/A'}
                    </span>
                </div>
                <div>{risk_badge(risk)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"📄 View Details — {disease} ({date[:10]})", expanded=False):
            det_col1, det_col2 = st.columns(2)
            with det_col1:
                st.markdown("**🧑‍🌾 Farmer Input**")
                st.write(f"- Crop: {crop or 'N/A'}")
                st.write(f"- Variety: {report.get('crop_variety', 'N/A')}")
                st.write(f"- Growth Stage: {report.get('growth_stage', 'N/A')}")
                st.write(f"- Symptoms: {report.get('visible_symptoms', 'N/A')}")
                st.write(f"- Pest: {report.get('pest_presence', 'N/A')}")
            with det_col2:
                st.markdown("**🌡️ Environment**")
                st.write(f"- Temp: {report.get('temperature', 'N/A')}°C")
                st.write(f"- Humidity: {report.get('humidity', 'N/A')}%")
                st.write(f"- Soil pH: {report.get('soil_ph', 'N/A')}")
                st.write(f"- Region: {report.get('region', 'N/A')}")

            llm_diag = report.get("llm_diagnosis")
            if llm_diag:
                st.markdown(f"**🤖 AI Diagnosis:** {llm_diag}")
            remedies_json = report.get("llm_remedies")
            if remedies_json:
                try:
                    remedies = json.loads(remedies_json) if isinstance(remedies_json, str) else remedies_json
                    if remedies.get("organic"):
                        st.markdown("**🌿 Organic Remedies:**")
                        for r in remedies["organic"]:
                            st.write(f"  - {r}")
                except (json.JSONDecodeError, AttributeError):
                    pass


# ─── PROFILE PAGE ───
def profile_page():
    st.markdown("""
    <h1 style="font-size:2em;">👤 Your Profile</h1>
    <p style="color:#64748B;">Manage your account and farm details</p>
    """, unsafe_allow_html=True)

    profile = auth.get_current_profile()
    user_email = st.session_state.get("user_email", "")

    st.markdown(f"""
    <div class="glass-card">
        <div style="display:flex; align-items:center; gap:20px;">
            <div style="width:64px; height:64px; border-radius:50%;
                        background:linear-gradient(135deg, #10B981, #06D6A0);
                        display:flex; align-items:center; justify-content:center;
                        font-size:1.5em; font-weight:800; color:#fff;">
                {profile.get('full_name', 'U')[0].upper()}
            </div>
            <div>
                <p style="font-size:1.4em; font-weight:700; color:#F0FDF4 !important; margin:0;">
                    {profile.get('full_name', 'User')}
                </p>
                <p style="color:#64748B !important; margin:0;">📧 {user_email}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✏️ Edit Profile")
    with st.form("profile_form"):
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            new_name = st.text_input("Full Name", value=profile.get("full_name", ""))
            new_phone = st.text_input("Phone", value=profile.get("phone", ""))
            new_location = st.text_input("Farm Location", value=profile.get("farm_location", ""))
        with p_col2:
            new_lat = st.number_input("Latitude", value=profile.get("latitude"), format="%.6f")
            new_lon = st.number_input("Longitude", value=profile.get("longitude"), format="%.6f")

        if st.form_submit_button("💾 Save Changes", use_container_width=True):
            updates = {
                "full_name": new_name,
                "phone": new_phone,
                "farm_location": new_location,
                "latitude": new_lat,
                "longitude": new_lon,
            }
            result = database.update_user_profile(auth.get_current_user_id(), updates)
            if result.get("success"):
                st.session_state["profile"].update(updates)
                st.session_state["user_name"] = new_name
                st.success("✅ Profile updated!")
            else:
                st.error(f"Update failed: {result.get('error', 'Unknown error')}")


# ─── SIDEBAR & NAVIGATION ───
def sidebar_nav():
    with st.sidebar:
        # Brand
        st.markdown("""
        <div style="text-align:center; padding:16px 0 24px 0;">
            <span style="font-size:2em;">🌿</span>
            <h2 style="margin:4px 0 0 0;">
                <span class="brand-gradient">CropGuard AI</span>
            </h2>
            <p style="color:#4B5563; font-size:0.8em; margin:0;">Disease Detection System</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # User info
        user_name = st.session_state.get("user_name", "User")
        user_email = st.session_state.get("user_email", "")
        st.markdown(f"""
        <div style="padding:8px 12px; background:rgba(16,185,129,0.06);
                    border-radius:10px; border:1px solid rgba(16,185,129,0.1); margin-bottom:16px;">
            <span style="font-weight:600; color:#E2E8F0; font-size:0.95em;">👤 {user_name}</span><br>
            <span style="color:#64748B; font-size:0.78em;">{user_email}</span>
        </div>
        """, unsafe_allow_html=True)

        # Navigation
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "New Scan", "History", "Profile"],
            icons=["house-fill", "camera-fill", "clock-history", "person-circle"],
            default_index=0,
            styles={
                "container": {"padding": "0", "background-color": "transparent"},
                "icon": {"color": "#10B981", "font-size": "1.1em"},
                "nav-link": {
                    "font-size": "0.95em",
                    "text-align": "left",
                    "padding": "12px 16px",
                    "margin": "4px 0",
                    "border-radius": "10px",
                    "color": "#94A3B8",
                    "font-weight": "500",
                    "--hover-color": "rgba(16,185,129,0.08)",
                },
                "nav-link-selected": {
                    "background-color": "rgba(16,185,129,0.12)",
                    "color": "#10B981",
                    "font-weight": "600",
                },
            },
        )

        st.markdown("---")

        # Logout
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            auth.sign_out()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Footer
        st.markdown("""
        <div style="position:fixed; bottom:16px; padding:0 12px;">
            <p style="color:#374151; font-size:0.72em; text-align:center;">
                CropGuard AI v1.0<br>Built with ❤️ for Farmers
            </p>
        </div>
        """, unsafe_allow_html=True)

    return selected


# ─── MAIN ───
def main():
    inject_css()

    if not auth.is_authenticated():
        auth_page()
        return

    selected = sidebar_nav()

    if selected == "Dashboard":
        dashboard_page()
    elif selected == "New Scan":
        new_scan_page()
    elif selected == "History":
        history_page()
    elif selected == "Profile":
        profile_page()


if __name__ == "__main__":
    main()
