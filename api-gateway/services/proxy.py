import json
import http.client

# SERVICES = {
#     "auth": ("localhost", 8002),
#     "content": ("localhost", 8003),
#     "media": ("localhost", 8004)
# }

# With container
SERVICES = {
    "auth": ("auth-service", 8002),
    "content": ("content-service", 8003),
    "media": ("media-service", 8004),
}


def forward_request(service_name, method, path, headers=None, body=None):

    host, port = SERVICES[service_name]

    connection = http.client.HTTPConnection(host, port)

    connection.request(method=method, url=path, body=body, headers=headers or {})

    response = connection.getresponse()

    data = response.read()

    return {"status": response.status, "headers": response.getheaders(), "body": data}
