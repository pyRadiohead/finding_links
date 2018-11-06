import scrapy
f = open('website_list.txt', 'r')
website_list = [i.strip() for i in f]



class QuotesSpider(scrapy.Spider):
    name = "find_links"
    start_urls = website_list
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)