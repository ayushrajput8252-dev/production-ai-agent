import sqlite3

def _get_connection():
    conn = sqlite3.connect("memory.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_message TEXT,
            ai_message TEXT
        )
        """
    )
    conn.commit()
    return conn

# SAVE CHAT
def save_chat(session_id, user_msg, ai_msg):
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO memory
        (session_id, user_message, ai_message)
        VALUES (?, ?, ?)
        """,
        (session_id, user_msg, ai_msg),
    )
    conn.commit()
    conn.close()

# LOAD MEMORY
def load_memory(session_id):
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT user_message, ai_message
        FROM memory
        WHERE session_id = ?
        ORDER BY id
        """,
        (session_id,),
    )
    rows = cur.fetchall()
    conn.close()

    history = ""

    for user_msg, ai_msg in rows:

        history += f"User: {user_msg}\n"
        history += f"AI: {ai_msg}\n"

    return history