import sqlite3

# CREATE DATABASE
conn = sqlite3.connect("memory.db")

cur = conn.cursor()

# CREATE TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    user_message TEXT,
    ai_message TEXT
)
""")

conn.commit()

# SAVE CHAT
def save_chat(session_id, user_msg, ai_msg):

    cur.execute(
        """
        INSERT INTO memory
        (session_id, user_message, ai_message)
        VALUES (?, ?, ?)
        """,
        (session_id, user_msg, ai_msg)
    )

    conn.commit()

# LOAD MEMORY
def load_memory(session_id):

    cur.execute(
        """
        SELECT user_message, ai_message
        FROM memory
        WHERE session_id = ?
        ORDER BY id
        """,
        (session_id,)
    )

    rows = cur.fetchall()

    history = ""

    for user_msg, ai_msg in rows:

        history += f"User: {user_msg}\n"
        history += f"AI: {ai_msg}\n"

    return history