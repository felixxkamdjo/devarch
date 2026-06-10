import os
import sqlite3

DB_PATH = os.environ.get("DB_PATH", "/app/db/data.db")

SCHEMA_PATH = os.path.join(
    os.path.dirname(__file__),
    "schema.sql"
)


def get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():
    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()

    conn = get_connection()

    conn.executescript(schema)

    conn.commit()
    conn.close()

    print("[media-service] Database initialized.", flush=True)
