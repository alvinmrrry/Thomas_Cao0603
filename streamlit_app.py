import streamlit as st
from groq import Groq
from config import groq_api_key
import base64

client = Groq(api_key=groq_api_key) 

llava_model = 'llama-3.1-70b-versatile'

# image encoding 
image_path = 'original.jpg'
def encode_image(image_path):
    """Encode an image to base64 format."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

base64_image = encode_image(image_path)

def image_to_text(client, model, base64_image, prompt):
    chat_completion = client.chat.completions.create(
        model=model, 
        messages=[
            {
                'role': 'user',
                'content': f"Describe the following image: {base64_image} with prompt: {prompt}"  # Fixed structure
            }
        ]
    )
    return chat_completion.choices[0].message['content']  # Fixed access to message content

prompt = 'Describe this image'

result = image_to_text(client, llava_model, base64_image, prompt)

st.write(result)  # Added result to display the output