from handlers.gateway import gateway_handler


def route_request(handler):
    path = handler.path

    # AUTH SERVICE
    if path.startswith("/auth"):
        return gateway_handler(handler, "auth")

    # CONTENT SERVICE — articles, categories, comments
    if (path.startswith("/articles")
            or path.startswith("/categories")
            or path.startswith("/comments")):
        return gateway_handler(handler, "content")

    # MEDIA SERVICE
    if path.startswith("/media") or path.startswith("/upload"):
        return gateway_handler(handler, "media")

    # OPTIONS preflight sur route inconnue
    if handler.command == "OPTIONS":
        handler.send_response(204)
        handler.send_header("Access-Control-Allow-Origin",  "http://localhost:8080")
        handler.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        handler.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        handler.end_headers()
        return

    # NOT FOUND
    handler.send_response(404)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    handler.wfile.write(b'{"error":"Route not found"}')