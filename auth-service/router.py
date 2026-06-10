# router.py

from handlers import (
    register_handler,
    login_handler,
    current_user_handler
)

from utils.http import send_error


# Route registry
ROUTES = {

    # Authentication
    ("POST", "/auth/register"): register_handler,

    ("POST", "/auth/login"): login_handler,

    ("GET", "/auth/me"): current_user_handler,
}


def route_request(handler):
    """
    Routes incoming HTTP requests
    to the appropriate handler.
    """

    method = handler.command
    path = handler.path

    # Remove query parameters if present
    path = path.split("?")[0]

    route_key = (method, path)

    target_handler = ROUTES.get(route_key)

    # Route not found
    if not target_handler:

        send_error(
            handler,
            "Route not found.",
            404
        )

        return

    # Execute handler
    target_handler(handler)