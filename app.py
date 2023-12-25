import streamlit as st
import os
import google.generativeai as genai
import dotenv
from dotenv import load_dotenv

from pages.info import info_page
from pages.journal import journal_page
from pages.query_images import query_images_page



# def initialize_env_states() -> None:
#     """
    
#     """
# Function to initialize the session state

# else:
#     user_api_key = st.text_input("Enter your API key:", type="password")
#     user_email = st.text_input("Enter your EMAIL:", type="password")
#     st.session_state['user_email'] = user_email
#     st.session_state['user_api_key'] = user_api_key


def init_session_state():
    if 'user_api_key' not in st.session_state:
        st.session_state['user_api_key'] = None
    
    if 'user_email' not in st.session_state:
        st.session_state['user_email'] = None
    
# Initialize session state
init_session_state()

# user_api_key = st.text_input("Enter your API key:", type="password")
# user_email = st.text_input("Enter your EMAIL:", type="password")


if os.getenv('DEV_ENV'):
    user_api_key = os.getenv('DEV_API_KEY')
    user_email = os.getenv('DEV_EMAIL')





if user_api_key:
    st.session_state['user_api_key'] = user_api_key
else:
    user_api_key = st.text_input("Enter your API key:", type="password")



if user_email:
    user_email = st.text_input("Enter your EMAIL:", type="password")
else:
    st.session_state['user_email'] = user_email
    

PAGES = {
    # "Info": pages.info,
    "Info": info_page,
    "Journal": journal_page,
    "Query Images": query_images_page,
}

load_dotenv()

# initialize_env_states()


st.title("Chat - Gemini Bot")


# Set Google API key
genai.configure(api_key = st.secrets['GEMINI_API_KEY'])


# Create the Model
model = genai.GenerativeModel('gemini-pro')


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"Ask me Anything"
        }
    ]



# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Process and store Query and Response
def llm_function(query):
    response = model.generate_content(query)


    # Displaying the Assistant Message
    with st.chat_message("assistant"):
        st.markdown(response.text)


    # Storing the User Message
    st.session_state.messages.append(
        {
            "role":"user",
            "content": query
        }
    )


    # Storing the User Message
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content": response.text
        }
    )

def clear_chat_history():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "How may I assist you today?"
        }
    ]


   
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

   
# Accept user input
query = st.chat_input("What is up?")


# Calling the Function when Input is Provided
if query:
    # Displaying the User Message
    with st.chat_message("user"):
        st.markdown(query)


    llm_function(query)