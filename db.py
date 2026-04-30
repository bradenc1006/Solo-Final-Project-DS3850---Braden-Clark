import sqlite3

DB_PATH = "freelance.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        hourly_rate REAL NOT NULL,
        contact TEXT,
        active INTEGER DEFAULT 1)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        hours REAL NOT NULL,
        description TEXT,
        FOREIGN KEY(client_id) REFERENCES clients(id))""")

    conn.commit()
    conn.close()
