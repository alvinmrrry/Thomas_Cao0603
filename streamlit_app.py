import streamlit as st
from groq import Groq
from config import groq_api_key
import base64

client = Groq() 

# llama_model = 'llama-3.1-70b-versatile'
llava_model = 'llava-v1.5-7b-4096-preview'

# image encoding 
image_path = 'original.jpg'
def encode_image(image_path):
    """Encode an image to base64 format."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

base64_image = encode_image(image_path)

def image_to_text(client, model, base64_image, prompt):
    """
    Converts an image in base64 format to a descriptive text using a chat completion API.
    
    Parameters:
    - client: The client instance for the chat API.
    - model: The specific model to use for text generation.
    - base64_image: The image encoded in base64.
    - prompt: Additional context for the description.
    """
    try:
        # Create chat completion request
        chat_completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': f"Describe the following image: {base64_image} with prompt: {prompt}"
                }
            ]
        )
        
        # Return the generated description
        return chat_completion.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

prompt = 'Describe this image'

result = image_to_text(client, llava_model, base64_image, prompt)

st.write(result)  # Added result to display the output