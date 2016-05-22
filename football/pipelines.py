# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class FootballPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'football')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
#        namelist = ['epl' + i.split('-')[0] for i in item['season']]
#        name = namelist[0]
        name = 'epl' + item['season'][0].replace('-','')
        self.db[name].insert(dict(item))
        return item

#    def process_item(self, item, spider):
#        if spider.name == 'football':
#            if '2015-2016' in item['season']:
#                self.db['epl1516'].insert(dict(item))
#            elif '2014-2015' in item['season']:
#                self.db['epl1415'].insert(dict(item))
#            else:
#                self.db['epl1314'].insert(dict(item))
#        return item