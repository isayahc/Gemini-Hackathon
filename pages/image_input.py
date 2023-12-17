import streamlit as st
from PIL import Image
from typing import List
import io
from src.Gemini.gemini import genai

model = genai.GenerativeModel('gemini-pro-vision')

# response = model.generate_content(["Write a short, engaging blog post based on this picture. It should include a description of the meal in the photo and talk about my journey meal prepping.", img], stream=True)
# response.resolve()

def load_images(uploaded_files: List) -> List[Image.Image]:
    images = []
    for uploaded_file in uploaded_files:
        # Read the file and convert it to a PIL image
        image = Image.open(io.BytesIO(uploaded_file.read()))
        images.append(image)
    return images

def main():
    st.title("Image Upload Example")

    # File uploader allows user to add multiple files
    uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

    if uploaded_files:
        images = load_images(uploaded_files)

        response = model.generate_content(
            ["Write a short, engaging blog post based on this picture. It should include a description of the meal in the photo and talk about my journey meal prepping.", images], 
            stream=True)
        st.text(response.resolve())
        # response.resolve()

        for image in images:
            st.image(image, use_column_width=True)

if __name__ == "__main__":
    main()
