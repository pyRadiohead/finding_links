import scrapy
import datetime
from ..items import TraderPrice


class TraderPriceSpider(scrapy.Spider):
    name = 'trader_prices'
    download_delay = 5.0
    start_urls = [
        'https://agrotender.com.ua/traders.html',
    ]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            "company",
            "currency",
            "date",
            "page_url",
            "scraping_date",
            "price_uah",
            "price_usd",
            "product",
            "delivery",
            "region",
            "warehouse",
            "date_alt",
        ],
    }

    def parse(self, response):
        links = response.css('div.trader-tit a::attr(href)').extract()
        # url = 'https://agrotender.com.ua/kompanii/comp-1098-pricetbl.html'
        # url = 'https://agrotender.com.ua/kompanii/comp-1667-pricetbl.html'
        # yield response.follow(url, self.parse_trader_prices)
        for link in links:
            yield response.follow(link, self.parse_trader_prices)

    def parse_trader_prices(self, response):
        _today = datetime.datetime.now().strftime('%d.%m.%Y')
        _url = response.url
        _company = response.xpath(
                '/html/body/div[1]/div/div[2]/div[1]/div[2]/span/text()'
            ).extract_first()
        _date = response.css('#dtviewtxt h1::text').extract_first().split()[-1]
        _date_alt = datetime.datetime.strptime(_date, '%d.%m.%Y').strftime('%Y%m%d')
        _currency = 'usd' if _url.endswith('-pricetbl-2.html') else 'uah'

        tables = response.css('table.cprtbl')
        for table in tables:
            t_data = []
            rotate_table = False
            for row in table.css('tr'):
                ths = row.css('th')

                tds = row.css('td')
                if ths:
                    cells = []
                    for x in ths:
                        chunk = x.css('::text').extract()
                        if len(chunk) == 1:
                            cells.append(chunk[0])
                        else:
                            rotate_table = True
                            cells.append(tuple(chunk))
                    t_data.append(cells)
                elif tds:
                    cells = []
                    for x in tds:
                        _div = x.css('div::text')
                        _span = x.css('span::text')
                        if _div:
                            cells.append((_div.extract_first(), _span.extract_first()))
                        elif _span:
                            cells.append(_span.extract_first())
                        else:
                            cells.append(x.css('::text').extract_first())
                    t_data.append(cells)
            # print(t_data)

            for j, row in enumerate(t_data):
                for i, x in enumerate(row):
                    if i > 0 and j > 0:
                        if x:
                            _price_uah = x if _currency == 'uah' else ''
                            _price_usd = x if _currency == 'usd' else ''

                            if rotate_table:
                                item = TraderPrice(
                                    page_url=_url,
                                    company=_company,
                                    date=_date,
                                    scraping_date=_today,
                                    region=t_data[0][i][0],
                                    warehouse=t_data[0][i][1],
                                    delivery='cpt' if t_data[0][i][1] else 'fca',
                                    price_uah=_price_uah,
                                    price_usd=_price_usd,
                                    product=row[0],
                                    currency=_currency,
                                    date_alt=_date_alt,
                                )
                            else:
                                item = TraderPrice(
                                    page_url=_url,
                                    company=_company,
                                    date=_date,
                                    scraping_date=_today,
                                    region=row[0][0],
                                    warehouse=row[0][1],
                                    delivery='cpt' if row[0][1] else 'fca',
                                    price_uah=_price_uah,
                                    price_usd=_price_usd,
                                    product=t_data[0][i],
                                    currency=_currency,
                                    date_alt=_date_alt,
                                )
                            yield item

        if _currency == 'uah':
            usd_url = response.xpath('/html/body/div[1]/div/div[2]/div[3]/div[3]/ul/li[2]/a/@href').extract_first()
            if usd_url:
                yield response.follow(usd_url, self.parse_trader_prices)
