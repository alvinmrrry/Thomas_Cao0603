import os

import numpy as np
import streamlit as st
import google.generativeai as genai
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Gemini client
model = genai.GenerativeModel(api_key='AIzaSyDBvuL_-rHm8M9Vi-YOYqnbSs0Wcj3gVLA')

# Function to generate content from Gemini vision model
def generate_content(image_bytes, input_text):
    # Prepare the image
    image = Image.open(BytesIO(image_bytes))
    image = image.convert("RGB")
    image = image.resize((224, 224))  # Resize to the model's expected input size
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0  # Normalize the image

    # Prepare the input data
    instances = [
        {
            "image": {"content": image_bytes},
            "text": input_text
        }
    ]

    # Prepare the parameters
    parameters = {}

    # Make the prediction request
    response = model.generate_content(
        model="gemini-pro-vision",
        instances=instances,
        parameters=parameters
    )

    # Extract and return the generated content
    return response.text[0]

# Streamlit UI
st.title("Google Gemini Vision Model")

# Image uploader
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Text input for the user to provide a prompt
user_input = st.text_area("Enter your prompt here:")

# When the user clicks the 'Generate' button
if st.button("Generate"):
    if uploaded_image and user_input:
        with st.spinner('Generating content...'):
            # Read the image bytes
            image_bytes = uploaded_image.read()

            # Generate the content
            output = generate_content(image_bytes, user_input)

            st.subheader("Generated Content:")
            st.text(output)  # Display the generated content
    else:
        st.error("Please upload an image and enter a prompt before generating content.")
