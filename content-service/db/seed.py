# content-service/db/seed.py

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "db", "articles.db")

CATEGORIES = [
    {"name": "Backend"},
    {"name": "DevOps"},
    {"name": "Architecture"},
    {"name": "Frontend"},
    {"name": "Sécurité"},
    {"name": "Bases de données"},
]

ARTICLES = [
    {
        "title":       "Containerizing a Node.js microservices architecture with Docker Compose",
        "content":     "<h2>Why Docker Compose?</h2><p>Docker Compose is the natural starting point for local microservice orchestration.</p><blockquote>Container isolation lets each service fail independently.</blockquote>",
        "author_id":   2,
        "author_name": "Felix Kamdjo",
        "category_id": 2,   # DevOps
        "image_url":   None,
        "status":      "published",
    },
    {
        "title":       "JWT authentication best practices in 2025",
        "content":     "<h2>What is a JWT?</h2><p>A JSON Web Token is a compact, URL-safe means of representing claims between two parties.</p>",
        "author_id":   3,
        "author_name": "Amara Diallo",
        "category_id": 5,   # Sécurité
        "image_url":   None,
        "status":      "published",
    },
    {
        "title":       "Event-driven design with RabbitMQ and Python",
        "content":     "<h2>Why event-driven?</h2><p>Synchronous REST calls between services create tight coupling.</p>",
        "author_id":   4,
        "author_name": "Chen Wei",
        "category_id": 3,   # Architecture
        "image_url":   None,
        "status":      "published",
    },
    {
        "title":       "PostgreSQL indexing strategies for high-traffic APIs",
        "content":     "<h2>The default: B-tree</h2><p>PostgreSQL creates a B-tree index by default.</p>",
        "author_id":   2,
        "author_name": "Felix Kamdjo",
        "category_id": 6,   # Bases de données
        "image_url":   None,
        "status":      "published",
    },
    {
        "title":       "Rate limiting at the nginx layer — a complete guide",
        "content":     "<h2>limit_req_zone</h2><p>Define a shared memory zone that tracks request rates per key.</p>",
        "author_id":   3,
        "author_name": "Amara Diallo",
        "category_id": 5,   # Sécurité
        "image_url":   None,
        "status":      "published",
    },
    {
        "title":       "Building a real-time notification system with WebSockets",
        "content":     "<h2>Introduction</h2><p>WebSockets allow bidirectional communication between client and server.</p>",
        "author_id":   4,
        "author_name": "Chen Wei",
        "category_id": 3,   # Architecture
        "image_url":   None,
        "status":      "draft",
    },
]

COMMENTS = [
    {"text": "Super article, très bien expliqué !",   "author_id": 3, "author_name": "Amara Diallo",  "article_id": 1},
    {"text": "J'ai enfin compris Docker Compose.",     "author_id": 5, "author_name": "Sara Mensah",   "article_id": 1},
    {"text": "Le point sur RS256 est crucial.",        "author_id": 2, "author_name": "Felix Kamdjo",  "article_id": 2},
    {"text": "Merci pour les exemples concrets.",      "author_id": 5, "author_name": "Sara Mensah",   "article_id": 3},
    {"text": "Les indexes partiels m'ont sauvé !",     "author_id": 4, "author_name": "Chen Wei",      "article_id": 4},
]


def run():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    cur.execute("DELETE FROM comments")
    cur.execute("DELETE FROM articles")
    cur.execute("DELETE FROM categories")

    # Categories
    for cat in CATEGORIES:
        cur.execute("INSERT INTO categories (name) VALUES (?)", (cat["name"],))
    print(f"  -  {len(CATEGORIES)} catégories insérées")

    # Articles
    for a in ARTICLES:
        cur.execute(
            """
            INSERT INTO articles
                (title, content, author_id, author_name, category_id, image_url, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (a["title"], a["content"], a["author_id"], a["author_name"],
             a["category_id"], a["image_url"], a["status"]),
        )
        print(f"  -  [{a['status']:9}]  {a['title'][:55]}")

    # Comments
    for c in COMMENTS:
        cur.execute(
            """
            INSERT INTO comments (text, author_id, author_name, article_id)
            VALUES (?, ?, ?, ?)
            """,
            (c["text"], c["author_id"], c["author_name"], c["article_id"]),
        )
    print(f"  -  {len(COMMENTS)} commentaires insérés")

    conn.commit()
    conn.close()
    print(f"\nSeed terminé → {DB_PATH}")


if __name__ == "__main__":
    print("--- Content service seed ---")
    run()