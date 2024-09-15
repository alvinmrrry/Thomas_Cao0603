import streamlit as st
from langchain import agents
from langchain_community.utilities import SerpAPIWrapper

SERPAPI_API_KEY = '2203d27aa32a1d92275134fb632bf009714b2476'

# Load tools
tools = agents.load_tools(["serpapi"])

# Initialize SerpAPI wrapper
serpapi_wrapper = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)

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