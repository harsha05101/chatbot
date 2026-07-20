import sqlite3
import json

DB_FILE = "phishguard.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            message TEXT,
            risk_score INTEGER,
            category TEXT,
            similarity REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_scan(message, risk_score, category, similarity):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scan_history (message, risk_score, category, similarity)
        VALUES (?, ?, ?, ?)
    ''', (message, risk_score, category, similarity))
    conn.commit()
    conn.close()