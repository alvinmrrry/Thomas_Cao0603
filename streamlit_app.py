import streamlit as st
import sqlite3
import asyncio
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
from functools import wraps

# Create a Groq model
# model = GroqModel('llama-3.3-70b-versatile', api_key='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')
model = GroqModel('llama-3.1-8b-instant', api_key='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')
agent = Agent(model)

# Custom exception for rate limit errors
class SDKError(Exception):
    pass

def retry_with_backoff(func, max_retries=10, initial_delay=3):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        delay = initial_delay
        for attempt in range(max_retries):
            try:
                return await func(*args, **kwargs)
            except SDKError as e: # type: ignore
                if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                    await asyncio.sleep(delay)
                    delay *= 2
                else:
                    raise
    return wrapper

@agent.tool
async def get_player_goals(_: RunContext, player_name: str) -> str:
    player_name = player_name.lower()
    
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    
    c.execute('SELECT goals FROM players WHERE name = ?', (player_name,))
    result = c.fetchone()
    
    if result:
        conn.close()
        return str(result[0])
    
    input_names = player_name.split()
    for name in input_names:
        c.execute('SELECT name, goals FROM players WHERE name LIKE ?', (f'%{name}%',))
        result = c.fetchone()
        if result:
            conn.close()
            return str(result[1])
    
    conn.close()
    return f"Player {player_name} not found in database."

@agent.system_prompt
def name_matching_instruction(_: RunContext) -> str:
    return """CRITICAL INSTRUCTIONS: DO NOT attempt to correct player names or suggest full names. 
    Use the exact input name as provided to query the tool."""

async def init_database():
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS players
                 (name TEXT PRIMARY KEY, goals INTEGER)''')
    
    players = [
        ('lionel messi', 100),
        ('lionel messy', 102),
        ('cristian fei', 66),
        ('cristiano ronaldo', 108),
        ('tom charlie', 10),
        ('tommy lee', 30),
        ('tomorrow', 50),
    ]
    
    c.executemany('INSERT OR REPLACE INTO players VALUES (?, ?)', players)
    conn.commit()
    conn.close()

asyncio.run(init_database())

async def get_consistent_response(prompt, max_attempts=10):
    responses = []
    last_response = None
    attempt = 0
    
    retry_agent_run = retry_with_backoff(agent.run)
    
    while attempt < max_attempts:
        response = await retry_agent_run(prompt)
        response = response.data
        responses.append(response)
        
        if last_response is not None and response == last_response:
            return response
        last_response = response
        attempt += 1
    
    # 如果尝试了 max_attempts 次仍然没有得到两次相同的结果，就返回最常见的结果
    return max(set(responses), key=responses.count)

# Streamlit app
# Streamlit app
def main():
    try:
        st.title("Groq AI Chat Completion")
        st.write("Get answers from database based on fast language models")

        # Get user input
        # st.header("Enter a player's name")
        player_name = st.text_input("Enter a player's name")

        if player_name:
            prompt = f"Get the number of goals scored by {player_name}. Use the get_player_goals tool."
            result = asyncio.run(get_consistent_response(prompt))
            st.write("Goals:")
            st.write(result)
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()