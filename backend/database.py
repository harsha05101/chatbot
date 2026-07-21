import sqlite3
import os

# Store the database file in the same directory as this file
DB_NAME = os.path.join(os.path.dirname(__file__), "scans.db")


def init_db():
    """Initializes the SQLite scans table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            risk_score INTEGER DEFAULT 0,
            category TEXT DEFAULT 'Unknown',
            similarity REAL DEFAULT 0.0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def save_scan(input_text, risk_score=0, category="Unknown", similarity=0.0):
    """Saves scan metrics into the SQLite scans database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO scans (input_text, risk_score, category, similarity) VALUES (?, ?, ?, ?)',
            (input_text, risk_score, category, similarity)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Save Error: {e}")