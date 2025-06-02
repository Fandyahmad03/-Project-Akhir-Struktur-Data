import sqlite3
import os

# Tentukan lokasi file database
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, '..', 'database.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Buat tabel users
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
''')

# Buat tabel uploads
c.execute('''
    CREATE TABLE IF NOT EXISTS uploads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        filename TEXT,
        score REAL
    )
''')

# Buat tabel flags
c.execute('''
    CREATE TABLE IF NOT EXISTS flags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        upload_id INTEGER,
        reason TEXT
    )
''')


conn.commit()
conn.close()
print("✅ Database initialized with all required tables!")
