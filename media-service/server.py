from http.server import HTTPServer, BaseHTTPRequestHandler
from router import route_request

HOST = "0.0.0.0"
PORT = 8004


class MediaHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        route_request(self)

    def do_GET(self):
        route_request(self)

    def do_DELETE(self):
        route_request(self)

    def log_message(self, format, *args):
        return


def run_server():

    HTTPServer.allow_reuse_address = True

    server = HTTPServer((HOST, PORT), MediaHTTPRequestHandler)

    print(f"Media service running on {HOST}:{PORT}")

    server.serve_forever()


if __name__ == "__main__":
    run_server()
