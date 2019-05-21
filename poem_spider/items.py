# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PoemSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    author=scrapy.Field()
    chaodai=scrapy.Field()
    content=scrapy.Field()
    tag=scrapy.Field()
    translation=scrapy.Field()
    author_link=scrapy.Field()
    url=scrapy.Field()


class PoemSpiderItem_shicidaquan(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    author=scrapy.Field()
    chaodai=scrapy.Field()
    content=scrapy.Field()
    tag=scrapy.Field()
    #translation=scrapy.Field()
    #author_link=scrapy.Field()
    url=scrapy.Field()

class BaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    author=scrapy.Field()
    chaodai=scrapy.Field()
    content=scrapy.Field()
    tag=scrapy.Field()
    yiwen=scrapy.Field()
    zhushi=scrapy.Field()
    shangxi=scrapy.Field()
    url=scrapy.Field()