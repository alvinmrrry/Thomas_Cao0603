import streamlit as st
import time

# Sidebar content
with st.sidebar():
    st.title('Sidebar Title')
    st.write('This is a sidebar')
    option = st.radio('Choose an option:', ['Option 1', 'Option 2', 'Option 3'])

# Main content based on sidebar selection
if option == 'Option 1':
    st.write('You selected Option 1')
elif option == 'Option 2':
    st.write('You selected Option 2')
elif option == 'Option 3':
    st.write('You selected Option 3')

st.title('Streamlit Write Stream Example')

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

# Using the st.button function
if st.button('Start Stream'):
    with st.empty():  # Creates an empty container
        for piece in generate_data():
            st.write(piece)