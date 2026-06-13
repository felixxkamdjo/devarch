# utils/http.py

import json


def parse_json_body(handler):
    """
    Reads and parses a JSON request body.
    """

    try:

        content_length = int(handler.headers.get("Content-Length", 0))

        if content_length == 0:
            return {}

        raw_body = handler.rfile.read(content_length)

        decoded_body = raw_body.decode("utf-8")

        body = json.loads(decoded_body)

        return body

    except json.JSONDecodeError:
        raise ValueError("Invalid JSON body.")


def send_json(handler, data, status_code=200):
    """
    Sends a JSON response.
    """

    response = json.dumps(data).encode("utf-8")

    handler.send_response(status_code)

    handler.send_header("Content-Type", "application/json")

    handler.send_header("Content-Length", str(len(response)))

    handler.end_headers()

    handler.wfile.write(response)


def read_bearer_token(handler):
    """
    Reads the Bearer token from Authorization header.
    """

    authorization_header = handler.headers.get("Authorization")

    if not authorization_header:
        raise ValueError("Authorization header is missing.")

    if not authorization_header.startswith("Bearer "):
        raise ValueError("Invalid Authorization header format.")

    token = authorization_header.replace("Bearer ", "").strip()

    return token


def send_error(handler, message, status_code=400):
    """
    Sends a standardized JSON error response.
    """

    error_response = {"success": False, "error": message}

    send_json(handler=handler, data=error_response, status_code=status_code)
