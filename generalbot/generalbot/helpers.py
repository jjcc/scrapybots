# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup



class CryptoHelper(object):


    def process_coinsite(self,response, rank, spider):
        soup = BeautifulSoup(response.text, 'lxml')
        print("extra info for rank:%d"%rank)

        if rank not in spider.data2.keys():
            spider.data2[rank] = {}
        if 'extrainfo' not in spider.data2[rank]:
            spider.data2[rank]['extrainfo'] = {}
        for link in soup.find_all('a'):
            address = link.get('href')
            if address is None:
                continue
            if 'twitter' in address:
                spider.data2[rank]['extrainfo']['twitter'] = address
                print("twitter: %s"%address)
            if 'reddit' in address:
                spider.data2[rank]['extrainfo']['reddit'] = address
                print("reddit: %s"%address)
            if 'facebook' in address:
                spider.data2[rank]['extrainfo']['facebook'] = address
                print("facebook: %s"%address)
            if 'linkedin' in address:
                spider.data2[rank]['extrainfo']['linkedin'] = address
                print("linkein: %s"%address)
        pass


    def process_github(self,response):
        pass


