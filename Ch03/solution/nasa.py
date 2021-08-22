"""Add geo information to IPs"""
import gzip
from ipaddress import IPv4Address
from functools import lru_cache

import requests

headers = {
    'X-GEOIP-TOKEN': 'l3tm3in',
}
base_url = 'http://localhost:8988/geoip'


@lru_cache(1024)
def country_of(ip):
    params = {
        'ip': ip,
    }
    resp = requests.get(base_url, params=params, headers=headers)
    if not resp.ok:
        return ''
    reply = resp.json()
    if not reply['found']:
        return ''

    return reply['name']


def is_ip(host):
    try:
        IPv4Address(host)
        return True
    except ValueError:
        return False


def iter_ips(file_name, limit):
    count = 0
    for line in gzip.open(file_name, 'rt'):
        if count >= limit:
            break
        i = line.find('-')
        if i == -1:  # not found
            continue
        host = line[:i].strip()
        if not is_ip(host):
            continue
        yield host
        count += 1


if __name__ == '__main__':
    from collections import Counter

    countries = Counter()
    ips = iter_ips('NASA_access_log_Aug95.gz', 1000)
    for ip in ips:
        country = country_of(ip)
        if not country:
            country = '<Unknown>'
        countries[country] += 1

    total = sum(countries.values())
    for country, count in countries.most_common(10):
        percent = count / total * 100
        print(f'{country:<20} {percent:.2f}%')
