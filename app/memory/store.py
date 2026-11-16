import sqlite3
from pathlib import Path

class ConversationStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL, conversation_id TEXT NOT NULL,
                role TEXT NOT NULL, content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_messages ON messages(user_id, conversation_id, id)')

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def add(self, user_id, conversation_id, role, content):
        with self.connect() as conn:
            conn.execute("INSERT INTO messages(user_id,conversation_id,role,content) VALUES(?,?,?,?)",
                         (user_id, conversation_id, role, content))

    def history(self, user_id, conversation_id, limit=20):
        with self.connect() as conn:
            rows = conn.execute("SELECT role,content,created_at FROM messages WHERE user_id=? AND conversation_id=? ORDER BY id DESC LIMIT ?",
                                (user_id, conversation_id, limit)).fetchall()
        return [dict(row) for row in reversed(rows)]

    def clear(self, user_id, conversation_id):
        with self.connect() as conn:
            conn.execute("DELETE FROM messages WHERE user_id=? AND conversation_id=?", (user_id, conversation_id))
