from groq import Groq
from config import groq_api_key
import streamlit as st
import base64

client = Groq(api_key=groq_api_key)

llava_model='llava-v1.5-7b-4096-preview'
llama31_model='llama-3.1-70b-versatile'

# image encoding
image_path = 'original.jpg'
def encode_image(image_path):
    """
    Encodes an image file into a base64 string.
    
    Args:
        image_path (str): The path to the image file.
    
    Returns:
        str: The base64 encoded string of the image.
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_string
    except FileNotFoundError:
        raise ValueError(f"File {image_path} not found.")
    except IOError:
        raise ValueError(f"Error reading file {image_path}.")
    except Exception as e:
        raise ValueError(f"An error occurred: {e}") from e


base64_image = encode_image(image_path)

# image to text function
def image_to_text(client, model, base64_image, prompt):
    if not client:
        raise ValueError("Groq client cannot be None")
    if not model:
        raise ValueError("Model cannot be None")
    if not base64_image:
        raise ValueError("Base64 image cannot be None")
    if not prompt:
        raise ValueError("Prompt cannot be None")
    try:
        chat_completion = client.chat.completions.create(
            messages = [
                {"role": "user",
                 "content": [
                     {"type":"text", "text":prompt},
                     {"type":"image_url",
                      "image_url":{
                          "url":f"data:image/jpg;base64,{base64_image}",
                      }}
                 ]
                }
            ],
            model = model
        )
    except Exception as e:
        raise RuntimeError(f"Error calling Groq API: {e}") from e
    return chat_completion

prompt = 'Describe the image'

result = image_to_text(client, llava_model, base64_image, prompt)
st.write(result)