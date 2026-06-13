#

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "articles.db")
SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")

conn = sqlite3.connect(DB_PATH)
with open(SCHEMA) as f:
    conn.executescript(f.read())
conn.commit()

count = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
print(f"  Schema OK — {count} article(s) existant(s)")
print(count)  # dernière ligne lue par le shell

conn.close()
