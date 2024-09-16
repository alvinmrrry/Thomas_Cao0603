import streamlit as st
from groq import Groq
from config import groq_api_key
from your_module import create_conversation_chain  
import base64

client = Groq(api_key=groq_api_key) 

llava_model = 'llama-3.1-70b-versatile'

# image encoding 
def encode_image(image_path):
    """Encode an image to base64 format."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

# Example usage     
image_path = "path/to/your/image.jpg"
encoded_image = encode_image(image_path)
st.write(encoded_image)

def read_image_content(encoded_image):
    """Use the LLM to read the content of the image and return the text."""
    model_name = 'llama-3.1-70b-versatile'  # Specify the model to use
    system_prompt = "Describe the provided image."
    
    # Create a conversation chain with the LLM
    conversation_chain = create_conversation_chain(model_name, system_prompt, encoded_image)
    
    # Get the response from the LLM
    return conversation_chain

# Use the encoded image to read its content
if encoded_image:
    image_text = read_image_content(encoded_image)
    st.write("Extracted Text from Image:", image_text)
