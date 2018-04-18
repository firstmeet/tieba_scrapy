# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8') 
import codecs  
import json  
from logging import log
import pymongo
from scrapy.conf import settings
from baidu.TbaiduItems import BaiduItem,ContentItem,ReplyItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BaiduPipeline(object):
    def __init__(self):  
        self.file = codecs.open('info.json', 'w', encoding='utf-8')#保存为json文件  
    def process_item(self, item, spider):  
        line = json.dumps(dict(item)) + "\n"#转为json的  
        self.file.write(line)#写入文件中  
        return item  
    def spider_closed(self, spider):#爬虫结束时关闭文件  
        self.file.close() 

class MongoDbPipeline(object):
    def __init__(self):
        self.host = settings["MONGODB_HOST"]
        self.port = settings["MONGODB_PORT"]
        self.dbname = settings["MONGODB_DBNAME"]
        self.sheetname = settings["MONGODB_SHEETNAME"]
        # 创建MONGODB数据库链接
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        # 指定数据库
        self.mydb = self.client[self.dbname]
        # 存放数据的数据库表名
        self.post = self.mydb[self.sheetname]

    def process_item(self, item, spider):
        if isinstance(item,BaiduItem):
            data = dict(item)
            self.post.insert(data)
            return item
        if isinstance(item,ContentItem):
            content_data=dict(item)
            self.sheetname=settings["MONGODB_CONTENT"]
            self.post=self.mydb[self.sheetname]
            self.post.insert(content_data)
            return item
        if isinstance(item,ReplyItem):
            reply_data=dict(item)
            self.sheetname=settings["MONGODB_REPLY"]
            self.post=self.mydb[self.sheetname]
            self.post.insert(reply_data)
            return item
