import streamlit as st
from groq import Groq
import os
import time
import base64
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Amazon Saathi | Premium AI Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to safely load and encode binary image assets to Base64 (prevents browser file:/// CORS blocks)
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return ""

img_path = r"C:\Users\ratho\.gemini\antigravity-ide\brain\4e1b0712-17a4-49e7-b7b1-717cfb6c3d4f\shopping_cart_illustration_1780420201907.png"
img_base64 = get_base64_image(img_path)

# Cache loaded knowledge - must be defined before sidebars
@st.cache_data
def load_rag_knowledge():
    try:
        with open("amazon.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "You are Amazon Saathi."

base_rag_content = load_rag_knowledge()

# Initialize theme mode in session state
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# First block of sidebar for Theme selection
with st.sidebar:
    # Amazon Logo with Smile filter
    st.markdown('<div class="amazon-sidebar-logo">', unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", width=110)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Custom Navigation Menu
    st.markdown("""
        <div class="nav-menu">
            <a href="#" class="nav-item active">
                <span class="nav-item-icon">🏠</span> Home
            </a>
            <a href="#" class="nav-item">
                <span class="nav-item-icon">📋</span> Orders
            </a>
            <a href="#" class="nav-item">
                <span class="nav-item-icon">❤️</span> Wishlist
            </a>
            <a href="#" class="nav-item">
                <span class="nav-item-icon">🏷️</span> Deals & Offers
            </a>
            <a href="#" class="nav-item">
                <span class="nav-item-icon">👤</span> Account
            </a>
            <a href="#" class="nav-item">
                <span class="nav-item-icon">👑</span> Prime
            </a>
            <a href="#" class="nav-item">
                <span class="nav-item-icon">💬</span> Support
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    # User Profile Card
    st.markdown("""
        <div class="profile-card-container">
            <div class="profile-avatar-circle">
                <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#006636" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
            </div>
            <div class="profile-info">
                <span class="profile-name">Simran Kanwar</span>
                <span class="profile-prime-status">Prime Member 👑</span>
            </div>
        </div>
        <div class="profile-badge-pill">Prime since Jan 2024</div>
    """, unsafe_allow_html=True)

    # Appearance mode toggle (placed natively inside the sidebar)
    st.markdown('<div class="sidebar-section-header">🌓 Appearance</div>', unsafe_allow_html=True)
    theme = st.radio("Theme Mode", ["Light", "Dark"], label_visibility="collapsed", index=0, horizontal=True)
    st.session_state.theme = theme

# Define theme color tokens using CSS variables
if st.session_state.theme == "Dark":
    css_vars = """
    :root {
        --font-display: 'Space Grotesk', sans-serif;
        --font-body: 'Plus Jakarta Sans', sans-serif;
        --bg-app: #0e1117;
        --bg-main: #0e1117;
        --bg-sidebar: #131921;
        --border-sidebar: #232f3e;
        --shadow-sidebar: rgba(0,0,0,0.3);
        --text-nav: #cbd5e0;
        --bg-nav-hover: #1c2d22;
        --text-nav-hover: #4ade80;
        --bg-nav-active: #1a3a2a;
        --text-nav-active: #4ade80;
        --border-nav-active: #4ade80;
        --bg-profile: #1c2026;
        --border-profile: #2d3748;
        --text-profile-name: #f7fafc;
        --text-profile-prime: #f6ad55;
        --bg-profile-pill: #1a3a2a;
        --text-profile-pill: #4ade80;
        --bg-hero: linear-gradient(135deg, #092c1a 0%, #123e25 60%, #1c2026 100%);
        --border-hero: #14532d;
        --shadow-hero: rgba(0, 0, 0, 0.2);
        --text-hero-title: #4ade80;
        --text-hero-sub: #cbd5e0;
        --bg-welcome: #1a202c;
        --border-welcome: #14532d;
        --text-welcome: #e2e8f0;
        
        /* Card Blue */
        --bg-card-phone: #1e293b;
        --border-card-phone: #2563eb;
        --text-card-phone: #93c5fd;
        --bg-card-phone-hover: #1e3a8a;

        /* Card Amber */
        --bg-card-track: #272015;
        --border-card-track: #d97706;
        --text-card-track: #fcd34d;
        --bg-card-track-hover: #451a03;

        /* Card Purple */
        --bg-card-prime: #221c3b;
        --border-card-prime: #7c3aed;
        --text-card-prime: #c084fc;
        --bg-card-prime-hover: #3b0764;

        /* Card Green */
        --bg-card-sell: #142d1f;
        --border-card-sell: #16a34a;
        --text-card-sell: #86efac;
        --bg-card-sell-hover: #052e16;

        --bg-trust: #1a202c;
        --border-trust: #2d3748;
        --text-trust-title: #f7fafc;
        --text-trust-span: #a0aec0;
        --border-trust-divider: #2d3748;

        --bg-chat-input: #1a202c;
        --border-chat-input: #008f4c;
        --text-chat-input: #ffffff;
        --bg-chat-submit: #006636;
        --bg-chat-submit-hover: #004b23;
        
        --filter-logo: hue-rotate(95deg) saturate(1.4) brightness(0.9);
        --bg-user-avatar: #1a3a2a;
        --text-user-avatar: #4ade80;
    }
    """
else:
    css_vars = """
    :root {
        --font-display: 'Space Grotesk', sans-serif;
        --font-body: 'Plus Jakarta Sans', sans-serif;
        --bg-app: #f4f7f5;
        --bg-main: #f4f7f5;
        --bg-sidebar: #ffffff;
        --border-sidebar: #e2e8f0;
        --shadow-sidebar: rgba(0,102,54,0.02);
        --text-nav: #4a5568;
        --bg-nav-hover: #f0fdf4;
        --text-nav-hover: #006636;
        --bg-nav-active: #e6f7ed;
        --text-nav-active: #006636;
        --border-nav-active: #006636;
        --bg-profile: #ffffff;
        --border-profile: #e2e8f0;
        --text-profile-name: #1a202c;
        --text-profile-prime: #b7791f;
        --bg-profile-pill: #e6f7ed;
        --text-profile-pill: #006636;
        --bg-hero: linear-gradient(135deg, #dcfce7 0%, #e6fdf0 50%, #ffffff 100%);
        --border-hero: #a7f3d0;
        --shadow-hero: rgba(0, 102, 54, 0.05);
        --text-hero-title: #004b23;
        --text-hero-sub: #4a5568;
        --bg-welcome: #ffffff;
        --border-welcome: #eef9f3;
        --text-welcome: #2d3748;
        
        /* Card Blue */
        --bg-card-phone: #eff6ff;
        --border-card-phone: #bfdbfe;
        --text-card-phone: #1e3a8a;
        --bg-card-phone-hover: #dbeafe;

        /* Card Amber */
        --bg-card-track: #fffbeb;
        --border-card-track: #fde68a;
        --text-card-track: #78350f;
        --bg-card-track-hover: #fef3c7;

        /* Card Purple */
        --bg-card-prime: #faf5ff;
        --border-card-prime: #e9d5ff;
        --text-card-prime: #4c1d95;
        --bg-card-prime-hover: #f3e8ff;

        /* Card Green */
        --bg-card-sell: #f0fdf4;
        --border-card-sell: #bbf7d0;
        --text-card-sell: #14532d;
        --bg-card-sell-hover: #dcfce7;

        --bg-trust: #ffffff;
        --border-trust: #e2e8f0;
        --text-trust-title: #2d3748;
        --text-trust-span: #718096;
        --border-trust-divider: #edf2f7;

        --bg-chat-input: #ffffff;
        --border-chat-input: #006636;
        --text-chat-input: #2d3748;
        --bg-chat-submit: #006636;
        --bg-chat-submit-hover: #004b23;
        
        --filter-logo: hue-rotate(95deg) saturate(1.4) brightness(0.9);
        --bg-user-avatar: #e6f7ed;
        --text-user-avatar: #006636;
    }
    """

# Inject Dynamic Stylesheet based on selection
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

    {css_vars}

    /* ========== TYPOGRAPHY & LAYOUT BASE ========== */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"], 
    input, select, textarea, button, p, span, div, li, a, label {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        letter-spacing: 0.01em;
    }}

    h1, h2, h3, h4, h5, h6, .hero-title, .section-title, .sidebar-section-header, 
    [data-baseweb="tab"] *, [data-testid="stExpander"] summary {{
        font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 700 !important;
    }}

    h1, .hero-title {{
        font-size: 38px !important;
        font-weight: 800 !important;
        letter-spacing: -0.025em !important;
        line-height: 1.15 !important;
    }}

    h2 {{
        font-size: 26px !important;
        letter-spacing: -0.02em !important;
    }}

    code, pre, [data-testid="stMarkdownContainer"] code, [data-testid="stMarkdownContainer"] pre {{
        font-family: Consolas, Monaco, 'Andale Mono', monospace !important;
        font-size: 13.5px !important;
        background-color: #2d3748 !important;
        color: #e2e8f0 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background-color: var(--bg-app) !important;
    }}
    
    [data-testid="stMainBlockContainer"] {{
        background-color: var(--bg-main) !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }}

    /* ========== SIDEBAR COMPONENT ========== */
    [data-testid="stSidebar"] {{
        background-color: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border-sidebar) !important;
        box-shadow: 4px 0 16px var(--shadow-sidebar) !important;
    }}
    
    .amazon-sidebar-logo img {{
        filter: var(--filter-logo);
    }}
    
    .nav-menu {{
        margin-top: 15px;
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        gap: 3px;
    }}
    
    .nav-menu a.nav-item, .nav-menu a.nav-item:visited {{
        display: flex;
        align-items: center;
        padding: 10px 14px;
        color: var(--text-nav) !important;
        font-weight: 500;
        font-size: 13.5px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none !important;
    }}
    
    .nav-menu a.nav-item:hover {{
        background-color: var(--bg-nav-hover) !important;
        color: var(--text-nav-hover) !important;
        padding-left: 18px;
        text-decoration: none !important;
    }}
    
    .nav-menu a.nav-item.active {{
        background-color: var(--bg-nav-active) !important;
        color: var(--text-nav-active) !important;
        font-weight: 600;
        position: relative;
        text-decoration: none !important;
    }}
    
    .nav-menu a.nav-item.active::before {{
        content: '';
        position: absolute;
        left: 4px;
        top: 50%;
        transform: translateY(-50%);
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: var(--text-nav-active) !important;
        box-shadow: 0 0 6px var(--text-nav-active) !important;
    }}
    
    .nav-item-icon {{
        margin-right: 10px;
        font-size: 15px;
    }}

    .profile-card-container {{
        border: 1px solid var(--border-profile);
        border-radius: 12px;
        padding: 12px;
        background-color: var(--bg-profile);
        margin: 15px 0 8px;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 4px 12px rgba(0, 102, 54, 0.02);
    }}
    
    .profile-avatar-circle {{
        background-color: var(--bg-profile-pill);
        border-radius: 50%;
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}
    
    .profile-avatar-circle svg {{
        stroke: var(--text-nav-hover);
    }}
    
    .profile-info {{
        display: flex;
        flex-direction: column;
    }}
    
    .profile-name {{
        font-size: 13.5px;
        font-weight: 600;
        color: var(--text-profile-name) !important;
    }}
    
    .profile-prime-status {{
        font-size: 11px;
        color: var(--text-profile-prime) !important;
        font-weight: 600;
    }}
    
    .profile-badge-pill {{
        background-color: var(--bg-profile-pill);
        color: var(--text-profile-pill) !important;
        font-size: 10px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 99px;
        display: inline-block;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}

    .sidebar-section-header {{
        font-size: 10.5px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-nav) !important;
        margin: 20px 0 10px;
        border-bottom: 1px solid var(--border-profile);
        padding-bottom: 4px;
    }}

    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] div[data-baseweb="radio"] span,
    [data-testid="stSidebar"] div[data-baseweb="checkbox"] span,
    [data-testid="stSidebar"] div[data-baseweb="select"] div,
    [data-testid="stSidebar"] .sidebar-section-header {{
        color: var(--text-nav) !important;
        font-size: 12.5px !important;
    }}
    
    [data-testid="stSidebar"] input {{
        border-radius: 8px !important;
        border: 1.5px solid var(--border-profile) !important;
        font-size: 13px !important;
        background-color: var(--bg-app) !important;
        color: var(--text-profile-name) !important;
    }}

    [data-testid="stSidebar"] [data-testid="stButton"] button {{
        background-color: #006636 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 8px 12px !important;
        font-size: 13px !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        box-shadow: 0 4px 10px rgba(0, 102, 54, 0.1) !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stButton"] button:hover {{
        background-color: #004b23 !important;
        box-shadow: 0 6px 14px rgba(0, 102, 54, 0.2) !important;
        transform: translateY(-1px);
    }}

    .quick-links-list {{
        display: flex;
        flex-direction: column;
        gap: 3px;
    }}
    
    .quick-links-list a.quick-link-item, .quick-links-list a.quick-link-item:visited {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 12.5px;
        color: var(--text-nav) !important;
        text-decoration: none !important;
        padding: 6px 8px;
        border-radius: 6px;
        transition: all 0.2s ease;
    }}
    
    .quick-links-list a.quick-link-item:hover {{
        color: var(--text-nav-hover) !important;
        background-color: var(--bg-nav-hover);
        padding-left: 12px;
        text-decoration: none !important;
    }}

    /* ========== MAIN APP COMPONENTS ========== */
    /* Hero Card */
    .hero-card {{
        background: var(--bg-hero) !important;
        border: 1px solid var(--border-hero) !important;
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 10px 25px var(--shadow-hero) !important;
    }}
    
    .hero-text-content {{
        max-width: 65%;
    }}
    
    .hero-title-wrapper {{
        margin-bottom: 6px;
    }}
    
    .hero-smile-svg {{
        height: 10px;
        width: 120px;
        margin-top: -2px;
        margin-bottom: 8px;
    }}
    
    .hero-smile-svg path {{
        stroke: var(--text-hero-title) !important;
    }}
    
    .hero-subtitle {{
        font-size: 15px;
        color: var(--text-hero-sub);
        margin-bottom: 18px;
        font-weight: 500;
    }}

    .hero-welcome-bubble {{
        background-color: var(--bg-welcome);
        border-radius: 14px;
        padding: 14px;
        border: 1.5px solid var(--border-welcome);
        display: flex;
        gap: 12px;
        align-items: center;
    }}
    
    .hero-welcome-logo-container {{
        width: 42px;
        height: 42px;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: var(--bg-app);
        border-radius: 8px;
        border: 1px solid var(--border-profile);
    }}
    
    .hero-welcome-logo {{
        width: 28px;
        height: 28px;
    }}
    
    .hero-welcome-text {{
        font-size: 13px;
        line-height: 1.5;
        color: var(--text-profile-name);
    }}

    .hero-image-container {{
        max-width: 32%;
        display: flex;
        justify-content: center;
    }}
    
    .hero-image-container img {{
        max-width: 100%;
        height: auto;
        filter: drop-shadow(0 12px 20px rgba(0,102,54,0.08));
    }}

    .section-title {{
        font-size: 16px;
        color: var(--text-profile-name);
        margin: 25px 0 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    /* Grid Button Cards configuration */
    [data-testid="column"] {{
        padding: 0 4px !important;
    }}

    /* Card Themes dynamically loaded */
    .card-phone button {{ background-color: var(--bg-card-phone) !important; border: 1.5px solid var(--border-card-phone) !important; }}
    .card-phone button:hover {{ background-color: var(--bg-card-phone-hover) !important; border-color: #3b82f6 !important; }}
    .card-phone button p {{ color: var(--text-card-phone) !important; }}
    .card-phone button::after {{ content: "Best phones in your budget"; color: var(--text-card-phone); }}

    .card-track button {{ background-color: var(--bg-card-track) !important; border: 1.5px solid var(--border-card-track) !important; }}
    .card-track button:hover {{ background-color: var(--bg-card-track-hover) !important; border-color: #d97706 !important; }}
    .card-track button p {{ color: var(--text-card-track) !important; }}
    .card-track button::after {{ content: "Check your order status"; color: var(--text-card-track); }}

    .card-prime button {{ background-color: var(--bg-card-prime) !important; border: 1.5px solid var(--border-card-prime) !important; }}
    .card-prime button:hover {{ background-color: var(--bg-card-prime-hover) !important; border-color: #8b5cf6 !important; }}
    .card-prime button p {{ color: var(--text-card-prime) !important; }}
    .card-prime button::after {{ content: "Explore Prime advantages"; color: var(--text-card-prime); }}

    .card-sell button {{ background-color: var(--bg-card-sell) !important; border: 1.5px solid var(--border-card-sell) !important; }}
    .card-sell button:hover {{ background-color: var(--bg-card-sell-hover) !important; border-color: #22c55e !important; }}
    .card-sell button p {{ color: var(--text-card-sell) !important; }}
    .card-sell button::after {{ content: "Start selling with us"; color: var(--text-card-sell); }}

    div[data-testid="column"] button {{
        border-radius: 12px !important;
        padding: 14px 16px !important;
        text-align: left !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        align-items: flex-start !important;
        min-height: 85px !important;
        width: 100% !important;
    }}
    div[data-testid="column"] button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.04) !important;
    }}
    div[data-testid="column"] button p {{
        font-weight: 700 !important;
        font-size: 14.5px !important;
        margin: 0 !important;
    }}
    div[data-testid="column"] button::after {{
        display: block;
        font-size: 11.5px;
        margin-top: 4px;
        font-weight: 500;
        opacity: 0.85;
    }}

    /* Trust Badges styling */
    .trust-badges-container {{
        background-color: var(--bg-trust);
        border: 1px solid var(--border-profile);
        border-radius: 14px;
        padding: 16px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 25px 0;
        gap: 12px;
    }}
    
    .trust-badge {{
        flex: 1;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .badge-icon {{
        font-size: 20px;
    }}
    
    .badge-text {{
        display: flex;
        flex-direction: column;
    }}
    
    .badge-text strong {{
        font-size: 13px;
        font-weight: 700;
        color: var(--text-trust-title);
    }}
    
    .badge-text span {{
        font-size: 10.5px;
        color: var(--text-trust-span);
        line-height: 1.3;
    }}
    
    .trust-badges-container .divider {{
        width: 1px;
        height: 32px;
        background-color: var(--border-trust-divider);
    }}

    /* Chat Elements Customization */
    [data-testid="stChatInput"] {{
        background-color: var(--bg-chat-input) !important;
        border: 2px solid var(--border-chat-input) !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 16px rgba(0,102,54,0.04) !important;
        padding: 2px 4px !important;
    }}
    
    [data-testid="stChatInput"] textarea {{
        color: var(--text-chat-input) !important;
        background-color: var(--bg-chat-input) !important;
        font-size: 13.5px !important;
        font-weight: 500 !important;
    }}
    
    [data-testid="stChatInput"] button {{
        background-color: var(--bg-chat-submit) !important;
        color: #ffffff !important;
        border-radius: 6px !important;
    }}
    
    [data-testid="stChatInput"] button:hover {{
        background-color: var(--bg-chat-submit-hover) !important;
    }}

    [data-testid="stChatMessage"] {{
        background-color: var(--bg-profile) !important;
        border: 1px solid var(--border-profile) !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.01);
    }}

    [data-testid="chatAvatarIcon-user"] {{
        background-color: var(--bg-user-avatar) !important;
        color: var(--text-user-avatar) !important;
    }}
    
    [data-testid="chatAvatarIcon-assistant"] {{
        background-color: var(--bg-profile-pill) !important;
    }}

    /* ========== THEME SYNC OVERRIDES (Light / Dark Compatibility) ========== */
    h1, h2, h3, h4, h5, h6, p, span, li, strong, em, label,
    [data-testid="stMarkdownContainer"] *, [data-testid="stChatMessageContent"] *, 
    [data-testid="stWidgetLabel"] p, [data-baseweb="tab"] *, [data-testid="stAlert"] * {{
        color: var(--text-profile-name) !important;
    }}

    [data-testid="stMainBlockContainer"] a, [data-testid="stMarkdownContainer"] a {{
        color: var(--text-hero-title) !important;
        text-decoration: underline !important;
    }}

    [data-testid="stMainBlockContainer"] pre, [data-testid="stMarkdownContainer"] pre {{
        background-color: #2d3748 !important;
        padding: 10px 14px !important;
        border-radius: 6px !important;
        overflow-x: auto !important;
    }}

    [data-testid="stSpinner"] p, [data-testid="stSpinner"] span {{
        color: var(--text-hero-title) !important;
    }}

    [data-testid="stChatInput"] textarea::placeholder, 
    [data-testid="stSidebar"] input::placeholder, 
    [data-testid="stMain"] input::placeholder {{
        color: #718096 !important;
    }}

    [data-testid="stChatMessageContent"] {{
        background-color: transparent !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Main settings module (continues in sidebar)
with st.sidebar:
    # Settings Header
    st.markdown('<div class="sidebar-section-header">⚙️ Settings</div>', unsafe_allow_html=True)
    
    try:
        env_api_key = os.getenv("GROQ_API_KEY", "") or st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        env_api_key = os.getenv("GROQ_API_KEY", "")
        
    api_key = st.text_input("Groq API Key", value=env_api_key, type="password", help="Loaded from .env or enter here.")
    
    preferred_language = st.selectbox(
        "Response Language",
        ["English", "Hindi", "Hinglish", "Tamil", "Telugu", "Kannada"]
    )
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    # Quick Links
    st.markdown('<div class="sidebar-section-header">🔗 Quick Links</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="quick-links-list">
            <a href="https://www.amazon.in" target="_blank" class="quick-link-item">
                <span>Amazon.in</span> <span>↗</span>
            </a>
            <a href="https://www.amazon.in/gp/goldbox" target="_blank" class="quick-link-item">
                <span>Today's Deals</span> <span>↗</span>
            </a>
            <a href="https://www.amazon.in/gp/help/customer/display.html" target="_blank" class="quick-link-item">
                <span>Customer Service</span> <span>↗</span>
            </a>
            <a href="https://sell.amazon.in" target="_blank" class="quick-link-item">
                <span>Sell on Amazon</span> <span>↗</span>
            </a>
        </div>
    """, unsafe_allow_html=True)

dynamic_prompt = f"{base_rag_content}\n\nIMPORTANT: The user has selected {preferred_language} as their preferred language. Respond exactly in this language."

# Main Page - Premium Hero Banner Layout with base64 image data-URI
img_src = f"data:image/png;base64,{img_base64}" if img_base64 else ""

hero_html = f"""
<div class="hero-card">
    <div class="hero-text-content">
        <div class="hero-title-wrapper">
            <h1 class="hero-title">Amazon Saathi</h1>
            <svg class="hero-smile-svg" viewBox="0 0 110 10" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 2C35 9 75 9 105 2" stroke-width="3.5" stroke-linecap="round"/>
                <path d="M100 1.5L105 2L101.5 6.5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div class="hero-subtitle">Your Next-Gen Shopping Assistant</div>
        <div class="hero-welcome-bubble">
            <div class="hero-welcome-logo-container">
                <img class="hero-welcome-logo" src="https://upload.wikimedia.org/wikipedia/commons/4/4a/Amazon_icon.svg" />
            </div>
            <div class="hero-welcome-text">
                Namaste! I'm <strong>Amazon Saathi</strong>, your personal shopping assistant. Whether you're looking for the best electronics, tracking an order, or exploring Prime, I'm here to help!<br/>
                How can I make your shopping experience magical today? ✨
            </div>
        </div>
    </div>
    <div class="hero-image-container">
        <img src="{img_src}" alt="Shopping Cart Illustration" />
    </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! I'm **Amazon Saathi**, your personal shopping assistant. Whether you're looking for the best electronics, tracking an order, or exploring Prime, I'm here to help! \n\nHow can I make your shopping experience magical today? ✨"}
    ]

bot_avatar = "https://upload.wikimedia.org/wikipedia/commons/4/4a/Amazon_icon.svg"
user_avatar = "👤"

# Display conversation messages (skipping the initial greeting in standard chat because it is already featured in the Hero Card banner)
for msg in st.session_state.messages[1:]:
    avatar = bot_avatar if msg["role"] == "assistant" else user_avatar
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Quick recommendation cards
if len(st.session_state.messages) == 1:
    st.markdown('<div class="section-title">✨ Try asking about:</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="card-phone">', unsafe_allow_html=True)
        if st.button("📱 Phones under ₹20k", key="phone_btn", use_container_width=True):
            st.session_state.quick_reply = "Recommend me the best smartphones under 20000 rupees with great cameras."
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card-track">', unsafe_allow_html=True)
        if st.button("📦 Track latest order", key="track_btn", use_container_width=True):
            st.session_state.quick_reply = "Where is my order? It was supposed to arrive yesterday."
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="card-prime">', unsafe_allow_html=True)
        if st.button("👑 Prime Benefits", key="prime_btn", use_container_width=True):
            st.session_state.quick_reply = "What are the benefits of Amazon Prime?"
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="card-sell">', unsafe_allow_html=True)
        if st.button("🏪 Sell on Amazon", key="sell_btn", use_container_width=True):
            st.session_state.quick_reply = "I want to sell my handmade products on Amazon. How do I start?"
        st.markdown('</div>', unsafe_allow_html=True)

    # Trust Badges
    st.markdown("""
        <div class="trust-badges-container">
            <div class="trust-badge">
                <span class="badge-icon">🔒</span>
                <div class="badge-text">
                    <strong>Secure & Trusted</strong>
                    <span>Your data is protected with end-to-end encryption</span>
                </div>
            </div>
            <div class="divider"></div>
            <div class="trust-badge">
                <span class="badge-icon">⚡</span>
                <div class="badge-text">
                    <strong>Quick Assistance</strong>
                    <span>Get instant answers to all your queries</span>
                </div>
            </div>
            <div class="divider"></div>
            <div class="trust-badge">
                <span class="badge-icon">🧠</span>
                <div class="badge-text">
                    <strong>AI-Powered</strong>
                    <span>Smart responses powered by advanced AI</span>
                </div>
            </div>
            <div class="divider"></div>
            <div class="trust-badge">
                <span class="badge-icon">⭐</span>
                <div class="badge-text">
                    <strong>24/7 Available</strong>
                    <span>Always here to help, anytime you need</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# User Chat Input
user_input = st.chat_input("Ask Saathi (e.g. 'Show me laptop deals' or 'Return policy for clothes')...")

if getattr(st.session_state, "quick_reply", None):
    user_input = st.session_state.quick_reply
    del st.session_state.quick_reply

if user_input:
    if not api_key:
        st.warning("⚠️ Please provide a valid Groq API Key in the `.env` file or in the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar=user_avatar):
            st.markdown(user_input)

        client = Groq(api_key=api_key)
        
        messages = [
            {"role": "system", "content": dynamic_prompt}
        ]
        
        for msg in st.session_state.messages[:-1]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant", avatar=bot_avatar):
            with st.spinner("Saathi is thinking..."):
                response_placeholder = st.empty()
                full_response = ""
                
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=messages,
                        stream=True
                    )
                    
                    for chunk in response:
                        if chunk.choices[0].delta.content:
                            full_response += chunk.choices[0].delta.content
                            response_placeholder.markdown(full_response + "▌")
                            time.sleep(0.01)
                    response_placeholder.markdown(full_response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")