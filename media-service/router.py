from handlers import upload_file_handler, delete_file_handler, get_file_handler

from utils.http import send_error


def route_request(handler):

    method = handler.command
    path = handler.path.split("?")[0]

    # -------------------------
    # UPLOAD
    # -------------------------

    if method == "POST" and path == "/upload":
        return upload_file_handler(handler)

    # -------------------------
    # GET FILE
    # -------------------------

    if method == "GET" and path.startswith("/files/"):
        filename = path.split("/")[-1]
        return get_file_handler(handler, filename)

    # -------------------------
    # DELETE FILE
    # -------------------------

    if method == "DELETE" and path.startswith("/files/"):
        filename = path.split("/")[-1]
        return delete_file_handler(handler, filename)

    return send_error(handler, "Route not found", 404)
