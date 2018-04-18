# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_info = scrapy.Field()  
    title = scrapy.Field()  
    url = scrapy.Field()  
    short_content = scrapy.Field()  
    imgs = scrapy.Field()
class ContentItem(scrapy.Item):
    url=scrapy.Field()
    author_info=scrapy.Field()
    content=scrapy.Field()
    floor_num=scrapy.Field()
    created_at=scrapy.Field()
class ReplyItem(scrapy.Item):
    url=scrapy.Field()
    floor_num=scrapy.Field()
    reply_user_info=scrapy.Field()
    reply_content=scrapy.Field()
    created_at=scrapy.Field()   