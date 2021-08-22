from datetime import datetime, timedelta
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
from pathlib import Path
from urllib.parse import urlparse
import re

here = Path(__file__).absolute().parent
start_date = datetime(2019, 11, 1)
num_days = 8
start_prices = [
    ('GBP', 0.83),
    ('EUR', 0.89),
    ('JPY', 105.3),
    ('BTC', 0.01),
    ('ILS', 3.48),
]
time_fmt = '%Y-%m-%d'


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == '/':
            html = self.index()
        else:
            try:
                # /2019-11-02
                date = datetime.strptime(url.path[1:], time_fmt)
            except ValueError:
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            diff = (date - start_date).days / 100
            args = {
                symbol: price + diff for symbol, price in start_prices
            }
            args['date'] = date.strftime(time_fmt)

            template = self.load_html('day.html')

            def replace(match):
                val = args[match.group(1)]
                if isinstance(val, float):
                    val = f'{val:.2f}'
                return val
            html = re.sub('{{([a-zA-Z]+)}}', replace, template)

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def index(self):
        io = StringIO()
        print('<ul class="list-group">', file=io)
        for i in range(num_days):
            day = start_date + timedelta(days=i)
            day = day.strftime(time_fmt)
            li = (
                '\t<li class="list-group-item">'
                f'<a href="/{day}">{day}</a></li>'
            )
            print(li, file=io)
        print('</ul>', file=io)

        dates = io.getvalue()
        return self.load_html('index.html').format(dates=dates)

    def load_html(self, name):
        path = here / name
        with path.open() as fp:
            return fp.read()


if __name__ == '__main__':
    host, port = 'localhost', 8987
    server = ThreadingHTTPServer((host, port), Handler)
    print(f'server ready on {host}:{port}')
    server.serve_forever()
