# -*- coding: UTF-8 -*-
from __future__ import absolute_import
import re
import scrapy
import urlparse
import json
import math
from bs4 import BeautifulSoup
from scrapy.http import Request
from baidu.TbaiduItems import BaiduItem,ContentItem,ReplyItem


class Myspider(scrapy.Spider):
    name = 'baidu'
    allowed_domins = ['baidu.com']
    bash_url = 'http://tieba.baidu.com/f?kw=%E5%89%91%E7%BD%913&fr=index'
    base_url='http://tieba.baidu.com'
    comment_url='http://tieba.baidu.com/p/comment'

    def start_requests(self):
            # print('url---------------------:'+url)
            yield Request(self.bash_url, self.parse_url)

    def parse_url(self, response):
        pg = self.get_page(response)
        print('--------page-----------')
        get_page = int(pg) / 50
        for i in range(0, get_page):
            yield Request(self.bash_url + '&pn=' + str(i * 50), self.parse_all)
        # yield Request('https://tieba.baidu.com/p/5302194011?pn=1',self.get_all_content)

    def parse_all(self, response):
         print('--------------------start scrapy----------------------')
         item = BaiduItem()
         print('-----------start---------------')
         boxs = response.xpath("//li[contains(@class,'j_thread_list')]")
         for box in boxs:
                item['user_info'] = box.xpath('./@data-field').extract()[0]
                item['title'] = box.xpath(
                    ".//div[contains(@class,'threadlist_title')]/a/text()").extract()[0]
                item['url'] = box.xpath(
                    ".//div[contains(@class,'threadlist_title')]/a/@href").extract()[0]
                item['short_content'] = box.xpath(".//div[contains(@class,'threadlist_abs')]/text()").extract(
                )[0] if len(box.xpath(".//div[contains(@class,'threadlist_abs')]/text()").extract()) > 0 else ''
                if box.xpath('.//img/@src'):
                   item['imgs'] = box.xpath('.//img/@src').extract()[0]
                else:
                   item['imgs'] = []
                yield item   
                yield Request(self.base_url+item['url'],self.get_content)
    def get_content(self,response):
        url=response.url
        parse_url=urlparse.urlparse(url)
        page=self.get_content_page(response)
        for i in page:
            yield Request(self.base_url+parse_url[2]+'?pn='+str(i),self.get_all_content)
    def get_all_content(self,response):
        url=response.url
        parse_url=urlparse.urlparse(url)
        page=self.get_content_page(response)
        item=ContentItem()
        reply_item=ReplyItem()
        print('-------------get content-------------------')
        boxs=response.xpath("//div[contains(@class,'l_post l_post_bright j_l_post clearfix  ')]")
        for box in boxs:
            # print(box)
            item['url']=parse_url[2]
            json_info=box.xpath('./@data-field').extract()[0]
            data_info=json.loads(json_info)
            item['author_info']=data_info['author']
            item['content']=data_info['content']
            comment=data_info['content']['comment_num']
            print('------------comment_num:'+str(comment)+'---------------------')
            comment_page=math.ceil(float(comment)/10)
            comment_page=int(comment_page);
            item['post_id']=data_info['content']['post_id']
            item['thread_id']=data_info['content']['thread_id']
            item['floor_num']=data_info['content']['post_no']
            item['created_at']=box.xpath(".//span[contains(@class,'tail-info')]/text()").extract()[2] if len(box.xpath(".//span[contains(@class,'tail-info')]/text()").extract())>2 else box.xpath(".//span[contains(@class,'tail-info')]/text()").extract()[1]  
            print('--------------comment_page:'+str(comment_page)+'----------------')
            yield item
            if comment_page>0:
               for i in range(1,comment_page):
            #        print('------------test:'+str(i)+'--------------')
                   yield Request(self.comment_url+'?tid='+str(data_info['content']['thread_id'])+'&pid='+str(data_info['content']['post_id'])+'&pn='+str(i),self.get_comment)
            
    def get_content_page(self,response):
        page=response.xpath("//div[contains(@class,'p_thread thread_theme_5')]/div[@class='l_thread_info']/ul/li[@class='l_reply_num']/span[@class='red']/text()").extract()[1]
        return page        
    def get_page(self, response):
        print('------------------')
        sites = response.xpath('//div[@class="thread_list_bottom clearfix"]')
        for site in sites:
            urls = site.xpath(
                './/a[@class="last pagination-item "]/@href').extract_first()
            print(urls)
            parse = urlparse.urlparse(urls)
            print(parse)
            pg = dict((k, v if len(v) > 1 else v[0])
                      for k, v in urlparse.parse_qs(parse[4]).iteritems())
            return pg['pn']
    def get_comment(self,response):
        url=response.url
        query=urlparse.urlparse(url).query
        querys=dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])
        print(querys);
        item=ReplyItem()
        body=response.xpath("//li[contains(@class,'lzl_single_post j_lzl_s_p')]")
        for bg in body:
            user_name=bg.xpath(".//div[contains(@class,'lzl_cnt')]/a[contains(@class,'at j_user_card ')]/text()").extract_first()
            content=bg.xpath(".//div[contains(@class,'lzl_cnt')]/span").extract_first()
            item['user_name']=user_name
            item['content']=content
            item['post_id']=querys['pid']
            item['thread_id']=query['tid']
            item['created_at']=bg.xpath(".//div[contains(@class,'lzl_cnt')]/div[contains(@class,'lzl_content_reply')/span[contains(@class,'lzl_time')]/text()]").extract_first()
            yield item
            
        