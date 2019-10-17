# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider,Request
import json
from image_baidu.items import ImageBaiduItem
class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['image.baidu.com']
    start_urls = ['http://image.baidu.com/']

    def start_requests(self):
        """将所有要爬取的url加入Request队列"""
        bash_url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E7%81%AB%E5%BD%B1%E5%BF%8D%E8%80%85%E5%A3%81%E7%BA%B8&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word=%E7%81%AB%E5%BD%B1%E5%BF%8D%E8%80%85%E5%A3%81%E7%BA%B8&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&cg=wallpaper&pn='
        # 网页需要AJAX请求,分析发现只需改变最后的&pn=即可,这里爬取30页，共计900章
        for page in range(self.settings.get('MAX_PAGE')+1):
            data = page * 30
            url = bash_url+str(data)
            yield Request(url,self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        # 分析网页知道图片在json的data中,循环遍历每一页的data取出需要的内容
        for image in result.get('data'):
            item = ImageBaiduItem()
            item['title'] = image.get('fromPageTitleEnc')
            item['url'] = image.get('hoverURL')
            yield item

