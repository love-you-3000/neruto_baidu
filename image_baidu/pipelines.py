# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ImageBaiduPipeline(object):
    def process_item(self, item, spider):
        return item

import pymongo

class MongoPipline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        """
        scrapy为我们访问settings提供了这样的一个方法,这里,
        我们需要从settings.py文件中,取得数据库的URI和数据库名称
        """
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        """
        爬虫一旦开启,就会实现这个方法,连接到数据库
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        """
        每个实现保存的类里面必须都要有这个方法,且名字固定,用来具体实现怎么保存
        """
        name = item.__class__.__name__  # 将表名定义成item的类名,即QuoteItem
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self,spider):
        """
        爬虫一旦开启,就会实现这个方法,连接到数据库
        """
        self.client.close()

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class ImagePipeline(ImagesPipeline):
    """
    为了实现图片的下载,需要使用ImagePipeline,但内置的此类会默认读取image_urls
    并认为该字段是一个列表,它会遍历Item的image_urls字段执行下载
    但是现在生成的item的图片链接既不是image_urls,也不是列表形式,而是单个的url,所以需要自定义ImagePipeline
    继承内置ImagePipeline,并且重写几个方法.
    """
    def file_path(self, request, response=None, info=None):
        """
        第一个参数request就是当前下载对应的Request对象,这个方法用来返回保存的文件名
        直接将图片链接的最后一部分当做文件名即可
        利用split函数分割链接并提取最后一部分,返回结果
        """
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        """
        这个函数是单个item完成下载后的处理方式
        因为并不是每张图片都会下载成功,所以我们需要分析下载结果并剔除下载失败的图片
        第一个参数results就是该Item对应的下载结果
        它是一个列表形式,列表的每一个元素是一个元祖,其中包含了下载成功还是失败的信息
        这里我们遍历下载结果找出所有成功的下载列表
        如果列表为空,那么该item即下载失败,抛出异常
        否则返回该item
        """
        image_paths = [x['path'] for ok,x in results if ok]
        if not image_paths:
            raise DropItem('Image Download Failed!')
        return item

    def get_media_requests(self, item, info):
        """
        第一个参数item是爬取生成的Item对象,我们将它的url字段取出来,然后直接生成Request对象
        此Request对象加入调度队列,等待被调度,执行下载
        """
        yield Request(item['url'])