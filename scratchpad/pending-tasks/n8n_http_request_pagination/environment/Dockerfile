FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g n8n && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="n8n environment with a mock Python API server for pagination."

RUN cat > /home/user/server.py <<'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/api/users':
            query = parse_qs(parsed_url.query)
            page = int(query.get('page', ['1'])[0])
            
            data = []
            next_url = None
            
            if page == 1:
                data = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
                next_url = "http://localhost:3000/api/users?page=2"
            elif page == 2:
                data = [{"id": 3, "name": "Charlie"}, {"id": 4, "name": "Dave"}]
                next_url = "http://localhost:3000/api/users?page=3"
            elif page == 3:
                data = [{"id": 5, "name": "Eve"}]
                next_url = None
                
            response = {
                "data": data,
                "next_url": next_url
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

httpd = HTTPServer(('localhost', 3000), SimpleHTTPRequestHandler)
httpd.serve_forever()
EOF

# Container contents:
#   - n8n installed globally via npm.
#   - Python 3 installed.
#   - /home/user/server.py: A mock API server that returns paginated users on port 3000.

CMD ["/bin/bash", "-c", "python3 /home/user/server.py & trap : TERM INT; sleep infinity & wait"]