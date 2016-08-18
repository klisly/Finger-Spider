# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json
acceptPre0 = "http://www.sanwen.com/sanwen/"
acceptPre1 = "http://www.sanwen.com/quwen/"
acceptPre2 = "http://www.sanwen.com/xiaohua/"
acceptPre3 = "http://www.sanwen.com/lishigushi/"
acceptPre4 = "http://www.lookmw.cn/"

class XiaohuaPipeline(object):
    def __init__(self):
        self.file = open('xiaohua.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item))
        self.file.write(line)
        self.file.write("\n\r")
        return item
class Meiwenting(object):
    def __init__(self):
        self.file = open('meiwenting.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item))
        self.file.write(line)
        self.file.write("\n\r")
        return item

class MongoPipeline(object):

    def getCollectionName(self, url):
        if url.startswith(acceptPre0):
            item = "sanwen";
        elif url.startswith(acceptPre1):
            item = "quwen";
        elif url.startswith(acceptPre2):
            item = "xiaohua";
        elif url.startswith(acceptPre3):
            item = "lishi";
        elif url.startswith(acceptPre4):
            item = "lookmw";
        return item;
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'corpus')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print "save item to mongodb";
        self.db[self.getCollectionName(item["url"])].insert(item)
        return item
