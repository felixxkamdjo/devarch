from http.server import HTTPServer, BaseHTTPRequestHandler
from router import route_request
from db.connection import init_db


HOST = "0.0.0.0"
PORT = 8003


class ArticleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        route_request(self)

    def do_POST(self):
        route_request(self)

    def do_PUT(self):
        route_request(self)

    def do_DELETE(self):
        route_request(self)

    def log_message(self, format, *args):
        return


def run_server():

    init_db()

    HTTPServer.allow_reuse_address = True

    server = HTTPServer((HOST, PORT), ArticleHTTPRequestHandler)

    print(f"Content service running on {HOST}:{PORT}")

    server.serve_forever()


if __name__ == "__main__":
    run_server()