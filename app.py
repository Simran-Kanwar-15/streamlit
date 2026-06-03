import streamlit as st

st.set_page_config(
    page_title="My Streamlit App",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    # Adding some custom CSS for premium aesthetics
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');
        
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"], 
        input, select, textarea, button, p, span, div, li, a, label {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            letter-spacing: 0.01em;
        }

        h1, h2, h3, h4, h5, h6, [data-baseweb="tab"] *, [data-testid="stExpander"] summary {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
        }

        h1 {
            color: #1a202c;
            font-size: 36px !important;
            font-weight: 800 !important;
            letter-spacing: -0.025em !important;
            line-height: 1.15 !important;
        }

        .main {
            background-color: #f4f7f5;
        }

        .stButton>button {
            background-color: #006636;
            color: white;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1.25rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 10px rgba(0, 102, 54, 0.1);
        }
        .stButton>button:hover {
            background-color: #004b23;
            transform: translateY(-1px);
            box-shadow: 0 6px 14px rgba(0, 102, 54, 0.2);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("✨ Welcome to Your Streamlit Website")
    st.markdown("---")
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "About", "Contact"])

    if page == "Home":
        st.header("Home Page")
        st.write("This is your new Streamlit workspace. You can start building your interactive web application here!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("💡 **Tip**: Use `st.columns` to create responsive layouts.")
        with col2:
            st.success("✅ **Tip**: Streamlit automatically updates when you save `app.py`.")
        with col3:
            st.warning("⚡ **Tip**: Add interactive widgets easily!")

        if st.button("Click me!"):
            st.balloons()
            st.success("Button clicked! You're ready to go.")

    elif page == "About":
        st.header("About")
        st.write("Add your project description here.")

    elif page == "Contact":
        st.header("Contact")
        st.write("Add contact forms or details here.")

if __name__ == "__main__":
    main()
