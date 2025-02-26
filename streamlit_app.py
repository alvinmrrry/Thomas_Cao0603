import os
import streamlit as st
from google import genai
from google.genai import types

# Function to generate content from Google GenAI
def generate_content(input_text):
    client = genai.Client(api_key='AIzaSyDBvuL_-rHm8M9Vi-YOYqnbSs0Wcj3gVLA')

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=input_text)],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
    )

    # Generate the content and return as a string
    result = ""
    for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
    ):
        result += chunk.text
    return result

# Streamlit UI
st.title("Google GenAI Content Generator")

# Text input for the user to provide input text
user_input = st.text_area("Enter your input text here:", "")

# When the user clicks the 'Generate' button
if st.button("Generate"):
    if user_input:
        with st.spinner('Generating content...'):
            output = generate_content(user_input)
            st.subheader("Generated Content:")
            st.text(output)  # Display the generated content
    else:
        st.error("Please enter some input text before generating content.")
