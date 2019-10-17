# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageBaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection  = 'images'  # mongo存储的colletcion名称
    url = scrapy.Field() # 图片的链接
    title = scrapy.Field()  # 图片的标题


