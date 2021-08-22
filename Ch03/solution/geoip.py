import csv
import json
from collections import namedtuple
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import TextIOWrapper
from ipaddress import IPv4Address, IPv4Network
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from zipfile import ZipFile

Country = namedtuple('Country', 'name iso')

blocks_csv = f'GeoLite2-Country-Blocks-IPv4.csv'
countries_csv = f'GeoLite2-Country-Locations-en.csv'
blocks_db = None


def load_countries(fp):
    countries = {}
    for record in csv.DictReader(fp):
        name, iso = record['country_name'], record['country_iso_code']
        countries[record['geoname_id']] = Country(name, iso)
    return countries


def find_zinfo(zf: ZipFile, name):
    for zinfo in zf.filelist:
        if Path(zinfo.filename).name == name:
            return zinfo


def load_db():
    here = Path(__file__).absolute().parent
    csv_file = here / 'GeoLite2-Country-CSV.zip'
    with ZipFile(csv_file) as zf:
        zinfo = find_zinfo(zf, countries_csv)
        assert zinfo, f'cannot find {countries_csv}'
        with zf.open(zinfo) as fp:
            countries = load_countries(TextIOWrapper(fp))

        zinfo = find_zinfo(zf, blocks_csv)
        assert zinfo, f'cannot find {blocks_csv}'
        blocks = []
        with zf.open(zinfo) as fp:
            for record in csv.DictReader(TextIOWrapper(fp)):
                geo_id = record['geoname_id']
                if not geo_id:
                    continue
                network = IPv4Network(record['network'])
                country = countries[record['geoname_id']]
                blocks.append((network, country))
        return blocks


def ip2country(ip):
    # TODO: Speedup with sort & binary search?
    for block, country in blocks_db:
        if ip in block:
            return country


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path != '/geoip':
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        auth = self.headers.get('X-GEOIP-TOKEN')
        if auth != 'l3tm3in':
            self.send_error(HTTPStatus.UNAUTHORIZED)
            return

        ip = parse_qs(url.query).get('ip')
        if ip:
            try:
                ip = IPv4Address(ip[0])
            except ValueError:
                ip = None

        if ip is None:
            self.send_error(HTTPStatus.BAD_REQUEST)
            return

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        country = ip2country(ip)
        if not country:
            reply = {'found': False}
        else:
            reply = {
                'found': True,
                'name': country.name,
                'iso': country.iso,
            }

        data = json.dumps(reply)
        self.wfile.write(data.encode('utf-8'))


if __name__ == '__main__':
    host, port = 'localhost', 8988
    server = ThreadingHTTPServer((host, port), Handler)
    blocks_db = load_db()
    print(f'server ready on {host}:{port}')
    server.serve_forever()
