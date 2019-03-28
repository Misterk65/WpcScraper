# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class WpcscraperPipeline(object):

    def __init__(self):
        self.conn = pymongo.MongoClient(

            'mongodb+srv://DevUser:$B116168kp$@cluster0-4am5x.mongodb.net/test?retryWrites=true'
        )

        db = self.conn['scraper']
        self.collection = db['tbl_data_temp']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
