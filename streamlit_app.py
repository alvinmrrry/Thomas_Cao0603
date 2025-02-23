import streamlit as st
import sqlite3
import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from functools import wraps

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
            except Exception as e:
                if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                    await asyncio.sleep(delay)
                    delay *= 2
                else:
                    raise
    return wrapper

@retry_with_backoff
async def fetch_data_from_database(player_name):
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('SELECT goals FROM players WHERE name = ?', (player_name,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return f"Player {player_name} not found in database."

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

# Streamlit app
def main():
    st.title("Groq AI Chat Completion")
    st.write("Get answers from fast language models")

    # Get user input
    st.header("Enter a player's name")
    player_name = st.text_area("")

    # Get chat completion
    if st.button("Get Data"):
        result = asyncio.run(fetch_data_from_database(player_name))
        st.write("Goals:")
        st.write(result)

if __name__ == "__main__":
    main()