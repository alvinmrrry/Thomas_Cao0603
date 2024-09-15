import streamlit as st
import time

st.sidebar("Streamlit Write Stream Example")

st.title("Streamlit Write Stream Example")



# Stream data generation
def generate_data():
    """
    Generates a sequence of strings, with a delay of 1 second between each generation.
    
    Yields:
        str: A string of the form "Stream data point: <i>"
    """
    for i in range(10):
        yield f"Stream data point: {i}"
        time.sleep(1)  # Simulating delay for streaming


# Using the st.write_stream function
if st.button("Start Streng"):
    with st.empty():  # Creates an empty container
        for piece in generate_data():
            st.write(piece)