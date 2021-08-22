"""Parsing HTML with BeautifulSoup"""
from datetime import datetime

from bs4 import BeautifulSoup


def parse_html(html):
    """Parse FX html, return date and dict of {symbol -> rate}"""
    soup = BeautifulSoup(html, 'html.parser')

    # <h4>Date: <i class="date">2019-11-11</i></h4>
    i = soup('i', {'class': 'date'})
    if not i:
        raise ValueError('cannot find date')

    date = datetime.strptime(i[0].text, '%Y-%m-%d')

    rates = {}
    for tr in soup('tr'):
        # <tr>
        # <td><i class="fas fa-pound-sign" data-toggle="tooltip"
        #   title="GBP"></i></td>
        # <td>0.83</td>
        # </tr>
        symbol_td, rate_td = tr('td')
        symbol = symbol_td('i')[0]['title']
        rate = float(rate_td.text)
        rates[symbol] = rate

    return date, rates


if __name__ == '__main__':
    with open('fx.html') as fp:
        html = fp.read()

    date, rates = parse_html(html)
    print(f'date: {date}')
    for symbol, rate in rates.items():
        print(f'USD/{symbol} = {rate:f}')
