import os
import numpy as np
import streamlit as st
from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types



# Initialize the Gemini model with the specific version
model = genai.GenerativeModel('gemini-2.0-flash')
genai.configure(api_key='AIzaSyDBvuL_-rHm8M9Vi-YOYqnbSs0Wcj3gVLA')
# Initialize the GenAI client
client = genai.Client()

def process_image(image_bytes, prompt):
    try:
        # Prepare the image
        image = Image.open(BytesIO(image_bytes))
        image = image.convert('RGB')
        # Resize to the model's expected input size (e.g., 224x224)
        image = image.resize((224, 224))
        image_array = np.array(image)
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        # Normalize the image data
        image_array = image_array / 255.0

        # Upload the image to Gemini
        file = client.files.upload(file=image_bytes)
        file_uri = file.uri
        mime_type = file.mime_type

        # Prepare the content
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(
                        file_uri=file_uri,
                        mime_type=mime_type,
                    ),
                    types.Part.from_text(
                        text=prompt
                    ),
                ],
            ),
        ]

        # Configure the generation settings
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="text/plain",
        )

        # Generate content using the Gemini model
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=contents,
            config=generate_content_config,
        )

        return response.text

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
            generated_text = process_image(image_bytes, user_prompt)
            st.subheader('Generated Content:')
            st.write(generated_text)
    else:
        st.error('Please upload an image and enter a prompt before generating content.')