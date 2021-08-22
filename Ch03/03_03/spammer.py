import bz2
import csv
import json
from pathlib import Path
from random import random
from time import sleep

from pynats import NATSClient

here = Path(__file__).absolute().parent
csv_file = here / 'taxi.csv.bz2'


conversions = [
    ('VendorID', 'vendor', int),
    ('tpep_pickup_datetime', 'pickup', str),
    ('tpep_dropoff_datetime', 'dropoff', str),
    ('passenger_count', 'passengers', int),
    ('trip_distance', 'distance', float),
    ('tip_amount', 'tip', float),
    ('total_amount', 'amount', float),
]


def iter_rides():
    with bz2.open(csv_file, 'rt') as fp:
        for row in csv.DictReader(fp):
            record = {}
            for src, dest, conv in conversions:
                record[dest] = conv(row[src])
            yield record


client = NATSClient('nats://localhost:4222')
client.connect()
for ride in iter_rides():
    sleep(random())
    payload = json.dumps(ride)
    client.publish('rides', payload=payload)
