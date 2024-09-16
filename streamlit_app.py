from groq import Groq
from config import groq_api_key
import streamlit as st
import base64
from PIL import Image
import io

client = Groq(api_key=groq_api_key)

llava_model = 'llava-v1.5-7b-4096-preview'

st.title('Describe the image')
uploaded_file = st.file_uploader("Choose a JPG file", type=["jpg", "jpeg"])

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

    # image to text function
    def image_to_text(client, model, base64_image, prompt):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "user",
                     "content": [
                         {"type": "text", "text": prompt},
                         {"type": "image_url",
                          "image_url": {
                              "url": f"data:image/jpg;base64,{base64_image}",
                          }}
                     ]
                     }
                ],
                model=model
            )
        except Exception as e:
            raise RuntimeError(f"Error calling Groq API: {e}") from e
        return chat_completion.choices[0].message.content

    prompt = '用中文详细描述这张照片'
    result = image_to_text(client, llava_model, base64_image, prompt)
    st.write(result)