# Chinese-Traditional-Art-KG

For graduation

## 暑假：预学习

[暑假学习记录](./note/2021Summer.md)

## 阶段1学习

在暑假学习记录的基础上先测试一下知识图谱的构建

需要启动neo4j

```bash
$ neo4j console
```

然后浏览器输入`http://localhost:7474/browser/`

经过测试后，有了一个例子的输出：

![image-20211003155620654](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20211003155620654.png)

好了现在是有一个结果了

<img src="https://ruin-typora.oss-cn-beijing.aliyuncs.com/graph.png" alt="graph" style="zoom:50%;" />

## 预备

>那个图谱中的对象的话呢，是这样，就因为这个里面一方面是那个作者，就这张图画的谁画的。还有就是这张画的那个就是收藏者，因为有的时候那个藏家也很重要，它这个里面有一个历史的关系在里面。当然那个图画本身也是建立这个联系的话呢，里面还有一个关键，就是我们也需要通过这个里面的印章来获取，因为印章是非常重要的一个环节。
>
>所以的话，我们其实就是要通过这个图谱来梳理各个对象之间的一种关系。因此这个图谱可能会有点小复杂，从我们可视化的角度来看的话呢，我们会做几种不同的图谱，通过图谱之间相互关联关系来阐明某一张画他的艺术价值，或者他的真伪，或者其中还有些什么故事。

预先在网上搜查到一些可能比较全面的数据集：

**关于古画**：[古代书画索引 - 中华珍宝馆 (ltfc.net)](http://g2.ltfc.net/suhaindex)

在这个数据集中，一个比较完整的条目大概长这样：

![image-20211007095059818](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20211007095059818.png)

* 画名
* 年代
* 作者
* 纸张
* 画法
* 尺寸
* 收藏者/博物馆

**关于书法**：[搜索结果 - 中華書法數據庫 (ancientbooks.cn)](https://calligraphy.ancientbooks.cn/subLib/shufa/platformSearchPicture.jspx?field=txt&q=)

在这个数据集中，一个比较完整的条目大概长这样：

![image-20211007095212220](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20211007095212220.png)

* 提名
* 书体
* 年代
* 作者
* 译文

计划先从前一个“中华珍宝馆”数据库中进行数据爬取和收集。

