# handlers/auth.py

from services import (
    register_user,
    login_user,
    get_current_user
)

from utils import (
    parse_json_body,
    send_json,
    send_error,
    read_bearer_token
)


def register_handler(handler):

    try:

        body = parse_json_body(handler)

        register_user(
            user_firstname = body.get("user_firstname"),
            user_lastname  = body.get("user_lastname"),
            email          = body.get("email"),
            password       = body.get("password")
        )

        # Login automatique après inscription
        auth_result = login_user(
            email    = body.get("email"),
            password = body.get("password")
        )

        send_json(handler, {
            "success": True,
            "message": "User registered successfully.",
            "data": auth_result
        }, 201)

    except ValueError as error:

        send_error(handler, str(error), 400)

    except Exception:

        send_error(handler, "Internal server error.", 500)
        

def login_handler(handler):
    try:
        body = parse_json_body(handler)

        auth_result = login_user(
            email=    body.get("email"),
            password= body.get("password")
        )

        send_json(handler, {
            "success": True,
            "message": "Login successful.",
            "data":    auth_result
        }, 200)

    except ValueError as error:
        send_error(handler, str(error), 401)

    except Exception:
        send_error(handler, "Internal server error.", 500)


def current_user_handler(handler):
    try:
        token = read_bearer_token(handler)
        user  = get_current_user(token)

        send_json(handler, {
            "success": True,
            "user":    user
        }, 200)

    except ValueError as error:
        send_error(handler, str(error), 401)

    except Exception:
        send_error(handler, "Internal server error.", 500)