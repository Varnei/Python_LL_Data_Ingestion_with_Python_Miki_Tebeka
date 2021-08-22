import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

here = Path(__file__).absolute().parent


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == '/':
            response = self.load_html('fx.html')
            content_type = 'text/html'
        else:
            response = json.dumps({
                'ratios': [
                    {'symbol': 'GBP', 'ratio': 0.83},
                    {'symbol': 'EUR', 'ratio': 0.89},
                    {'symbol': 'JPY', 'ratio': 105.3},
                    {'symbol': 'BTC', 'ratio': 0.01},
                    {'symbol': 'ILS', 'ratio': 3.48},
                ],
                'date': '2019-11-11',
            })
            content_type = 'application/json'

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def load_html(self, name):
        path = here / name
        with path.open() as fp:
            return fp.read()


if __name__ == '__main__':
    host, port = 'localhost', 8985
    server = ThreadingHTTPServer((host, port), Handler)
    print(f'server ready on {host}:{port}')
    server.serve_forever()
