import sqlite3
import os

DB_PATH = '/data/alerts.db' if os.environ.get('RENDER') else 'alerts.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crypto_id TEXT NOT NULL,
            target_price REAL NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
