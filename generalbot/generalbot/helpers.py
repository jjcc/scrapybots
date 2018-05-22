# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from misc.log import *


class CryptoHelper(object):


    def process_coinsite(self,response, rank, spider):
        soup = BeautifulSoup(response.text, 'lxml')
        info("extra info for rank:%d"%rank)

        if rank not in spider.data2.keys():
            spider.data2[rank] = {}
        if 'extrainfo' not in spider.data2[rank]:
            spider.data2[rank]['extrainfo'] = {}
        for link in soup.find_all('a'):
            address = link.get('href')
            if address is None:
                info("no href link for this one,rank%d"%rank)
                continue
            if 'twitter' in address:
                spider.data2[rank]['extrainfo']['twitter'] = address
                #print("twitter: %s"%address)
            if 'reddit' in address:
                spider.data2[rank]['extrainfo']['reddit'] = address
                #print("reddit: %s"%address)
            if 'facebook' in address:
                spider.data2[rank]['extrainfo']['facebook'] = address
                #print("facebook: %s"%address)
            if 'linkedin' in address:
                spider.data2[rank]['extrainfo']['linkedin'] = address
                #print("linkein: %s"%address)
            if 'telegram' in address:
                spider.data2[rank]['extrainfo']['telegram'] = address
                #print("telegram: %s"%address)
            if 't.me' in address:
                spider.data2[rank]['extrainfo']['telegram'] = address
                #print("telegram: %s"%address)
            if 'slack' in address:
                spider.data2[rank]['extrainfo']['slack'] = address
                #print("slack: %s"%address)
            if 'wechat' in address:
                spider.data2[rank]['extrainfo']['wechat'] = address
                #print("wechat: %s"%address)
        pass


    def process_github(self,response):
        pass


