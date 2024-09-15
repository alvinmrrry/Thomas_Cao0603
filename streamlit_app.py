import streamlit as st
from groq import Groq
from langchain_groq import ChatGroq
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import load_tools

groq_api_key = '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'
SERPAPI_API_KEY = '2203d27aa32a1d92275134fb632bf009714b2476'

tools = load_tools(["serpapi"])
serpapi_wrapper = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)

# Function to search using SerpAPI
def search(query):
    results = serpapi_wrapper.run(query)
    return results

# Example usage
query = "What is the latest news in AI?"
search_results = search(query)
st.write(search_results)