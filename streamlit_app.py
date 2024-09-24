from groq import Groq
from config import groq_api_key
import streamlit as st
import base64
from PIL import Image
import io

from crewai import Agent, Task, Crew, Process
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool, BaseTool
from langchain_groq import ChatGroq
# Initialize the ChatGroq model
llm = ChatGroq(
    api_key="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",
    model="mixtral-8x7b-32768"
)

client = Groq(api_key=groq_api_key)

llava_model = 'llava-v1.5-7b-4096-preview'
llama31_model='llama-3.1-70b-versatile'

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

    prompt = 'Describe the scene depicted in the image, including the facial expressions of the people and the background. What is the main subject of the image and how does it relate to the rest of the scene?'
    image_description = image_to_text(client, llava_model, base64_image, prompt)
    st.write(image_description)

    # short story generation funtion
    def short_story(client, image_description):
        chat_completion = client.chat.completions.create(
            messages = [
                {"role": "system",
                "content": "You are a children's book author. Write a short story based on the image description."},
                {"role": "user",
                "content": image_description}
            ],
            model = llama31_model
        )
        
        return chat_completion.choices[0].message.content

    # signle image processing 
    short_story = short_story(client, image_description)
    st.write('Short story:')
    st.write(short_story)



st.write('ok')