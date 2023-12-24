import streamlit as st
import os



def info_page():
    st.markdown(
        """
        # Welcome to Health Assistant

        Use AI to automate the boring things about your health. Focus on living well and feeling your best.

        ## Before You Begin

        - To use this service, you must create an account [here]({}) via Google or GitHub.
        - After logging in to the service, you will be given an API key. Copy this key and paste it in the input box below, along with your email account.

        ## Additional Notes

        ### Tech stack

        - Google Cloud Platform
        - Streamlit
        - Firestore

        ### Bugs

        - In the journal page, if you get an error, try swtiching to the main page and back to the journal page.
        - In the journal page, you have to press the edit button twice to edit the entry.
        """.format(os.getenv('API_DOMAIN'))
    )



if __name__ == "__main__":
    info_page()