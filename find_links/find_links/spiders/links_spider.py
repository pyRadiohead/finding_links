import scrapy
f = open('website_list.txt', 'r')
website_list = [i.strip() for i in f]



class LinksFinder(scrapy.Spider):
    name = "find_links"
    start_urls = ['http://15krace.co.nz/',]
    current_website =''
    # custom_settings = {
    #     # specifies exported fields and order
    #     'FEED_EXPORT_FIELDS': [
    #        'website',
    #         'link1',
    #         'link2',
    #         'link3',
    #     ],
    # }
    def parse(self, response):
        self.current_website = response.url
        links = response.xpath('*//a/@href').extract()
        for link in links:
            if link.startswith(response.url) and len(link) > len(response.url):
                print('Link start with', link)
                yield response.follow(link,self.parse_internal_links)
            pass

    def parse_internal_links(self, response):
            links = response.xpath('*//a/@href').extract()
            if links is not None:
                for link in links:
                    if link != self.current_website:
                        print(link)
            else:
                pass


