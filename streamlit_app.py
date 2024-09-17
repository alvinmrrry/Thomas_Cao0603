import base64
from io import BytesIO
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from groq import Groq
from PIL import Image
from config import groq_api_key
import io

llava_model = 'llava-v1.5-7b-4096-preview'
llama_model='llama-3.1-70b-versatile'

def main():
    # Initialize session state
    if "button_id" not in st.session_state:
        st.session_state["button_id"] = ""
    if "color_to_label" not in st.session_state:
        st.session_state["color_to_label"] = {}

    # Define pages
    PAGES = {
        "Basic example": full_app,
    }

    # Select page
    page = st.sidebar.selectbox("Page:", options=list(PAGES.keys()))
    PAGES[page]()

def full_app():
    # Configure canvas parameters
    st.sidebar.header("Configuration")
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    if drawing_mode == "point":
        point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
    else:
        point_display_radius = 0  # default value
    stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
    bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
    if bg_image:
        bg_image = Image.open(bg_image)
    else:
        bg_image = None
    realtime_update = st.sidebar.checkbox("Update in realtime", True)

    # Create canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=bg_image,
        update_streamlit=realtime_update,
        height=550,
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius,
        display_toolbar=st.sidebar.checkbox("Display toolbar", True),
        key="full_app",
    )

    # Process canvas result
    if canvas_result.image_data is not None and canvas_result.image_data.size > 0:
        image = Image.open(BytesIO(canvas_result.image_data))
        image_data = np.array(image)
        image_data = image_data[:, :, :3]  # Remove alpha channel
        image_data = image_data / 255.0  # Normalize to [0, 1]
        image_data = image_data.astype(np.float32)
        process_canvas_result(image_data)

def process_canvas_result(image_data):
    # Encode the resized image to base64
    image_data = base64.b64encode(image_data).decode("utf-8")

    # Initialize Groq client
    client = Groq(api_key=groq_api_key)

    # Define image-to-text function
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
                        }}}
                    ]])