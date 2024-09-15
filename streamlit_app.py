import streamlit as st
import time

with st.sidebar:
    st.write("Streamlit Write Streaample")
    if st.button('Click me'):
        st.button('Button clicked!')

st.title("Streamlit Write Stream Example")

# Stream data generation
def generate_data():
    for i in range(10):
        yield f"Stream data point: {i}"
        time.sleep(1)  # Simulating delay for streaming


# Using the st.write_stream function
if st.button("Start Streng"):
    with st.empty():  # Creates an empty container
        for piece in generate_data():
            st.write(piece)

# write a st checkbox
if st.checkbox("Check me！"):
    st.write("Checkbox is checked!")
else:
    st.write("Checkbox is unchecked!")
