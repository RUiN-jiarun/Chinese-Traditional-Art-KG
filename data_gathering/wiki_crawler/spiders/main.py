import scrapy
from scrapy.loader import ItemLoader
import pymongo
# import sys
# sys.path.append('../')
from wiki_crawler.items import WikiCrawlerItem
import zhconv

class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['zh.wikipedia.org']
    db = pymongo.MongoClient("mongodb://127.0.0.1:27017/")["db_wikikg"]
    # 爬取的url范围由上一个数据库db_urls决定
    start_urls = []
    names = []
    db_urls = db['db_urls']
    for x in db_urls.find():
        id_strip = x['_id'][:x['_id'].find(' (')] if x['_id'].find(' (') != -1 else x['_id']
        names.append(id_strip)
        start_urls.append(x['url'])

    print(start_urls)
    print(names)

    # 创建一个关于三元组的数据库
    db_triples = db['db_triples']
    # 结构：_id sub_name attr obj_name
    # 可能要将obj_name与names[]进行范围比对，确定我们查找的范围

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        # TODO: 分析页面规则
        pass