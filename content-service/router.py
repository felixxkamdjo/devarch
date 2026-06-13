from handlers.articles import (
    create_article_handler,
    list_articles_handler,
    get_article_handler,
    update_article_handler,
    delete_article_handler,
)
from handlers.categories import (
    list_categories_handler,
    get_category_handler,
    create_category_handler,
)
from handlers.comments import (
    list_comments_handler,
    create_comment_handler,
    update_comment_handler,
    delete_comment_handler,
)
from utils.http import send_error


#  Helpers
def extract_id(path):
    try:
        return int(path.rstrip("/").split("/")[-1])
    except ValueError:
        return None


#  Router
def route_request(handler):
    method = handler.command
    path = handler.path.split("?")[0].rstrip("/")

    #  /articles
    if path == "/articles":
        if method == "GET":
            return list_articles_handler(handler)
        if method == "POST":
            return create_article_handler(handler)

    #  /articles/:id
    if path.startswith("/articles/"):
        parts = path.split("/")  # ['', 'articles', '3', ...]

        # /articles/:id
        if len(parts) == 3:
            article_id = extract_id(path)
            if article_id is None:
                return send_error(handler, "Invalid article ID", 400)
            if method == "GET":
                return get_article_handler(handler, article_id)
            if method == "PUT":
                return update_article_handler(handler, article_id)
            if method == "DELETE":
                return delete_article_handler(handler, article_id)

        # /articles/:id/comments
        if len(parts) == 4 and parts[3] == "comments":
            article_id = extract_id(parts[2])
            if article_id is None:
                return send_error(handler, "Invalid article ID", 400)
            if method == "GET":
                return list_comments_handler(handler, article_id)
            if method == "POST":
                return create_comment_handler(handler, article_id)

    #  /comments/:id
    if path.startswith("/comments/"):
        comment_id = extract_id(path)
        if comment_id is None:
            return send_error(handler, "Invalid comment ID", 400)
        if method == "PUT":
            return update_comment_handler(handler, comment_id)
        if method == "DELETE":
            return delete_comment_handler(handler, comment_id)

    #  /categories
    if path == "/categories":
        if method == "GET":
            return list_categories_handler(handler)
        if method == "POST":
            return create_category_handler(handler)

    if path.startswith("/categories/"):
        category_id = extract_id(path)
        if category_id is None:
            return send_error(handler, "Invalid category ID", 400)
        if method == "GET":
            return get_category_handler(handler, category_id)

    return send_error(handler, "Route not found", 404)
