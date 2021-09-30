# 暑假学习记录

## 7.14

*计划从知识图谱的构建角度开始，找一些与知识图谱相关的内容，同时根据老师的指导进行数据的收集*

基本需要这几个重要步骤：

* 数据获取
  * 用scrapy框架
  * 对于词条**抽取哪些信息**需要再商量或者研究
  * 采用并行爬虫可以加速
* 数据库的建立
* 三元组的表达形式：（实体A，实体B，关系）
  * RDF检索语言，基于RDF的存储的开源方式
  * 存储数据库：关系型数据库？图数据库？文档数据库？
  * 图数据库的话，用哪种数据库？——
  * 备选项：Word2Vec对三元组的表示学习，可以建立稠密向量
* 构建工具
  * Java的Apache Jena
  * python的spacy库
* 知识融合



另外，确定了需要爬取的网页：（共143个页面）

[分类:明朝画家 - 维基百科，自由的百科全书 (wikipedia.org)](https://zh.wikipedia.org/wiki/Category:明朝畫家)

## 7.16

**学习scrapy框架**

环境与框架配置：

```sh
$ pip install wheel
$ pip install scrapy
$ scrapy startproject wiki_crawler
$ scrapy genspider main zh.wikipedia.org
```

下一步：对要爬取的页面要进行分析

```python
l.add_xpath('titles','//h3/ul/li/a/text()')
l.add_xpath('urls','//h3/ul/li/a/@href')
```

执行

```sh
$ scrapy crawl main --nolog
```

**甘霖娘！出错啦！这个xpath路径不对！！**

还是老老实实从xpath看起。。。

## 7.20

**Xpath**用于HTML或XML中系欸DNA的选择

* 多级定位：从根节点开始选择定位，以`/`开头，返回所有匹配的子节点选择器列表
* 跳级定位：不从根节点开始而是全局匹配，以`//`开头，返回所有能够匹配到的结果
* 属性匹配：使用id、class、title、href等来辅助查询，结合多级定位或跳级定位，如`//body/div[@id="header"]`
* 提取内容：在定位后加`/text()`，再调用get()或getall()方法获得
* 提取属性：如在定位后加`/@class`获得类信息

## 8.4

我是废物。。旷了好几天。。。

今天整了一点，把路径找好了

* 运行路径在`data_gathering/wiki`

* xpath：

  ```python
  print(response.xpath('//body/div[@id="content"]/div[@id="bodyContent"]/div[@id="mw-content-text"] \
                                  /div[@class="mw-category-generated"]/div[@id="mw-pages"] \
                                  /div[@class="mw-content-ltr"]/div[@class="mw-category"]/div[@class="mw-category-group"]/ul/li/a/text()'))
  ```

## 8.11

尝试将工作环境部署在Ubuntu 20.04.2.0系统上，但是网络问题比较严重，没有办法爬取wiki百科。所以还是在Windows操作系统里部署工程。


## 8.12

结合一个爬取Baidu百科三元组的例子，配置好了**Neo4j**以及**MongoDB**。下一步先看这个三元组在数据库里怎么构建的。

发现了这个工程的爬取原理是这样的：

* 在页面中寻找href链接中包含页面关键信息的类似链接，作为下一个爬取的页面
* 在百科总表中获取三元组

总结了一下，这个例子适用于“自由爬取”，不适合我们这种有限定范围的爬取。因此**首先需要确定一个爬取的页面list**，作为进一步爬取的范围。

然后是三元组，wiki百科中有些地方不包含这样的例表。如果包含的话，我们能也要先确认一下这个范围……

或者，先全部保存这个三元组关系，后面我们总能看到一些联系。计划明天先把爬取页面的范围确定下来。

## 8.13

**进度：获取了所有需要爬取的urls页面**。共240个子页面需要进行分析与爬取。

```python
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
            url = urls[i]
            try:
                self.db_urls.insert_one(
                    {
                        '_id': name,
                        'url': 'https://zh.wikipedia.org' + url
                    }
                )
            except pymongo.errors.DuplicateKeyError:
                print('Key Conflict: ' + name)
```



<img src="https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210813141318623.png" alt="image-20210813141318623" style="zoom:50%;" />

下面需要对这些具体的页面进行分析，提取网页内容。

## 8.15

**进度：准备创建三元组的DB，确定数据结构，分析目标页面**

|      | _id                 | sub_name | attr     | obj_name |
| ---- | ------------------- | -------- | -------- | -------- |
| Ex:  | 秦旭_碧山吟社\_陆勉 | 秦旭     | 碧山吟社 | 陆勉     |

![image-20210815101849064](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210815101849064.png)

看看这个例子的页面结构：

![image-20210815102214781](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210815102214781.png)

## 8.20

分析结构，得出两种xpath

```python
l1 = response.xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr/td/table/tbody/tr[1]/th/div[2]/text()').getall()
l2 = response.xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table/tbody/tr/td/table/tbody/tr[1]/th/div[2]/a/text()').getall()
```

下面可能要在该属性的范围里做一些筛选

用一个interset看看有没有交集

快了，这样三元组的架构基本就有了

## 8.25

考虑用正则表达式分析一下html内容

*另外需要考虑：多个属性怎么查找？*

比如：

/html/body/div[3]/div[3]/div[5]/div[1]/table[1]

```
/html/body/div[3]/div[3]/div[5]/div[1]/table[2]
/html/body/div[3]/div[3]/div[5]/div[1]/table[3]
```

下一步：从正则表达式中提取文字信息

```
<(\S*?)[^>]*>.*?|<.*? />
```

用上面这个来删除标签信息
