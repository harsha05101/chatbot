import sqlite3

DB_NAME = "scans.db"

def init_db():
    """Initializes the database schema if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            risk_score INTEGER,
            category TEXT,
            similarity REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_scan(input_text, risk_score, category, similarity):
    """Saves a single scan entry with metric details into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO scans (input_text, risk_score, category, similarity) VALUES (?, ?, ?, ?)',
        (input_text, risk_score, category, similarity)
    )
    conn.commit()
    conn.close()