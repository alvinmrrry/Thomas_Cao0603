from groq import Groq
from config import groq_api_key
import streamlit as st
import base64
from PIL import Image
import io
from click import prompt
from openai import OpenAI

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# Define models
llama31_model = 'llama-3.1-70b-versatile'

# Initialize OpenAI client
openai_client = OpenAI(
    base_url="https://api-inference.huggingface.co/v1/",
    api_key="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"
)

st.title('Describe the image')
uploaded_file = st.file_uploader("Choose a JPG file", type=["jpg", "jpeg"])

def describe_image(base64_image, model_name="meta-llama/Llama-3.2-11B-Vision-Instruct", max_tokens=500):

    url = "https://thumbnail1.baidupcs.com/thumbnail/a82217d32q0ec37513885753ad73d44c?fid=1102114614555-250528-310234319461360&rt=pr&sign=FDTAER-DCb740ccc5511e5e8fedcff06b081203-IYZliKb8Yz4MFRMj7%2bFb7eoI%2bZQ%3d&expires=8h&chkbd=0&chkv=0&dp-logid=260284334972795143&dp-callid=0&time=1730775600&size=c1383_u864&quality=90&vuk=1102114614555&ft=image&autopolicy=1"

    prompt = '''
    describe the image
    '''

    messages = [
        {"role": "user", "content": prompt},  # First message asking for a description
        {"role": "system", "content": url}  # Image URL as a separate message
    ]
    response = openai_client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=max_tokens
    )

    if response.choices:
        return response.choices[0].message.content
    else:
        return None



if uploaded_file:

    # Open the image file
    image = Image.open(uploaded_file)

    # Resize the image to a smaller size (e.g., 400x300)
    image.thumbnail((400, 300))

    # Compress the image to reduce the file size
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=50)

    # Encode the resized image to base64
    base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Image to text function
    image_description = describe_image(base64_image)
    st.write(image_description)

    # Short story generation function
    def short_story(image_description, model_name=llama31_model):
        chat_completion = client.chat.completions.create(
            messages = [
                {"role": "system",
                "content": "You are a children's book author. Write a short story based on the image description."},
                {"role": "user",
                "content": image_description}
            ],
            model = model_name
        )

        return chat_completion.choices[0].message.content

    # Single image processing 
    short_story_text = short_story(image_description)
    st.write('Short story:')
    st.write(short_story_text)