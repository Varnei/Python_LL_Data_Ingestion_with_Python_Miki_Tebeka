"""Load rides data from XML"""

import bz2
import xml.etree.ElementTree as xml

import pandas as pd

# Data conversions
conversion = [
    ('vendor', int),
    ('people', int),
    ('tip', float),
    ('price', float),
    ('pickup', pd.to_datetime),
    ('dropoff', pd.to_datetime),
    ('distance', float),
]


def iter_rides(file_name):
    with bz2.open(file_name, 'rt') as fp:
        tree = xml.parse(fp)

    rides = tree.getroot()
    for elem in rides:
        record = {}
        for tag, func in conversion:
            text = elem.find(tag).text
            record[tag] = func(text)
        yield record


def load_xml(file_name):
    records = iter_rides(file_name)
    return pd.DataFrame.from_records(records)


# Example
if __name__ == '__main__':
    df = load_xml('taxi.xml.bz2')
    print(df.dtypes)
    print(df.head())
