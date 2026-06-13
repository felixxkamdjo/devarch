from db import get_connection


def create_article(
    title,
    content,
    author_id,
    author_name=None,
    category_id=None,
    image_url=None,
    status="draft",
):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO articles
            (title, content, author_id, author_name, category_id, image_url, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (title, content, author_id, author_name, category_id, image_url, status),
    )
    conn.commit()
    article_id = cur.lastrowid
    conn.close()
    return article_id


def get_all_articles(status="published", category_id=None, limit=9, offset=0):
    conn = get_connection()
    cur = conn.cursor()
    params = [status]
    query = """
        SELECT a.*, c.name AS category_name
        FROM articles a
        LEFT JOIN categories c ON a.category_id = c.id
        WHERE a.status = ?
    """
    if category_id:
        query += " AND a.category_id = ?"
        params.append(category_id)

    query += " ORDER BY a.created_at DESC LIMIT ? OFFSET ?"
    params += [limit, offset]

    cur.execute(query, params)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def get_article_by_id(article_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT a.*, c.name AS category_name
        FROM articles a
        LEFT JOIN categories c ON a.category_id = c.id
        WHERE a.id = ?
        """,
        (article_id,),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def update_article(
    article_id, title, content, status, category_id=None, image_url=None
):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE articles
        SET title = ?, content = ?, status = ?,
            category_id = ?, image_url = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (title, content, status, category_id, image_url, article_id),
    )
    conn.commit()
    conn.close()


def delete_article(article_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    conn.commit()
    conn.close()
