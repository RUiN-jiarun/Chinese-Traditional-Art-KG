import scrapy


class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['g2.ltfc.net']
    start_urls = ['http://g2.ltfc.net/']

    def parse(self, response):
        pass
