import streamlit as st
import os
import google.generativeai as genai
import dotenv
from dotenv import load_dotenv

from pages.info import info_page
from pages.journal import journal_page
from pages.query_images import query_images_page


if os.getenv('DEV_ENV'):
    user_api_key = os.getenv('DEV_API_KEY')
    user_email = os.getenv('DEV_EMAIL')


else:
    st.write("API Key:", st.secrets["DEV_API_KEY"])
    st.write("YOUR EMAIL:", st.secrets["DEV_EMAIL"])

    st.session_state['user_api_key'] = st.secrets["DEV_API_KEY"]
    st.session_state['user_email'] = st.secrets["DEV_EMAIL"]


if user_api_key:
    # st.session_state['user_api_key'] = user_api_key
    st.write("Secret set. Navigate to Page 2 to view the secret.")


# Save the input to the session state
if user_email:
    # st.session_state['user_email'] = user_email
    st.write(f"Value set to: {user_email}")


PAGES = {
    # "Info": pages.info,
    "Info": info_page,
    "Journal": journal_page,
    "Query Images": query_images_page,
}

load_dotenv()


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
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    # del st.session_state.messages
    # if "messages" not in st.session_state:
    #     st.session_state.messages = [
    #         {
    #             "role":"assistant",
    #             "content":"Ask me Anything"
    #         }
    #     ]

   
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

   
# Accept user input
query = st.chat_input("What is up?")


# Calling the Function when Input is Provided
if query:
    # Displaying the User Message
    with st.chat_message("user"):
        st.markdown(query)


    llm_function(query)