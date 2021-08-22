"""Calculate average ride duration, from file with JSON object per line"""

import json
from datetime import datetime, timedelta


def parse_time(ts):
    """
    >>> parse_time('2018-10-31T07:10:55.000Z')
    datetime.datetime(2018, 10, 31, 7, 10, 55)
    """
    # [:-1] trims Z suffix
    return datetime.fromisoformat(ts[:-1])


def fix_pair(pair):
    key, value = pair
    if key not in ('pickup', 'dropoff'):
        return pair
    return key, parse_time(value)


def pairs_hook(pairs):
    return dict(fix_pair(pair) for pair in pairs)


durations = []
with open('taxi.jl') as fp:
    for line in fp:
        obj = json.loads(line, object_pairs_hook=pairs_hook)
        duration = obj['dropoff'] - obj['pickup']
        durations.append(duration)

avg_duration = sum(durations, timedelta()) / len(durations)
print(f'average ride duration: {avg_duration}')
