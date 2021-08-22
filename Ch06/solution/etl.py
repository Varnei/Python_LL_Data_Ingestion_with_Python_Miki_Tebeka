"""ETL from CSV to SQlite database"""
import csv
import sqlite3
from datetime import datetime
import logging


def parse_day(text):
    return datetime.strptime(text, '%Y%m%d')


def parse_temp(text):
    celsius = float(text) * 10
    return (celsius * 9/5) + 32


converts = [
    ('DATE', 'day', parse_day),
    ('TMIN', 'min_temp', parse_temp),
    ('TMAX', 'max_temp', parse_temp),
    ('SNOW', 'snow', int),
]


def row2db(row):
    obj = {}
    for src, dest, conv in converts:
        try:
            obj[dest] = conv(row[src])
        except ValueError:
            return None
    return obj


def iter_records(csv_file):
    with open(csv_file) as fp:
        for lnum, row in enumerate(csv.DictReader(fp), 2):
            obj = row2db(row)
            if not obj:
                logging.warning('%s:%d skipping bad row', csv_file, lnum)
                continue
            yield obj


schema_sql = '''
CREATE TABLE IF NOT EXISTS weather (
    day DATE,	    -- day of measurements
    min_temp FLOAT, -- min temperature in Fahrenheit
    max_temp FLOAT, -- max temperature in Fahrenheit
    snow INTEGETR   -- snow in inches
);

CREATE INDEX IF NOT EXISTS weather_day ON weather(day);
'''


insert_sql = '''
INSERT INTO weather (
    day,
    min_temp,
    max_temp,
    snow
) VALUES (
    :day,
    :min_temp,
    :max_temp,
    :snow
)
'''


def etl(csv_file, db_file):
    with sqlite3.connect(db_file) as db:
        cur = db.cursor()
        cur.executescript(schema_sql)
        cur.executemany(insert_sql, iter_records(csv_file))
        return cur.rowcount


if __name__ == '__main__':
    count = etl('weather.csv', 'weather.db')
    print(f'inserted {count} records')
