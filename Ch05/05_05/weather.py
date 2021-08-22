"""Schemd validation example"""
from collections import namedtuple
from datetime import date, time

Record = namedtuple('Record', 'date snow tmax tmin pgtm')
_missing = object()  # unique missing value


def validate_temp(name, temp):
    # temp in Celsius/10
    assert temp > -900, f'{name} {temp} too low'
    assert temp < 600, f'{name} {temp} too high'


def validate_snow(name, val):
    assert val >= 0, f'negative {name} - {val}'


validators = [
    ('date', None),  # No need, datetime will validate
    ('snow', validate_snow),
    ('tmax', validate_temp),
    ('tmin', validate_temp),
    ('pgtm', None),  # No need, datetime will validate
]


def validate(record):
    for attr, validator in validators:
        value = getattr(record, attr, _missing)
        assert value is not _missing, f'missing {attr}'
        if validator:
            validator(attr, value)


# Example

data = [
    Record(date(2000, 1, 1), 0, 100,  11, time(13, 37)),
    Record(date(2000, 1, 2), 0, 156,  61, time(23, 13)),
    Record(date(2000, 1, 3), 0, 178, 106, time(3,  20)),
    Record(date(2000, 1, 4), 0, 156,  78, time(18, 19)),
    Record(date(2000, 1, 5), 0,  83,  17, time(8,  43)),
]

for record in data:
    validate(record)
