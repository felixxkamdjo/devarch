from services.comments import (
    list_comments_service,
    create_comment_service,
    update_comment_service,
    delete_comment_service,
)
from utils.http import send_json, send_error, parse_json_body
from utils.jwt import verify_token
from utils import read_bearer_token


def list_comments_handler(handler, article_id):
    try:
        comments = list_comments_service(article_id)
        send_json(handler, {"success": True, "data": comments})
    except Exception as e:
        send_error(handler, str(e), 500)


def create_comment_handler(handler, article_id):
    try:
        body = parse_json_body(handler)
        token = read_bearer_token(handler)
        payload = verify_token(token)

        create_comment_service(
            text=body.get("text"),
            author_id=payload["user_id"],
            author_name=payload.get("user_firstname", ""),
            article_id=article_id,
        )

        send_json(handler, {"success": True, "message": "Comment created"}, 201)

    except ValueError as e:
        send_error(handler, str(e), 400)
    except Exception as e:
        send_error(handler, str(e), 401)


def update_comment_handler(handler, comment_id):
    try:
        body = parse_json_body(handler)
        update_comment_service(comment_id, body.get("text"))
        send_json(handler, {"success": True, "message": "Comment updated"})
    except ValueError as e:
        send_error(handler, str(e), 400)


def delete_comment_handler(handler, comment_id):
    try:
        delete_comment_service(comment_id)
        send_json(handler, {"success": True, "message": "Comment deleted"})
    except Exception as e:
        send_error(handler, str(e), 500)
