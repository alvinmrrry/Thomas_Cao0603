from groq import Groq
from config import groq_api_key
import streamlit as st
import base64
from PIL import Image
import io
import requests
import json

client = Groq(api_key=groq_api_key)

models = {
    "LLaVA 1.5 7B": "llava-v1.5-7b-4096-preview",
    "LLaMA 3.1 70B": "llama-3.1-70b-versatile",
}

st.title('Describe the image')

uploaded_file = st.file_uploader("Choose a JPG file", type=["jpg", "jpeg"])

if uploaded_file:
    if uploaded_file.type not in ["image/jpeg", "image/jpg"]:
        st.error("Invalid file type. Please upload a JPEG file.")
    if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
        st.error("File size exceeds 10MB. Please upload a smaller file.")

    # Open the image file
    image = Image.open(uploaded_file)

    # Resize the image to a smaller size (e.g., 800x600)
    image.thumbnail((800, 600))

    # Display the uploaded image
    st.image(image, caption="Uploaded Image")

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
        except requests.exceptions.RequestException as e:
            st.error("Error calling Groq API: Request Exception")
        except json.JSONDecodeError as e:
            st.error("Error calling Groq API: JSON Decode Error")
        except Exception as e:
            st.error(f"Error calling Groq API: {e}")
        return chat_completion.choices[0].message.content

    selected_model = st.selectbox("Select a model", list(models.keys()))
    model = models[selected_model]

    prompt = st.text_input("Enter a prompt", "Describe the image")

    result = image_to_text(client, model, base64_image, prompt)
    st.write(result)