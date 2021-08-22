import scrapy
from urllib.parse import urlparse


class FXSpider(scrapy.Spider):
    name = 'fx'
    start_urls = [
        'http://localhost:8987'
    ]

    def parse(self, response):
        for a in response.css('li.list-group-item a::attr(href)'):
            yield response.follow(a.get(), callback=self.parse_date)

    def parse_date(self, response):
        path = urlparse(response.url).path
        # /2019-11-03
        data = {'day': path[1:]}
        for tr in response.css('tr'):
            name_td, price_td = tr.css('td')
            # <i ... title="GBP">
            symbol = name_td.css('i::attr(title)').get()
            # <td>0.84</td>
            ratio = float(price_td.css('::text').get())
            data[symbol] = ratio
        yield data
