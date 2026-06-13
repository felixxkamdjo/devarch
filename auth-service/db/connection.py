# connection.py

import sqlite3
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "auth.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def get_connection():
    """
    Opens and configures the SQLite connection.
    Creates auth.db automatically if it does not exist.
    """

    connection = sqlite3.connect(DB_PATH)

    # Returns rows as dictionaries
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    """
    Initializes the database
    and executes the SQL script from schema.sql.
    """

    connection = None

    try:
        # Open connection
        connection = get_connection()

        # Open schema.sql
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            sql_script = schema_file.read()

        # Execute SQL script
        connection.executescript(sql_script)

        # Commit changes
        connection.commit()

        print("Database initialized successfully.")

    except sqlite3.Error as error:
        print(f"SQLite error: {error}")

    finally:
        #  Close connection
        if connection:
            connection.close()
            print("Connection closed.")


if __name__ == "__main__":
    init_db()
