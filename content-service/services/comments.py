from repositories.comment_repository import (
    get_comments_by_article,
    get_comment_by_id,
    create_comment,
    update_comment,
    delete_comment,
)


def list_comments_service(article_id):
    return get_comments_by_article(article_id)


def create_comment_service(text, author_id, author_name, article_id):
    if not text or not text.strip():
        raise ValueError("Comment text is required.")
    if not author_id:
        raise ValueError("author_id is required.")
    if not article_id:
        raise ValueError("article_id is required.")
    return create_comment(text.strip(), author_id, author_name, article_id)


def update_comment_service(comment_id, text):
    if not text or not text.strip():
        raise ValueError("Comment text is required.")
    comment = get_comment_by_id(comment_id)
    if not comment:
        raise ValueError("Comment not found.")
    update_comment(comment_id, text.strip())


def delete_comment_service(comment_id):
    delete_comment(comment_id)
