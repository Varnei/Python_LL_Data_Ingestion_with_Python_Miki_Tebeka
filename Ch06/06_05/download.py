"""Download Chicago food inspection data"""
from urllib.request import urlopen
import bz2

url = (
    'https://data.cityofchicago.org/api/views/4ijn-s7e5/'
    'rows.csv?accessType=DOWNLOAD'
)

with bz2.open('food.csv.bz2', 'w') as out, urlopen(url) as resp:
    for i, line in enumerate(resp):
        if i > 3001:
            break
        out.write(line)
