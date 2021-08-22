from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from http import HTTPStatus
import json

trips_db = None


def load_trips():
    here = Path(__file__).absolute().parent
    reply_file = here / 'trips.json'
    with reply_file.open('rb') as fp:
        return json.load(fp)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path != '/trips':
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        auth = self.headers.get('X-TRIPS-TOKEN')
        if auth != 'l3tm3in':
            self.send_error(HTTPStatus.UNAUTHORIZED)
            return

        args = parse_qs(url.query)
        if 'start' not in args or 'end' not in args:
            self.send_error(HTTPStatus.BAD_REQUEST)
            return

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        start = args['start'][0]
        end = args['end'][0]
        reply = {
            'ok': True,
            'trips': [
                trip for trip in trips_db
                if trip['pickup'] >= start and trip['pickup'] < end
            ],
        }
        data = json.dumps(reply)
        self.wfile.write(data.encode('utf-8'))


if __name__ == '__main__':
    host, port = 'localhost', 8989
    server = ThreadingHTTPServer((host, port), Handler)
    trips_db = load_trips()
    print(f'server ready on {host}:{port}')
    server.serve_forever()
