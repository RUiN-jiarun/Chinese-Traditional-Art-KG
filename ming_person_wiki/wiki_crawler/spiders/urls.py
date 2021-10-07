import scrapy
from scrapy.loader import ItemLoader
import pymongo
import sys
import importlib
importlib.reload(sys)

# sys.setdefaultencoding('utf8')
# sys.path.append('../')
from wiki_crawler.items import WikiCrawlerItem
import zhconv
import re


class UrlsSpider(scrapy.Spider):
    name = 'urls'
    allowed_domains = ['zh.wikipedia.org']
    start_urls = ['https://zh.wikipedia.org/wiki/Category:明朝畫家',
                'https://zh.wikipedia.org/wiki/Category:明朝書法家']
    db = pymongo.MongoClient("mongodb://127.0.0.1:27017/")["db_wikikg"]
    # 姓名对应的url
    db_urls = db['db_urls']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        names = response.xpath('//body/div[@id="content"]/div[@id="bodyContent"]/div[@id="mw-content-text"] \
                                /div[@class="mw-category-generated"]/div[@id="mw-pages"] \
                                /div[@class="mw-content-ltr"]/div[@class="mw-category"]/div[@class="mw-category-group"]/ul/li/a/text()').getall()
        urls = response.xpath('//body/div[@id="content"]/div[@id="bodyContent"]/div[@id="mw-content-text"] \
                                /div[@class="mw-category-generated"]/div[@id="mw-pages"] \
                                /div[@class="mw-content-ltr"]/div[@class="mw-category"]/div[@class="mw-category-group"]/ul/li/a/@href').getall()
        for i in range(len(names)):
            name = zhconv.convert(names[i], 'zh-hans')
            name = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", name)
            name = name.replace(' ', '')
            url = urls[i]
            # print(name)
            try:
                self.db_urls.insert_one(
                    {
                        '_id': name,
                        'url': 'https://zh.wikipedia.org' + url
                    }
                )
            except pymongo.errors.DuplicateKeyError:
                print('Key Conflict: ' + name)



