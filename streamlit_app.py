import base64
from io import BytesIO
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from groq import Groq
from PIL import Image
from config import groq_api_key
import io
import numpy as np

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
        process_canvas_result(canvas_result.image_data)

def process_canvas_result(canvas_result):
    # Convert canvas result to a numpy array
    canvas_image = np.zeros((550, 800, 4), dtype=np.uint8)
    for obj in canvas_result:
        if obj["type"] == "line":
            cv2.line(canvas_image, (obj["x0"], obj["y0"]), (obj["x1"], obj["y1"]), (obj["color"][0], obj["color"][1], obj["color"][2]), obj["width"])
        elif obj["type"] == "rect":
            cv2.rectangle(canvas_image, (obj["x0"], obj["y0"]), (obj["x1"], obj["y1"]), (obj["color"][0], obj["color"][1], obj["color"][2]), obj["width"])
        elif obj["type"] == "circle":
            cv2.circle(canvas_image, (obj["x0"], obj["y0"]), obj["radius"], (obj["color"][0], obj["color"][1], obj["color"][2]), obj["width"])

    # Save the numpy array to a bytes buffer
    buffer = BytesIO()
    cv2.imwrite(buffer, canvas_image)
    buffer.seek(0)

    # Encode the bytes buffer to base64
    base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

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
            model = LLAMA_MODEL
        )

        return chat_completion.choices[0].message.content

    # Generate image description
    prompt = 'Describe the scene depicted in the image, including the facial expressions of the people and the background. What is the main subject of the image and how does it relate to the rest of the scene?'
    image_description = image_to_text(client, LLAVA_MODEL, base64_image, prompt)
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