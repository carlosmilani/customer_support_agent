# app/repositories/feedback_repo.py
import asyncio
import aiosqlite
from datetime import datetime

# Updated database name to English
DB_PATH = "support_agent.db"

class FeedbackRepository:
    """
    Handles all database persistence logic. 
    Strictly follows the 'SQL only' repository pattern.
    """
    
    @staticmethod
    async def init_db():
        """
        Initializes the SQLite database and creates the interactions table if it doesn't exist.
        """
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT,
                    identified_route TEXT,
                    agent_response TEXT,
                    created_at TIMESTAMP
                )
            """)
            await db.commit()

    @staticmethod
    async def save_interaction(state: dict):
        """
        Saves the final LangGraph state into the SQL database.
        """
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                """
                INSERT INTO interactions 
                (user_input, identified_route, agent_response, created_at) 
                VALUES (?, ?, ?, ?)
                """,
                (
                    state["input"], 
                    state["route"], 
                    state["response"], 
                    datetime.now().isoformat()
                )
            )
            await db.commit()
        print(f"--- [Repository] Data persisted to {DB_PATH} successfully! ---")