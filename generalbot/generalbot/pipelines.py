# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import pickle
from collections import OrderedDict


class GeneralbotPipeline(object):
    def __init__(self):
        self.file = codecs.open('data_utf8.cvs', 'w', encoding='utf-8')
        self.pickle = open("data.pkl","wb")
        self.data = []

    def process_item(self, item, spider):
        line =  [ item[v] for v in item]
        l = ",".join(line) +'\n'#json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(l)
        self.data.append(item)
        return item

    def close_spider(self, spider):
        self.file.close()
        pickle.dump(self.data,self.pickle)
        self.picle.close()

