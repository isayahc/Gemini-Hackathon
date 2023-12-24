import streamlit as st
from PIL import Image
import io
from typing import List, Dict
from src.Gemini.gemini import genai

model = genai.GenerativeModel('gemini-pro-vision')

recipe_generator_template = """

Given an image of a food product, or a list of products, generate a recipe for that food product.


"""

health_product_prompt = """

Given an image of a food product, or a list of products, give a well researched health score for that food product.
You must be like a doctor and a nutritionist in one. If the product is not healthy, you must be able to suggest a healthier alternative.
If the product is healthy, you must explain why it is healthy and what are the benefits of eating it.
if it is not healthy explain what is in it that makes it unhealthy and what are the negative effects of eating it.

"""


def convert_uploaded_file(uploaded_file) -> Dict[str, bytes]:
    # Determine the MIME type
    mime_type = uploaded_file.type

    # Read the file and store it in the desired format
    file_data = {
        'mime_type': mime_type,
        'data': uploaded_file.read()
    }

    return file_data

def query_images_page():

    # st.title("Gemini Health Assistant")
    st.markdown(
        """
        # Gemini Health Assistant
        ## Use AI to automated the boring things about your health.
        This chatbot has 2 modes:
        - Generating recipes based on food products
        - Determines the healthiness of a food product
        """
    )


    user_prompt = ""
    converted_file = None

    prompt = st.radio(
        "Choose a mode",
        [":rainbow[Recipe Generator] 👨🏽‍🍳", "Healthiness Checker 🍎"],
        captions=["Generate a recipe for a food product", "Determine the healthiness of a food product"],
        index=0
    )

    additional_user_prompt = st.text_input(
        'Additional information',
        # "Write a short, engaging blog post based on these picture.",
        "I want a light snack. that will give me energy and help me focus. why does it give me focus?",
        # placeholder="please choose a prompt",
        )

    if prompt == ":rainbow[Recipe Generator] 👨🏽‍🍳":
        user_prompt = recipe_generator_template + additional_user_prompt
    elif prompt == "Healthiness Checker 🍎":
        user_prompt = health_product_prompt + additional_user_prompt

    
    st.write("You selected:", prompt)


    # File uploader allows user to add multiple files
    uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

    st.write(user_prompt)



    if uploaded_files:
        # converted_file = file_things(uploaded_files)
        for uploaded_file in uploaded_files:
            # Check if file size exceeds the limit
            if uploaded_file.size > 4194304:  # 4 MB limit
                st.error("File size exceeds the limit of 4 MB. Please upload a smaller file.")
                continue

            # converted_file = convert_uploaded_file(uploaded_file)
    if uploaded_files:

        if st.button("Submit"):

            for uploaded_file in uploaded_files:
                # Check if file size exceeds the limit
                if uploaded_file.size > 4194304:
                    st.error("File size exceeds the limit of 4 MB. Please upload a smaller file.")
                    continue
                else:
                    converted_file = convert_uploaded_file(uploaded_file)
                    # return converted_file
            try:
                # Generate content for each image
                response = model.generate_content(
                        [
                        user_prompt,
                        converted_file,
                        ], 
                    stream=True,
                    )
                # st.text(response.resolve())
                st.markdown(response.text)

                # Display the image
                image = Image.open(io.BytesIO(uploaded_file.getvalue()))
                st.image(image, use_column_width=True)
            except Exception as e:
                pass


if __name__ == "__main__":
    query_images_page()

