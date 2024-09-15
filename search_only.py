import streamlit as st
from langchain import agents
from langchain_community.utilities import SerpAPIWrapper

# Set the SERPAPI_API_KEY as an environment variable
import os
os.environ['SERPAPI_API_KEY'] = 'a4a2ff56f44eb5b47674a37a1ba7399b0a4d6a2df3dc9bc9a1ed370552a5572c'

# Load tools
tools = agents.load_tools(["serpapi"])

# Initialize SerpAPI wrapper
serpapi_wrapper = SerpAPIWrapper()

# Function to search using SerpAPI
def search(query):
    try:
        # Run the query on SerpAPI
        results = serpapi_wrapper.run(query)
        return results
    except Exception as e:
        # Handle any exceptions
        st.error(f"An error occurred: {e}")
        return None

# Example usage
query = "What is the latest news in AI?"
search_results = search(query)
if search_results:
    st.write(search_results)