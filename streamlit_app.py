from config import groq_api_key, search_api_key
import streamlit as st
import os
from crewai import Agent, Task, Crew
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool, BaseTool
from langchain_groq import ChatGroq

llava_model = 'llava-v1.5-7b-4096-preview'
llama31_model='llama-3.1-70b-versatile'

st.title('Describe the image')

# Initialize the ChatGroq model
llm = ChatGroq(
    api_key=os.getenv("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"),
    model="mixtral-8x7b-32768"
)