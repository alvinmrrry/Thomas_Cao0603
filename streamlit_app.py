import base64
from io import BytesIO
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

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

    # Create a canvas component
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
        return_strokes=True
    )

    if canvas_result is not None and 'image_data' in canvas_result:
        do_something(canvas_result['image_data'])   

def do_something(canvas_result):
    if canvas_result:
        # Note: You need to have your own Groq API key and LLaVA model
        groq_api_key = "YOUR_GROQ_API_KEY"
        llava_model = 'llava-v1.5-7b-4096-preview'
        llama31_model='llama-3.1-70b-versatile'

        client = Groq(api_key=groq_api_key)

        # Open the image file
        image = canvas_result.image_data

        # Resize the image to a smaller size (e.g., 800x600)
        image.thumbnail((800, 600))

        # Save the resized image to a bytes buffer
        buffer = BytesIO()
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

if __name__ == "__main__":
    st.set_page_config(
        page_title="Streamlit Drawable Canvas Demo", page_icon=":pencil2:"
    )
    st.title("Drawable Canvas Demo")
    st.sidebar.subheader("Configuration")
    main()