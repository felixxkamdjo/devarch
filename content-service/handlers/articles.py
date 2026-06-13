from services.articles import (
    create_article_service,
    list_articles_service,
    get_article_service,
    update_article_service,
    delete_article_service,
)
from utils.http import send_json, send_error, parse_json_body
from utils.jwt import verify_token
from utils import read_bearer_token


def create_article_handler(handler):
    try:
        body = parse_json_body(handler)
        token = read_bearer_token(handler)
        payload = verify_token(token)

        create_article_service(
            title=body.get("title"),
            content=body.get("content"),
            author_id=payload["user_id"],
            author_name=payload.get("user_firstname", ""),
            category_id=body.get("category_id"),
            image_url=body.get("image_url"),
        )

        send_json(handler, {"success": True, "message": "Article created"}, 201)

    except ValueError as e:
        send_error(handler, str(e), 400)
    except Exception as e:
        send_error(handler, str(e), 401)


def list_articles_handler(handler):
    try:
        from urllib.parse import urlparse, parse_qs

        qs = parse_qs(urlparse(handler.path).query)
        page = qs.get("page", ["1"])[0]
        limit = qs.get("limit", ["9"])[0]
        category_id = qs.get("category", [None])[0]

        articles = list_articles_service(
            category_id=category_id, page=page, limit=limit
        )

        send_json(handler, {"success": True, "data": articles})

    except Exception as e:
        import traceback

        print(f"[list_articles] {traceback.format_exc()}", flush=True)
        send_error(handler, str(e), 500)


def get_article_handler(handler, article_id):
    try:
        article = get_article_service(article_id)
        send_json(handler, {"success": True, "data": article})
    except ValueError as e:
        send_error(handler, str(e), 404)


def update_article_handler(handler, article_id):
    try:
        body = parse_json_body(handler)
        update_article_service(
            article_id=article_id,
            title=body.get("title"),
            content=body.get("content"),
            status=body.get("status", "draft"),
            category_id=body.get("category_id"),
            image_url=body.get("image_url"),
        )
        send_json(handler, {"success": True, "message": "Article updated"})
    except ValueError as e:
        send_error(handler, str(e), 400)


def delete_article_handler(handler, article_id):
    try:
        delete_article_service(article_id)
        send_json(handler, {"success": True, "message": "Article deleted"})
    except Exception as e:
        send_error(handler, str(e), 500)
