import streamlit as st
import sqlite3
import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# Create a Groq model
model = GroqModel('llama-3.3-70b-versatile', api_key='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')
agent = Agent(model)

def retry_with_backoff(func, max_retries=10, initial_delay=3):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        delay = initial_delay
        for attempt in range(max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                    await asyncio.sleep(delay)
                    delay *= 2
                else:
                    raise
    return wrapper

@agent.tool
async def get_player_goals(_: Agent.Context, player_name: str) -> str:
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
def name_matching_instruction(_: Agent.Context) -> str:
    return """CRITICAL INSTRUCTION: DO NOT attempt to correct player names or suggest full names. 
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

@agent.system_action
async def get_consistent_response(_: Agent.Context, prompt: str, num_attempts=3) -> str:
    responses = []
    tasks = []
    
    for _ in range(num_attempts):
        task = agent.run(prompt)
        tasks.append(task)
    
    responses = await asyncio.gather(*tasks)
    responses = [r.data for r in responses]
    
    if len(set(responses)) == 1:
        # print("All responses were consistent")
        return responses[0]
    else:
        return max(set(responses), key=responses.count)

asyncio.run(init_database())

# Streamlit app
def main():
    st.title("Groq AI Chat Completion")
    st.write("Get answers from fast language models")

    # Get user input
    st.header("Enter a player's name")
    player_name = st.text_area("").strip().lower()

    # Get chat completion
    if st.button("Get Data"):
        if player_name:
            prompt = f"Get the number of goals scored by {player_name}. Use the get_player_goals tool."
            result = asyncio.run(agent.run(prompt))
            st.write("Goals:")
            st.write(result.data)
        else:
            st.write("Please enter a player's name.")

if __name__ == "__main__":
    main()