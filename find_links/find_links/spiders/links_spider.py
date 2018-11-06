import scrapy
f = open('website_list.txt', 'r')
website_list = [i.strip() for i in f]
no_need_links =['twitter','facebook','pinterest','mythemeshop','google','respond','mailto','#']



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
    def link_filter(self,link_for_check):
        for link in no_need_links:
            if link in link_for_check:
                print(link +' not in ' + link_for_check)
                return False
            return True

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
            links = filter(self.link_filter,links)
            if links is not None:
                for link in links:
                    for i in no_need_links:
                        if not link.startswith(self.current_website):
                            print(link)
            else:
                pass


