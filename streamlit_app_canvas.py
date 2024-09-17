import base64
from io import BytesIO
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from groq import Groq
from config import groq_api_key
import io
import numpy as np

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

    bg_image_pil = None
    if bg_image is not None:
        bg_image_pil = Image.open(bg_image)
        bg_image_pil = bg_image_pil.convert("RGB")  # Convert to RGB
        st.sidebar.image(bg_image_pil, caption="Background image", use_column_width=True)

    realtime_update = st.sidebar.checkbox("Update in realtime", True)

    # Create canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="" if bg_image_pil else bg_color,
        background_image=bg_image_pil,
        update_streamlit=realtime_update,
        height=550,
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius,
        display_toolbar=st.sidebar.checkbox("Display toolbar", True),
        key="full_app",
    )

    # Process canvas result
    if canvas_result.image_data is not None:
        image = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGB')
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        image_data = img_byte_arr.getvalue()
        if st.button("Submit"):
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
                        }}
                    ]
                    }
                ],
                model=model
            )
        except Exception as e:
            raise RuntimeError(f"Error calling Groq API: {e}") from e
        return chat_completion.choices[0].message.content

    # Define short story generation function
    def short_story(client, image_description):
        chat_completion = client.chat.completions.create(
            messages = [
                {"role": "system",
                "content": "You are a children's book author. Write a short story based on the image description."},
                {"role": "user",
                "content": image_description}
            ],
            model = llama_model
        )

        return chat_completion.choices[0].message.content

    # Generate image description
    prompt = 'Describe the scene in the image, including any visible text, facial expressions, and background. Identify the main subject and its relationship to the surrounding elements'
    image_description = image_to_text(client, llava_model, image_data, prompt)
    st.write(image_description)

    # Generate short story
    short_story_result = short_story(client, image_description)
    st.write('Short story:')
    st.write(short_story_result)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Streamlit Drawable Canvas Demo", page_icon=":pencil2:"
    )
    st.title("Drawable Canvas Demo")
    st.sidebar.subheader("Configuration")
    main()