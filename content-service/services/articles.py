from repositories.article_repository import (
    create_article,
    get_all_articles,
    get_article_by_id,
    update_article,
    delete_article
)
from events.publisher import publish

def create_article_service(title, content, author_id, author_name=None,
                            category_id=None, image_url=None):
    if not title or not title.strip():
        raise ValueError("Title is required.")
    if not content or not content.strip():
        raise ValueError("Content is required.")
    if not author_id:
        raise ValueError("author_id is required.")
    
    article_id = create_article(
        title=title.strip(),
        content=content,
        author_id=author_id,
        author_name=author_name,
        category_id=category_id,
        image_url=image_url,
        status="draft"
    )

    publish("article.published", {
        "article_id":  article_id,
        "title":       title.strip(),
        "author_id":   author_id,
        "author_name": author_name or "",
    })

    return article_id


def list_articles_service(category_id=None, page=1, limit=9):
    offset = (int(page) - 1) * int(limit)
    return get_all_articles(
        status="published",
        category_id=category_id,
        limit=int(limit),
        offset=offset
    )


def get_article_service(article_id):
    article = get_article_by_id(article_id)
    if not article:
        raise ValueError("Article not found.")
    return article


def update_article_service(article_id, title, content, status,
                            category_id=None, image_url=None):
    if not title or not content:
        raise ValueError("Title and content are required.")
    update_article(article_id, title, content, status, category_id, image_url)


def delete_article_service(article_id, requesting_user_id, requesting_user_role):
    article = get_article_by_id(article_id)
    if article["author_id"] != requesting_user_id and requesting_user_role != "admin":
        raise PermissionError("Access denied.")
    delete_article(article_id)