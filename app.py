from openai import OpenAI
import streamlit as st
import os
from tempfile import NamedTemporaryFile

import pages.info
import pages.journal
import pages.login
import pages.query_images

PAGES = {
    "Info": pages.info,
    "Journal": pages.journal,
    "Login": pages.login,
    "Query Images": pages.query_images,

}


def main():
    # Set up the title of the application
    st.title("ChatGPT-like clone")

    # User input for email and API key (not used in Gemini client)
    user_email = st.sidebar.text_input("Email")
    user_api_key = st.sidebar.text_input("API Key", type="password")

    # Initialize OpenAI client with API key from Streamlit secrets
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Initialize session state variables for model and messages
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # File upload feature in the sidebar
    # The file uploader is placed in the sidebar so it remains accessible
    uploaded_files:list = st.sidebar.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        )

    # Check if any files have been uploaded
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save the uploaded file to a temporary location
            with NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.read())  # Use .read() to read the content of the uploaded file
                uploaded_file_path = tmp_file.name
            # Add the uploaded file path to the chat history
            st.session_state.messages.append({"role": "user", "content": f"Uploaded image: {uploaded_file_path}"})
            # Display the uploaded image in the sidebar
            st.sidebar.image(uploaded_file, caption=uploaded_file.name)
            # Send a message to the chatbot indicating an image has been uploaded
            with st.chat_message("user"):
                st.markdown(f"Uploaded image: {uploaded_file.name}")

    # Display previous messages in the chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input box for user input
    if prompt := st.chat_input("What is up?"):
        # Append user input to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Placeholder for assistant's response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # Stream responses from OpenAI client and concatenate them
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                # Update the placeholder with each new piece of the response
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            # Finalize the assistant's message
            message_placeholder.markdown(full_response)

        # Add the assistant's final response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()