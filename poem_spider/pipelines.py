# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

import MySQLdb
import MySQLdb.cursors
class PoemSpiderPipeline(object):

    def __init__(self):
        self.connect=pymysql.connect("localhost","root","stfk0615","seekpoem",charset='utf8',use_unicode=True)
        self.cursor=self.connect.cursor()
    def process_item(self, item, spider):
        insert_sql = """
                    INSERT INTO baidu(title,author,chaodai,content,tag,translations,author_link,url)
                    VALUES("{}","{}","{}","{}","{}","{}","{}","{}")
                """.format(item['title'],item['author'],item['chaodai'],item['content'],item['tag'],item['translation'],
                           item['author_link'],item['url'])
        print(insert_sql)
        self.cursor.execute(insert_sql)
        self.connect.commit()
        # return item

        return item

class MysqlTwistedPipeline(object):
    """
    异步插入数据进入数据库
    """

    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms=dict(
            host='localhost',
            db='seek_poem',
            user='root',
            password='stfk0615',
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool=adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)

    def process_item(self,item,spider):
        # 使用twisted将mysql插入变成异步执行
        query=self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)

    def handle_error(self,failure,item,spider):
        # 处理异步拆入的异常
        print(failure)
    def do_insert(self,cursor,item):
        # 执行具体的插入。
        insert_sql = """
                            INSERT INTO baidu(title,author,chaodai,content,tag,translations,author_link,url)
                            VALUES("{}","{}","{}","{}","{}","{}","{}","{}")
                        """.format(item['title'], item['author'], item['chaodai'], item['content'], item['tag'],
                                   item['translation'],
                                   item['author_link'], item['url'])
        # print(insert_sql)
        cursor.execute(insert_sql)


class MysqlTwistedPipeline_shicidaquan(object):
    """
    异步插入数据进入数据库
    """

    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms=dict(
            host='localhost',
            db='seek_poem',
            user='root',
            password='stfk0615',
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool=adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)

    def process_item(self,item,spider):
        # 使用twisted将mysql插入变成异步执行
        query=self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)

    def handle_error(self,failure,item,spider):
        # 处理异步拆入的异常
        print(failure)
    def do_insert(self,cursor,item):
        # 执行具体的插入。
        insert_sql = """
                            INSERT INTO gushiwen(title,author,chaodai,content,tag,url)
                            VALUES("{}","{}","{}","{}","{}","{}")
                        """.format(item['title'], item['author'], item['chaodai'], item['content'], item['tag'],
                                   item['url'])
        # print(insert_sql)
        cursor.execute(insert_sql)


class MysqlTwistedPipeline_baiduhanyu(object):
    """
    异步插入数据进入数据库
    """

    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms=dict(
            host='localhost',
            db='seek_poem',
            user='root',
            password='stfk0615',
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool=adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)

    def process_item(self,item,spider):
        # 使用twisted将mysql插入变成异步执行
        query=self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)

    def handle_error(self,failure,item,spider):
        # 处理异步拆入的异常
        print(failure)
    def do_insert(self,cursor,item):
        # 执行具体的插入。
        insert_sql = 'INSERT INTO baiduhanyu(title,author,chaodai,content,tag,yiwen,zhushi,shangxi,url)VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}")'\
            .format(item['title'], item['author'], item['chaodai'], item['content'], item['tag'],item['yiwen'],item['zhushi'],item['shangxi'],item['url'])
        a=insert_sql
        cursor.execute(insert_sql)