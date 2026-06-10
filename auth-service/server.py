# server.py

from http.server import HTTPServer, BaseHTTPRequestHandler
from router import route_request
from db import init_db


HOST = "0.0.0.0"
PORT = 8002


class AuthHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Main HTTP request handler.
    """

    # POST requests
    def do_POST(self):
        route_request(self)

    # GET requests
    def do_GET(self):
        route_request(self)

    # PUT requests
    def do_PUT(self):
        route_request(self)

    # DELETE requests
    def do_DELETE(self):
        route_request(self)

    # Disable default logs
    def log_message(self, format, *args):
        return


def run_server():
    """
    Initializes database and starts the HTTP server.
    """

    # Initialize database
    init_db()
    
    # Allow port reuse
    HTTPServer.allow_reuse_address = True

    # Create server
    server = HTTPServer(
        (HOST, PORT),
        AuthHTTPRequestHandler
    )

    print(f"Auth service running on {HOST}:{PORT}")

    # Start listening
    server.serve_forever()


if __name__ == "__main__":
    run_server()