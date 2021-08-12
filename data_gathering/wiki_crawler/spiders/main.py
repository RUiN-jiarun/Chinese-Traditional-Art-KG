import scrapy
from scrapy.loader import ItemLoader
# import sys
# sys.path.append('../')
from wiki_crawler.items import WikiCrawlerItem


class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['zh.wikipedia.org']
    start_urls = ['https://zh.wikipedia.org/wiki/Category:明朝畫家']

    def parse(self, response):
        # TODO: 定义规则
        # l = ItemLoader(item=WikiCrawlerItem, response=response)
        # l.add_xpath("title','//body/div[@id='content']")
        # l.add_xpath('urls','//h3/ul/li/a/@href')
        print(response.xpath('//body/div[@id="content"]/div[@id="bodyContent"]/div[@id="mw-content-text"] \
                                /div[@class="mw-category-generated"]/div[@id="mw-pages"] \
                                /div[@class="mw-content-ltr"]/div[@class="mw-category"]/div[@class="mw-category-group"]/ul/li/a/text()'))
        # print(response.xpath('//h3/ul/li/a/@href').extract())
        # return l.load_item()
        # print(response.text)