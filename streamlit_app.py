import os
import numpy as np
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables
load_dotenv()

# Initialize the Gemini model with the API key
model = genai.GenerativeModel()
genai.configure(api_key="AIzaSyDBvuL_-rHm8M9Vi-YOYqnbSs0Wcj3gVLA")
def generate_content(image_bytes, prompt):
    try:
        # Prepare the image
        image = Image.open(BytesIO(image_bytes))
        image = image.convert('RGB')
        # Resize to the model's expected input size (e.g., 224x224 or 256x256)
        image = image.resize((224, 224))
        image_array = np.array(image)
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        # Normalize the image data
        image_array = image_array / 255.0

        # Prepare the instances and parameters
        instances = [
            {
                'image': {'content': image_bytes},
                'text': prompt
            }
        ]
        parameters = {}

        # Generate content using the Gemini Vision model
        response = model.generate_content(
            model='gemini-pro-vision',
            instances=instances,
            parameters=parameters,
            
        )

        return response.text[0]

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error generating content. Please check the input and try again."

# Streamlit UI
st.title('Google Gemini Vision Model')

# Image uploader
uploaded_image = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png'])

# Text input for the user's prompt
user_prompt = st.text_area('Enter your prompt here:')

if st.button('Generate'):
    if uploaded_image and user_prompt:
        with st.spinner('Generating content...'):
            image_bytes = uploaded_image.read()
            generated_text = generate_content(image_bytes, user_prompt)
            st.subheader('Generated Content:')
            st.write(generated_text)
    else:
        st.error('Please upload an image and enter a prompt before generating content.')