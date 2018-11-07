import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

f = open('website_list.txt', 'r')
# website_list = ['http://'+i.strip() for i in f]
l = open('link_list.txt', 'r')
link_list = [i.strip() for i in l]

no_need_links =['twitter','facebook','pinterest','mythemeshop','google','respond','mailto']
key_words =['casino', 'gambling', 'poker','bet','lucky', 'gambl']

class LinksFinder(scrapy.Spider):
    name = "find_links"
    website_urls = ['http://tuplajaat.net','http://tt-kreis-pforzheim.de','http://otahunariding.co.nz','http://tarpilenskennel.com.preview.internetvikings.com']
    current_website =''

    def start_requests(self):
        for website in self.website_urls:
            yield scrapy.Request(website,self.parse)
        
    def link_filter(self,link_for_check):
        if not link_for_check.startswith(self.current_website):
            for i in link_list:
                if i in link_for_check:
                        return True
            return False
        return False

    def parse(self, response):
        self.current_website = response.url
        links = response.xpath('*//a/@href').extract()
        for link in links:
            if link.startswith(response.url) and len(link) > len(response.url):
                yield response.follow(link,self.parse_internal_links)
            pass

    def parse_internal_links(self, response):
        links = response.xpath('*//a/@href').extract()
        if links is not None:
            links = filter(self.link_filter, links)
            for link in links:
                print(response.url,link)
        else:
             pass



