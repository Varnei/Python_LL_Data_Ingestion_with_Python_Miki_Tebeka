import atexit
import bz2
import csv
from pathlib import Path
from subprocess import PIPE, Popen
from time import monotonic, sleep
from datetime import datetime

from elasticsearch import Elasticsearch, ElasticsearchException

here = Path(__file__).absolute().parent
csv_file = here / 'food.csv.bz2'

port = 9200

cmd = [
    'docker', 'run',
    '--rm', '-p', f'{port}:{port}',
    '-e', 'discovery.type=single-node',
    '--name', 'elastic-demo',
    'elasticsearch:7.3.0',
]

proc = Popen(cmd, stdout=PIPE)
atexit.register(proc.kill)

up = False
start = monotonic()
while monotonic() - start < 60:
    conn = Elasticsearch()
    try:
        if conn.ping():
            up = True
            break
    except ElasticsearchException:
        sleep(0.1)

if not up:
    raise SystemExit('error: elasticsearch not up')


def parse_date(text):
    return datetime.strptime(text, '%m/%d/%Y')


def parse_zip(text):
    return int(float(text))


schema = [
    ('Inspection ID', 'id', str),
    ('DBA Name', 'name', str),
    ('Address', 'address', str),
    ('City', 'city', str),
    ('Zip', 'zip', parse_zip),
    ('Inspection Date', 'date', parse_date),
    ('Latitude', 'lat', float),
    ('Longitude', 'lng', float),
    ('Violations', 'violations', str),
]


def convert(row):
    obj = {}
    for src, dest, conv in schema:
        obj[dest] = conv(row[src])
    return obj


print('populating database...')
es = Elasticsearch()
count = 0
with bz2.open(csv_file, 'rt') as fp:
    for row in csv.DictReader(fp):
        try:
            obj = convert(row)
        except ValueError:
            pass
        es.index(index='food', body=obj)
        count += 1

print(f'loaded {count} documents')
print(f'elasticsearch ready on port {port}, hit CTRL-C to quit')
try:
    proc.wait()
except KeyboardInterrupt:
    pass
print('\nkthxbai ☺')
