import streamlit as st
import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# Create a Groq model
model = GroqModel('llama-3.3-70b-versatile', api_key='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')
agent = Agent(model)

# Define a decorator for retrying with backoff
def retry_with_backoff(func, max_retries=10, initial_delay=3):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        delay = initial_delay
        for attempt in range(max_retries):
            try:
                return await func(*args, **kwargs)
            except SDKError as e:
                if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                    await asyncio.sleep(delay)
                    delay *= 2
                else:
                    raise
    return wrapper

# Define a function to get a consistent response from the agent
async def get_consistent_response(prompt, num_attempts=3):
    responses = []
    tasks = []
    
    for _ in range(num_attempts):
        task = retry_with_backoff(agent.run)(prompt)
        tasks.append(task)
    
    responses = await asyncio.gather(*tasks)
    responses = [r.data for r in responses]
    
    if len(set(responses)) == 1:
        return responses[0]
    else:
        return max(set(responses), key=responses.count)

# Streamlit app
def main():
    st.title("Groq AI Chat Completion")
    st.write("Get answers from fast language models")

    # Get user input
    st.header("Enter a question")
    message = st.text_area("")

    # Get model selection
    st.header("Select a model")
    model_options = ["llama-3.3-70b-versatile"]
    model = st.selectbox("Model", options=model_options)

    # Get chat completion
    if st.button("Get Answer"):
        prompt = message
        response = asyncio.run(get_consistent_response(prompt))
        st.write("Answer:")
        st.write(response)

if __name__ == "__main__":
    main()