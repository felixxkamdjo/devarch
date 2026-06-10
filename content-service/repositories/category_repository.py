from db import get_connection


def get_all_categories():
    conn = get_connection()

    try:
        cur = conn.cursor()

        query = """
            SELECT *
            FROM categories
            ORDER BY name ASC
        """

        cur.execute(query)

        rows = [dict(row) for row in cur.fetchall()]
        return rows

    finally:
        conn.close()


def get_category_by_id(category_id):
    conn = get_connection()

    try:
        cur = conn.cursor()

        query = """
            SELECT *
            FROM categories
            WHERE id = ?
        """

        cur.execute(query, (category_id,))

        row = cur.fetchone()

        return dict(row) if row else None

    finally:
        conn.close()


def create_category(name):
    conn = get_connection()

    try:
        cur = conn.cursor()

        query = """
            INSERT INTO categories (name)
            VALUES (?)
        """

        cur.execute(query, (name,))

        conn.commit()

        return cur.lastrowid

    finally:
        conn.close()