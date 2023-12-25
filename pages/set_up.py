import streamlit as st

if 'user_api_key' not in st.session_state:
    # user_api_key = None
    st.session_state['user_api_key'] = None
    print("Huh")
    # pass
else:
    user_api_key = st.text_input("Enter your API key:", type="password")
    st.session_state['user_api_key'] = user_api_key
    # st.secrets['user_api_key'] = user_api_key



if 'user_email' not in st.session_state:
    # user_email = None
    st.session_state['user_email'] = None
    print("Huh")
    # pass
else:
    user_email = st.text_input("Enter your EMAIL:", type="password")
    st.session_state['user_email'] = user_email
    # st.secrets['user_email'] = user_email

st.markdown(
"""
# Warning 
due to streamlit's archecture if you click on this session again you will have to input your info agin
"""



)