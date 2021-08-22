"""Convert CSV to JSON (one object per line)"""
import bz2
import csv
import json
from collections import namedtuple
from datetime import datetime

Column = namedtuple('Column', 'src dest convert')


def parse_timestamp(text):
    return datetime.strptime(text, '%Y-%m-%d %H:%M:%S')


columns = [
    Column('VendorID', 'vendor_id', int),
    Column('passenger_count', 'num_passengers', int),
    Column('tip_amount', 'tip', float),
    Column('total_amount', 'price', float),
    Column('tpep_dropoff_datetime', 'dropoff_time', parse_timestamp),
    Column('tpep_pickup_datetime', 'pickup_time', parse_timestamp),
    Column('trip_distance', 'distance', float),
]


def iter_records(file_name):
    with bz2.open(file_name, 'rt') as fp:
        reader = csv.DictReader(fp)
        for csv_record in reader:
            record = {}
            for col in columns:
                value = csv_record[col.src]
                record[col.dest] = col.convert(value)
            yield record


def encode_time(obj):
    if not isinstance(obj, datetime):
        return obj
    return obj.isoformat()


with open('taxi.jl', 'w') as out:
    for record in iter_records('taxi.csv.bz2'):
        data = json.dumps(record, default=encode_time)
        out.write(f'{data}\n')
