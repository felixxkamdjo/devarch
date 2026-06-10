# 

import os
import sys
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

DB_PATH = os.path.join(BASE_DIR, "db", "auth.db")

from utils.security import hash_password, generate_salt

DEFAULT_PASSWORD = "Password123!"

USERS = [
    {
        "email":          "admin@devarch.io",
        "user_firstname": "Admin",
        "user_lastname":  "DevArch",
        "role":           "admin",
    },
    {
        "email":          "felix@devarch.io",
        "user_firstname": "Felix",
        "user_lastname":  "Kamdjo",
        "role":           "author",
    },
    {
        "email":          "amara@devarch.io",
        "user_firstname": "Amara",
        "user_lastname":  "Diallo",
        "role":           "author",
    },
    {
        "email":          "chen@devarch.io",
        "user_firstname": "Chen",
        "user_lastname":  "Wei",
        "role":           "author",
    },
    {
        "email":          "sara@devarch.io",
        "user_firstname": "Sara",
        "user_lastname":  "Mensah",
        "role":           "author",
    },
]

def run():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute("DELETE FROM users")

    inserted = 0
    for user in USERS:

        # from utils.security import hash_password, generate_salt
        salt          = generate_salt()
        password_hash = hash_password(DEFAULT_PASSWORD, salt)

        cur.execute(
            """
            INSERT INTO users
                (email, user_firstname, user_lastname, role, password_hash, salt)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user["email"],
                user["user_firstname"],
                user["user_lastname"],
                user["role"],
                password_hash,
                salt,
            ),
        )
        inserted += 1
        print(f"  -  {user['email']}  [{user['role']}]")

    conn.commit()
    conn.close()
    
    print(f"\n{inserted} utilisateurs insérés dans {DB_PATH}")
    print(f"Mot de passe par défaut : {DEFAULT_PASSWORD}")

if __name__ == "__main__":
    print("--- Auth service seed ---")
    run()