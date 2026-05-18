import streamlit as st
from groq import Groq
import os
import time
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Amazon Saathi | Premium AI Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    h1 {
        color: #2c3e50;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background-color: #ff9900;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ffb84d;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_rag_knowledge():
    try:
        with open("amazon.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error("Could not find amazon.md. Using default prompt.")
        return "You are Amazon Saathi."

base_rag_content = load_rag_knowledge()

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", width=120)
    st.markdown("---")
    
    st.title("👤 User Profile")
    st.info("Status: Prime Member 👑")
    
    st.markdown("### ⚙️ Settings")
    
    env_api_key = os.getenv("GROQ_API_KEY", "") or st.secrets.get("GROQ_API_KEY", "")
    
    api_key = st.text_input("Groq API Key", value=env_api_key, type="password", help="Loaded from .env or enter here.")
    
    preferred_language = st.selectbox(
        "Response Language",
        ["English", "Hindi", "Hinglish", "Tamil", "Telugu", "Kannada"]
    )
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### 🔗 Quick Links")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("📦 My Orders", "https://www.amazon.in/gp/css/order-history", use_container_width=True)
    with col2:
        st.link_button("🛒 Cart", "https://www.amazon.in/gp/cart/view.html", use_container_width=True)
    st.link_button("🤝 Customer Service", "https://www.amazon.in/gp/help/customer/display.html", use_container_width=True)

dynamic_prompt = f"{base_rag_content}\n\nIMPORTANT: The user has selected {preferred_language} as their preferred language. Respond exactly in this language."

st.markdown("""
    <div class="premium-header">
        <div>
            <h1>Amazon Saathi</h1>
            <p>Your Next-Gen Shopping Assistant</p>
        </div>
        <div style="font-size: 3rem;">🛒</div>
    </div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! I'm **Amazon Saathi**, your personal shopping assistant. Whether you're looking for the best electronics, tracking an order, or exploring Prime, I'm here to help! \n\nHow can I make your shopping experience magical today? ✨"}
    ]

bot_avatar = "https://upload.wikimedia.org/wikipedia/commons/4/4a/Amazon_icon.svg"
user_avatar = "👤"

for msg in st.session_state.messages:
    avatar = bot_avatar if msg["role"] == "assistant" else user_avatar
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if len(st.session_state.messages) == 1:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ✨ Try asking about:")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="action-btn">', unsafe_allow_html=True)
        if st.button("📱 Phones under ₹20k", use_container_width=True):
            st.session_state.quick_reply = "Recommend me the best smartphones under 20000 rupees with great cameras."
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="action-btn">', unsafe_allow_html=True)
        if st.button("📦 Track latest order", use_container_width=True):
            st.session_state.quick_reply = "Where is my order? It was supposed to arrive yesterday."
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="action-btn">', unsafe_allow_html=True)
        if st.button("👑 Prime Benefits", use_container_width=True):
            st.session_state.quick_reply = "What are the benefits of Amazon Prime?"
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="action-btn">', unsafe_allow_html=True)
        if st.button("🏪 Sell on Amazon", use_container_width=True):
            st.session_state.quick_reply = "I want to sell my handmade products on Amazon. How do I start?"
        st.markdown('</div>', unsafe_allow_html=True)

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