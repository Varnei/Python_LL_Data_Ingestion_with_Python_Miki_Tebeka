"""Convert unstructured ride text to JSON"""
import bz2
import logging
import re
from datetime import datetime


def parse_line(line):
    # Example:
    # Ride of 1 passenger started at 2018-10-31T07:10:55 and paid $20.54
    match = re.search(
        r'(\d+) pass.*started at ([^ ]+).*paid \$(\d+\.\d+)',
        line)
    if not match:
        return None

    return {
        'count': int(match.group(1)),
        'start': datetime.fromisoformat(match.group(2)),
        'amount': float(match.group(3)),
    }


def iter_rides(file_name):
    with bz2.open(file_name, 'rt') as fp:
        for lnum, line in enumerate(fp, 1):
            record = parse_line(line)
            if not record:
                logging.warning('%s: cannot parse line', lnum)
                continue
            yield record


# Example
if __name__ == '__main__':
    from pprint import pprint

    for n, ride in enumerate(iter_rides('taxi.log.bz2')):
        if n > 5:
            break
        pprint(ride)
