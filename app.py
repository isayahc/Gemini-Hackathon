import streamlit as st
from PIL import Image
from io import BytesIO

def main():
    st.title("Image Upload and Display")

    # File uploader widget
    uploaded_files = st.file_uploader("Choose image files", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Convert the file to an image
            image = Image.open(BytesIO(uploaded_file.getvalue()))

            # Display the image
            st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_column_width=True)

if __name__ == "__main__":
    main()
