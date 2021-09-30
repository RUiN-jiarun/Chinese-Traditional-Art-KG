import scrapy
from scrapy.loader import ItemLoader
import pymongo
from wiki_crawler.items import WikiCrawlerItem
import zhconv
import re

def inter(a,b):
    return list(set(a)&set(b))

class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['zh.wikipedia.org']
    db = pymongo.MongoClient("mongodb://127.0.0.1:27017/")["db_wikikg"]
    # 爬取的url范围由上一个数据库db_urls决定
    start_urls = []
    names = []
    db_urls = db['db_urls']
    for x in db_urls.find():
        # id_strip = x['_id'][:x['_id'].find(' (')] if x['_id'].find(' (') != -1 else x['_id']
        # names.append(id_strip)
        names.append(x['_id'])
        start_urls.append(x['url'])

    # print(start_urls)
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
        sub_name = response.xpath('/html/body/div[3]/h1/text()').getall()[0]
        l1 = response.xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr/td/table/tbody/tr[1]/th/div[2]').getall()
        # 可能有多个属性，分别查找
        attr_len = len(l1)


        # l1[0] = l1[0].replace("（", "")
        # l1[1] = l1[1].replace("）", "")
        # l1[0] += l1[1]
        # if l2[0][-1] == "年":
        #     l2.clear()
        sub_name = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", sub_name)
        sub_name = sub_name.replace(' ', '')
        sub_name = zhconv.convert(sub_name, 'zh-hans')
        print(sub_name)
        print(l1)
        print(attr_len)
        for i in range(0, attr_len):
            allInfo = response.xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[@class="navbox"]['+str(i)+']//a/text()').getall()
            for i in range(0,len(allInfo)):
                allInfo[i] = allInfo[i].replace('\u3000', '')
                allInfo[i] = zhconv.convert(allInfo[i], 'zh-hans')
            # print(allInfo)
            interset = inter(allInfo, self.names)
            print(interset)
