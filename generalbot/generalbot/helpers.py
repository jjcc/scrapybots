# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from misc.log import *


class CryptoHelper(object):


    def process_coinsite(self,response, rank, spider):
        soup = BeautifulSoup(response.text, 'lxml')
        info("extra info for rank:%d"%rank)

        if rank not in spider.data.keys():
            spider.data[rank] = {}
        if 'extrainfo' not in spider.data[rank]:
            spider.data[rank]['extrainfo'] = {}
        for link in soup.find_all('a'):
            address = link.get('href')
            if address is None:
                info("no href link for this one,rank%d"%rank)
                continue
            if 'twitter' in address:
                spider.data[rank]['extrainfo']['twitter'] = address
                #print("twitter: %s"%address)
            if 'reddit' in address:
                spider.data[rank]['extrainfo']['reddit'] = address
                #print("reddit: %s"%address)
            if 'facebook' in address:
                spider.data[rank]['extrainfo']['facebook'] = address
                #print("facebook: %s"%address)
            if 'linkedin' in address:
                spider.data[rank]['extrainfo']['linkedin'] = address
                #print("linkein: %s"%address)
            if 'telegram' in address:
                spider.data[rank]['extrainfo']['telegram'] = address
                #print("telegram: %s"%address)
            if 't.me' in address:
                spider.data[rank]['extrainfo']['telegram'] = address
                #print("telegram: %s"%address)
            if 'discord' in address:
                spider.data[rank]['extrainfo']['discord'] = address
                #print("telegram: %s"%address)
            if 'slack' in address:
                spider.data[rank]['extrainfo']['slack'] = address
                #print("slack: %s"%address)
            if 'wechat' in address:
                spider.data[rank]['extrainfo']['wechat'] = address
                #print("wechat: %s"%address)
            if 'youtu' in address:
                spider.data[rank]['extrainfo']['youtube'] = address
                #print("wechat: %s"%address)
        pass


    def process_github(self,response):
        pass


