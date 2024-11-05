from groq import Groq
from config import groq_api_key
import streamlit as st
import base64
from PIL import Image
import io
import openai

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# Define models
llava_model = 'llava-v1.5-7b-4096-preview'
llama31_model = 'llama-3.1-70b-versatile'

# Initialize OpenAI client
openai_client = openai.OpenAI(
    base_url="https://api-inference.huggingface.co/v1/",
    api_key="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"
)

st.title('Describe the image')
uploaded_file = st.file_uploader("Choose a JPG file", type=["jpg", "jpeg"])

def describe_image(base64_image, model_name="meta-llama/Llama-3.2-11B-Vision-Instruct", max_tokens=5000):
    """
    使用 OpenAI 的 Llama 模型描述一张图片。

    Args:
    base64_image (str): 图片的 base64 编码。
    api_key (str): OpenAI 的 API 密钥。
    model_name (str): 使用的模型名称 (默认为 "meta-llama/Llama-3.2-11B-Vision-Instruct")。
    max_tokens (int): 响应的最大长度 (默认为 5000)。

    Returns:
    str: 图片的描述。
    """

    prompt = "describe the image"

    messages = [
        {"role": "user", "content": prompt},
        {"role": "system", "content": f"base64://{base64_image}"}
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

    # Resize the image to a smaller size (e.g., 800x600)
    image.thumbnail((800, 600))

    # Save the resized image to a bytes buffer
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")

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