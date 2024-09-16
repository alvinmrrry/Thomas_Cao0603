from groq import groq
from config import groq_api_key
import streamlit as st
import base64

client = groq(api_key=groq_api_key)

llava_model='llava-v1.5-7b-4096-preview'
llama31_model='llama-3.1-70b-versatile'

# image encoding
image_path = 'original.jpg'
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string

base64_image = encode_image(image_path)

# image to text function
def image_to_text(client, model, base64_image,prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": base64_image.decode("utf-8")},
        ],
        max_tokens=2048
    )
    return response.choices[0].message.content

prompt = 'Describe the image'

result = image_to_text(client, llava_model, base64_image, prompt)
st.write(result)