import streamlit as st
from PIL import Image
import io
from typing import List, Dict
from src.Gemini.gemini import genai

model = genai.GenerativeModel('gemini-pro-vision')

def convert_uploaded_file(uploaded_file) -> Dict[str, bytes]:
    # Determine the MIME type
    mime_type = uploaded_file.type

    # Read the file and store it in the desired format
    file_data = {
        'mime_type': mime_type,
        'data': uploaded_file.read()
    }

    return file_data

def main():
    st.title("Image Upload Example")
    st.subheader("Here is where you can upload images and see the results of GEMINI.")

    # File uploader allows user to add multiple files
    uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

    user_prompt = st.text_input(
        'prompt for gemi',
        "Write a short, engaging blog post based on these picture.",
        placeholder="please choose a prompt",
        )
    

    if uploaded_files:
        for uploaded_file in uploaded_files:
            converted_file = convert_uploaded_file(uploaded_file)

            # Generate content for each image
            response = model.generate_content(
                    [
                    user_prompt,
                    converted_file,
                    ], 
                stream=True,
                )
            st.text(response.resolve())
            st.markdown(response.text)

            # Display the image
            image = Image.open(io.BytesIO(uploaded_file.getvalue()))
            st.image(image, use_column_width=True)

if __name__ == "__main__":
    main()
