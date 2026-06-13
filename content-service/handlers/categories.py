from services.categories import (
    list_categories_service,
    get_category_service,
    create_category_service,
)
from utils.http import send_json, send_error, parse_json_body


def list_categories_handler(handler):
    try:
        categories = list_categories_service()
        send_json(handler, {"success": True, "data": categories})
    except Exception as e:
        send_error(handler, str(e), 500)


def get_category_handler(handler, category_id):
    try:
        category = get_category_service(category_id)
        send_json(handler, {"success": True, "data": category})
    except ValueError as e:
        send_error(handler, str(e), 404)


def create_category_handler(handler):
    try:
        body = parse_json_body(handler)
        category_id = create_category_service(body.get("name"))
        send_json(
            handler,
            {"success": True, "message": "Category created", "id": category_id},
            201,
        )
    except ValueError as e:
        send_error(handler, str(e), 400)
