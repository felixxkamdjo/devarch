from utils import send_json, send_error
from services import save_file, delete_file, get_file_path


# UPLOAD
def upload_file_handler(handler):

    try:

        content_length = int(handler.headers.get("Content-Length", 0))

        if content_length == 0:
            return send_error(handler, "Empty file", 400)

        file_data = handler.rfile.read(content_length)

        filename = handler.headers.get("X-Filename", "file.bin")
        file_type = handler.headers.get("X-Type", "files")

        result = save_file(file_data, filename, file_type)

        send_json(handler, {"success": True, "data": result}, 201)

    except Exception:
        send_error(handler, "Upload failed", 500)


# DELETE
def delete_file_handler(handler, filename):

    try:

        success = delete_file(filename)

        if not success:
            return send_error(handler, "File not found", 404)

        send_json(handler, {"success": True, "message": "File deleted"})

    except Exception:
        send_error(handler, "Delete failed", 500)


# GET FILE
def get_file_handler(handler, filename):

    try:

        path = get_file_path(filename)

        send_json(handler, {"success": True, "path": path})

    except Exception:
        send_error(handler, "Error retrieving file", 500)
