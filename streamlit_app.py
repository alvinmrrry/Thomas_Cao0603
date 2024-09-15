import streamlit as st
import time

st.title("Streamlit Write Stream Example")

# Stream data generation
def generate_data():
    for i in range(10):
        yield f"Stream data point: {i}"
        time.sleep(1)  # Simulating delay for streaming

st.sidebar("Streamlit Write Stream Example")

# Using the st.write_stream function
if st.button("Start Streng"):
    with st.empty():  # Creates an empty container
        for piece in generate_data():
            st.write(piece)