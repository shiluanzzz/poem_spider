# -*- coding: utf-8 -*-
import json
import traceback

import scrapy
from scrapy.http import Request
from urllib import parse
from poem_spider.items import PoemSpiderItem, BaiduItem


class BaiduChangjingSpider(scrapy.Spider):

    with open('F:\\PyProject\\poem_spider\\poem_spider\\util\\poet.json','r') as f:
        data=json.load(f)
        f.close()
        start_urls_data=["https://hanyu.baidu.com/hanyu/ajax/search_list?wd={}&from=poem&pn=1".format(each) for each in data]
    name = 'baidu_changjing'
    # allowed_domains = ['https://hanyu.baidu.com']
    start_urls = start_urls_data

    def parse(self, response):
        ## 从ajax接口中获取这诗人对应的所有页面
        data=json.loads(response.text)
        try:
            pages=data['ret_array'][0]['poems']['extra']['total-page']
            poet=data['ret_array'][0]['author']['baike_name'][0]
            for a in range(1, int(pages) + 1):
                url="https://hanyu.baidu.com/hanyu/ajax/search_list?wd={}&from=poem&pn={}".format(poet,a)
                yield Request(url=url,callback=self.parse_poem_url_page,dont_filter=True)
        except:
            # 防止查询不到这个诗人
            pass

    # 解析每一页中的sid
    def parse_poem_url_page(self,response):
        data = json.loads(response.text)
        a=data['ret_array'][0]['poems']['ret_array']
        b = [each['sid'][0] for each in a] # sid 列表
        for each in b:
            url="https://hanyu.baidu.com/shici/detail?pid={}".format(each)
            yield Request(url=url,callback=self.parse_poem_page,dont_filter=True)

    # 解析诗词页面
    def parse_poem_page(self,response):

        rr=response
        ob=BaiduItem()
        ob['url']=response.url
        try:
            title=rr.xpath('//*[@id="poem-detail-header"]/h1/text()').extract()[0]
            ob['title']=title
        except:
            ob['title'] = ""

        try:
            info=rr.xpath('string(//*[@id="poem-detail-header"]/div[1])').extract()[0]
            info=info.replace("\n"," ").replace(" ","").replace("译文对照","")
            author=info.replace("【作者】","-").replace("【朝代】","-").split("-")[1]
            chaodai=info.replace("【作者】","-").replace("【朝代】","-").split("-")[2]
            ob['chaodai'] = chaodai
            ob['author'] = author
        except:
            ob['chaodai'] = ""
            ob['author'] = ""

        try:
            content = rr.xpath('string(//*[@id="poem-detail-header"]/div[3])').extract()[0].replace(" ", "").replace("\n", "")
            #//*[@id="poem-detail-header"]/div[3]
            ob['content'] = content
        except:
            traceback.print_exc(file=open('error.txt',"w+"))
            ob['content'] = ""
        try:
            tags = rr.xpath('//*[@id="poem-detail-header"]/div[4]/div[2]//a//text()').extract()
            tag = ",".join(tags)
            ob['tag'] = tag
        except:
            traceback.print_exc(file=open('error.txt', "w+"))
            ob['tag'] = ""
        try:
            yiwen = rr.xpath('//*[@id="poem-detail-translation"]/div[3]//text()').extract()[0]
            ob['yiwen'] = yiwen
        except:
            ob['yiwen'] = ""
        try:
            zhushi = rr.xpath('string(//*[@id="poem-detail-zhushi"]/div[3]/p)').extract()[0].replace("\n", "").replace(
                " ", "")
            ob['zhushi'] = zhushi
        except:
            ob['zhushi'] = ""

        try:
            shangxi = rr.xpath('string(//*[@id="poem-detail-shangxi"]/div[3])').extract()[0].replace('\n', '').replace(' ', '')
            if '...' in shangxi:
                link=rr.xpath('//*[@id="poem-detail-shangxi"]/div[3]/a/@href').extract()[0]
                shangxi=shangxi+"link:{}".format(link)
            ob['shangxi'] = shangxi
        except:
            ob['shangxi'] = ""

        yield ob


    # 以前的写的一个函数
    def parse_former(self,response):
        """
        诗词详细页面调用，讲诗词内容写完。
        :param response:
        :return:
        """
        ob = PoemSpiderItem()
        try:
            title=response.xpath('//*[@id="poem-detail-header"]/h1/text()').extract()[0]
        except:
            title="null"
        try:
            author=response.xpath('//*[@id="poem-detail-header"]/div[1]/a').xpath('string(.)').extract()[0].replace('\n','').replace(' ','')
            author_link=parse.urljoin(response.url,response.xpath('//*[@id="poem-detail-header"]/div[1]/a/@href').extract()[0])
        except:
            author="null"
            author_link=""
        try:
            chaodai = response.xpath('//*[@id="poem-detail-header"]/div[1]/span').xpath('string(.)').extract()[0].replace('\n','').replace(' ','')
        except:
            chaodai=""
        try:
            content = response.xpath('//*[@id="poem-detail-header"]/div[3]').xpath('string(.)').extract()[0]
        except:
            content=""
        try:
            a = response.xpath('//*[@id="poem-detail-header"]/div[4]/div[2]/a/text()').extract()
            tag=",".join(a)
        except:
            tag=""
        try:
            translation = response.xpath('//*[@id="poem-detail-translation"]/div[3]/text()').extract()[0]
        except:
            translation=""

        ob['title']=title
        ob['author']=author
        ob['chaodai']=chaodai
        ob['content']=content
        ob['tag']=tag
        ob['translation']=translation
        ob['author_link']=author_link
        ob['url']=response.url
        yield ob


