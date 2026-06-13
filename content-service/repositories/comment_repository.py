from db import get_connection


def get_comments_by_article(article_id):
    conn = get_connection()

    try:
        cur = conn.cursor()

        query = """
            SELECT *
            FROM comments
            WHERE article_id = ?
            ORDER BY created_at ASC
        """

        cur.execute(query, (article_id,))

        rows = [dict(row) for row in cur.fetchall()]

        return rows

    finally:
        conn.close()


def get_comment_by_id(comment_id):
    conn = get_connection()

    try:
        cur = conn.cursor()

        query = """
            SELECT *
            FROM comments
            WHERE id = ?
        """

        cur.execute(query, (comment_id,))

        row = cur.fetchone()

        return dict(row) if row else None

    finally:
        conn.close()


def create_comment(text, author_id, author_name, article_id):
    conn = get_connection()

    try:
        cur = conn.cursor()

        query = """
            INSERT INTO comments (
                text,
                author_id,
                author_name,
                article_id
            )
            VALUES (?, ?, ?, ?)
        """

        cur.execute(query, (text, author_id, author_name, article_id))

        conn.commit()

        return cur.lastrowid

    finally:
        conn.close()


def update_comment(comment_id, text):
    conn = get_connection()

    try:
        cur = conn.cursor()

        query = """
            UPDATE comments
            SET
                text = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """

        cur.execute(query, (text, comment_id))

        conn.commit()

    finally:
        conn.close()


def delete_comment(comment_id):
    conn = get_connection()

    try:
        cur = conn.cursor()

        query = """
            DELETE FROM comments
            WHERE id = ?
        """

        cur.execute(query, (comment_id,))

        conn.commit()

    finally:
        conn.close()
