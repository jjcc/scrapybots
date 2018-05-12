# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import pickle
from collections import OrderedDict
from misc.log import *
from misc.metrices import *
import json

class GeneralbotPipeline(object):
    def __init__(self):
        self.file = codecs.open('data_utf8n.cvs', 'w', encoding='utf-8')
        self.pickle = open("datan.pkl","wb")
        self.data = []
        self.data2 = {}
        info(">>>GeneralPipeline Starting")

    def process_item(self, item, spider):
        line =  [ item['item'][v] for v in item['item']]
        l = ",".join(line) +'\n'#json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        ll = item['url'] + "," + l
        #self.file.write(ll)
        if item['url'] not in self.data2:
            self.data2[item['url']] = []
        self.data2[item['url']].append(item['item'])

        self.data.append(item)
        return item

    def close_spider(self, spider):
        for kurl,v in self.data2.iteritems():

            for item in v:
                line = [item[i] for i in item ]
                l = ",".join(line)
                ll = kurl + " ," + l + "\n"
                self.file.write(ll)

            print "############%s"%kurl
            metrices = calculate(v)
            print "total delta:%d, total comments:%d,count:%d, subscribers:%s,online:%s\n"%metrices
        self.file.close()
        pickle.dump(self.data2,self.pickle)

        info("<<<GeneralPipeline Closing")
        self.pickle.close()


class CryptobotPipeline(object):
    def __init__(self):
        self.file = codecs.open('crypto_utf8n.json', 'w', encoding='utf-8')
        self.file.write("[\n")
        self.pickle = open("crypton.pkl","wb")
        self.data = []
        self.data2 = {}
        info(">>>CryptoPipeline Starting")

    def process_item(self, item, spider):
        if item['Rank'] not in spider.data2.keys():
            spider.data2[item['Rank']] = {}
        spider.data2[item['Rank']]['coininfo'] = item
        data = json.dumps(OrderedDict(item),sort_keys=True, indent=4) + ",\n"
        self.file.write(data)
        return data

    def close_spider(self, spider):

        self.file.write("]")
        self.file.close()
        # pickle.dump(self.data2,self.pickle)
        ranklist = spider.data2.keys()
        ranklist.sort()
        file2  = codecs.open('crypto_utf8m.json', 'w', encoding='utf-8')
        file2.write("[\n")
        for rank in ranklist:
            item = spider.data2[rank]
            data = json.dumps(OrderedDict(item),sort_keys=True, indent=4) + ",\n"
            file2.write(data)
        file2.write("]\n")
        file2.close()

        info("<<<CryptoPipeline Closing")
        self.pickle.close()
