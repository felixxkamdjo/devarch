from services.proxy import forward_request

CORS_HEADERS = [
    ("Access-Control-Allow-Origin", "http://localhost:8080"),
    ("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"),
    ("Access-Control-Allow-Headers", "Content-Type, Authorization"),
]


def add_cors(handler):
    for header, value in CORS_HEADERS:
        handler.send_header(header, value)


def gateway_handler(handler, service_name):

    #  Preflight OPTIONS
    if handler.command == "OPTIONS":
        handler.send_response(204)
        add_cors(handler)
        handler.end_headers()
        return

    #  Normal request
    try:
        content_length = int(handler.headers.get("Content-Length", 0))
        body = None

        if content_length > 0:
            body = handler.rfile.read(content_length)

        response = forward_request(
            service_name=service_name,
            method=handler.command,
            path=handler.path,
            headers=dict(handler.headers),
            body=body,
        )

        handler.send_response(response["status"])

        add_cors(handler)

        for header, value in response["headers"]:
            if header.lower() == "transfer-encoding":
                continue
            handler.send_header(header, value)

        handler.end_headers()
        handler.wfile.write(response["body"])

    except Exception as error:
        import traceback

        print(f"[GATEWAY ERROR] {traceback.format_exc()}", flush=True)

        handler.send_response(500)
        handler.send_header("Content-Type", "application/json")

        add_cors(handler)

        handler.end_headers()
        handler.wfile.write(str(error).encode())
