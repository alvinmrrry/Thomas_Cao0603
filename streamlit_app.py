from groq import Groq
from config import groq_api_key
import streamlit as st
import base64

client = Groq(api_key=groq_api_key)

llava_model = 'llava-v1.5-7b-4096-preview'
llama31_model = 'llama-3.1-70b-versatile'

st.title('Describe the image')
uploaded_file = st.file_uploader("Choose a JPG file", type=["jpg", "jpeg"])

if uploaded_file:
    # encode the uploaded image
    base64_image = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

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

    prompt = 'Describe the image'
    result = image_to_text(client, llava_model, base64_image, prompt)
    st.write(result)