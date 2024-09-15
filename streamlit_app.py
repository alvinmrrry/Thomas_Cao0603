import streamlit as st
import time

st.sidebar.title("Streamlit Write Stream Example")

st.title("Streamlit Write Stream Example")



# Stream data generation
def generate_data():
    """Generate a sequence of string data points for streaming.

    This is a generator function that yields a sequence of 10 string data points
    at a rate of one per second. The strings are of the form "Stream data point: N"
    where N is the index of the data point in the sequence (0-9).

    The function uses the time.sleep() function to introduce a delay between
    yields, simulating the delay that would occur when streaming data in real time.

    Yields:
        str: A string data point of the form "Stream data point: N"
    """
    for i in range(10):
        yield f"Stream data point: {i}"
        time.sleep(1)  # Simulating delay for streaming


# Using the st.write_stream function
if st.button("Start Streng"):
    with st.empty():  # Creates an empty container
        for piece in generate_data():
            st.write(piece)