import streamlit as st

st.set_page_config(
    page_title="My Streamlit App",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    # Adding some custom CSS for better aesthetics
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
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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
