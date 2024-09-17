import base64
import json
import os
import re
import time
import uuid
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from svgpathtools import parse_path


def main():
    if "button_id" not in st.session_state:
        st.session_state["button_id"] = ""
    if "color_to_label" not in st.session_state:
        st.session_state["color_to_label"] = {}
    PAGES = {
        "Basic example": full_app,
    }
    page = st.sidebar.selectbox("Page:", options=list(PAGES.keys()))
    PAGES[page]()

def full_app():
    st.sidebar.header("Configuration")
    st.markdown(
        """
    Draw on the canvas, get the drawings back to Streamlit!
    * Configure canvas in the sidebar
    * In transform mode, double-click an object to remove it
    * In polygon mode, left-click to add a point, right-click to close the polygon, double-click to remove the latest point
    """
    )

    # Specify canvas parameters in application
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    if drawing_mode == "point":
        point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
    bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
    realtime_update = st.sidebar.checkbox("Update in realtime", True)

    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        height=150,
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius if drawing_mode == "point" else 0,
        display_toolbar=st.sidebar.checkbox("Display toolbar", True),
        key="full_app",
    )

    # Do something interesting with the image data and paths
    # if canvas_result.image_data is not None:
    #     st.image(canvas_result.image_data)
    # if canvas_result.json_data is not None:
    #     objects = pd.json_normalize(canvas_result.json_data["objects"])
    #     for col in objects.select_dtypes(include=["object"]).columns:
    #         objects[col] = objects[col].astype("str")
    #     st.dataframe(objects)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Streamlit Drawable Canvas Demo", page_icon=":pencil2:"
    )
    st.title("Drawable Canvas Demo")
    st.sidebar.subheader("Configuration")
    main()


# from groq import Groq
# from config import groq_api_key
# import streamlit as st
# import base64
# from PIL import Image
# import io

# client = Groq(api_key=groq_api_key)

# llava_model = 'llava-v1.5-7b-4096-preview'
# llama31_model='llama-3.1-70b-versatile'

# st.title('Describe the image')
# uploaded_file = st.file_uploader("Choose a JPG file", type=["jpg", "jpeg"])

# if uploaded_file:
    
#     # Open the image file
#     image = Image.open(uploaded_file)

#     # Resize the image to a smaller size (e.g., 800x600)
#     image.thumbnail((800, 600))

#     # Save the resized image to a bytes buffer
#     buffer = io.BytesIO()
#     image.save(buffer, format="JPEG")

#     # Encode the resized image to base64
#     base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

#     # image to text function
#     def image_to_text(client, model, base64_image, prompt):
#         try:
#             chat_completion = client.chat.completions.create(
#                 messages=[
#                     {"role": "user",
#                      "content": [
#                          {"type": "text", "text": prompt},
#                          {"type": "image_url",
#                           "image_url": {
#                               "url": f"data:image/jpg;base64,{base64_image}",
#                           }}
#                      ]
#                      }
#                 ],
#                 model=model
#             )
#         except Exception as e:
#             raise RuntimeError(f"Error calling Groq API: {e}") from e
#         return chat_completion.choices[0].message.content

#     prompt = 'Describe the scene depicted in the image, including the facial expressions of the people and the background. What is the main subject of the image and how does it relate to the rest of the scene?'
#     image_description = image_to_text(client, llava_model, base64_image, prompt)
#     st.write(image_description)

#     # short story generation funtion
#     def short_story(client, image_description):
#         chat_completion = client.chat.completions.create(
#             messages = [
#                 {"role": "system",
#                 "content": "You are a children's book author. Write a short story based on the image description."},
#                 {"role": "user",
#                 "content": image_description}
#             ],
#             model = llama31_model
#         )
        
#         return chat_completion.choices[0].message.content

#     # signle image processing 
#     short_story = short_story(client, image_description)
#     st.write('Short story:')
#     st.write(short_story)