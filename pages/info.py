import streamlit as st
import os


def info_page():
    # Set up the title of the application
    st.title("ChatGPT-like clone")

    if os.getenv('DEV_ENV'):
    # Development-only features
        st.write("This is visible only in development")


if __name__ == "__main__":
    info_page()