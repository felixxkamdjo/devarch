-- content-service/db/schema.sql


-- CATEGORIES
CREATE TABLE IF NOT EXISTS categories (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ARTICLES
CREATE TABLE IF NOT EXISTS articles (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,

    title       TEXT NOT NULL,
    content     TEXT NOT NULL,
    image_url   TEXT,

    author_id   INTEGER NOT NULL,
    author_name TEXT,

    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,

    status      TEXT DEFAULT 'draft',

    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- COMMENTS
CREATE TABLE IF NOT EXISTS comments (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,

    text       TEXT NOT NULL,

    author_id  INTEGER NOT NULL,
    author_name TEXT,

    article_id INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);