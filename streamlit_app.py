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

# 创建一个简单的下拉框
option = st.selectbox(
    
    ['红色', '绿色', '蓝色'])

st.write('你选择了:', option)
