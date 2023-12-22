import streamlit as st
import os


def info_page():
    # Set up the title of the application
    st.title("Welcome to Health Assistant")
    st.text("Use AI to automated the boring things about your health.\nFocus on living feel and feeling your best.")

    st.markdown(
        f"""
        To use this service you must crate an account [Here]({os.getenv('API_DOMAIN')}).
        """
    )

    if os.getenv('DEV_ENV'):
    # Development-only features
        st.write("This is visible only in development")


if __name__ == "__main__":
    info_page()