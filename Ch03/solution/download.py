from urllib.request import urlopen
from os import path
from functools import partial
from concurrent.futures import ThreadPoolExecutor

mb = 1 << 20


def download(url):
    outfile = path.basename(url)
    with open(outfile, 'wb') as out, urlopen(url) as resp:
        for chunk in iter(partial(resp.read, mb), b''):
            out.write(chunk)


urls = [
    (
        'https://geolite.maxmind.com/download/geoip/database/'
        'GeoLite2-Country-CSV.zip'
    ),
    'ftp://ita.ee.lbl.gov/traces/NASA_access_log_Aug95.gz',
]

with ThreadPoolExecutor() as pool:
    futs = [pool.submit(download, url) for url in urls]
    for fut in futs:
        fut.result()
