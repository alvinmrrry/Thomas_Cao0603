import requests
import json
import streamlit as st
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

# Configuration
groq_api_key = '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'
search_api_url = "https://google.serper.dev/search"
search_api_key = '2203d27aa32a1d92275134fb632bf009714b2476'

def get_search_results(query):
    """Make a POST request to the search API with the query."""
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': search_api_key,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", search_api_url, headers=headers, data=payload)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        st.error(f"Error fetching search results: {e}")
        return None

def create_conversation_chain(model_name, system_prompt, human_input):
    """Create a conversation chain using the LangChain LLM."""
    groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model_name)
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        HumanMessagePromptTemplate.from_template("{human_input}"),
    ])
    conversation = LLMChain(llm=groq_chat, prompt=prompt, verbose=True)
    return conversation.predict(human_input=human_input)

def main():
    st.sidebar.title('Customization')
    system_prompt = st.sidebar.text_input("System prompt:")
    model = st.sidebar.selectbox(
        'Choose a model',
        ['llama-3.1-70b-versatile', 'llama-3.1-8b-instant',
            'llama3-70b-8192', 'llama3-8b-8192']
    )

    query = st.text_input('Please input the query:')
    if query:
        search_results = get_search_results(query)
        if search_results:
            response = create_conversation_chain(model, system_prompt, search_results)
            st.write("Chatbot:", response)

if __name__ == "__main__":
    main()