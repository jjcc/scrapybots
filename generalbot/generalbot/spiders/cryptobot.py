# -*- coding: utf-8 -*-
import scrapy
from misc.log import *
import re
from scrapy.selector import Selector
from datetime import datetime
from generalbot.items import *
from generalbot.helpers import CryptoHelper

class CryptoSpider(scrapy.Spider):
    # spider name
    name = 'cryptobot'
    # list of allowed domains
    allowed_domains = []#'coinmarketcap.com']
    # staring url for scraping
    start_urls = ['https://coinmarketcap.com']
    #for url in open("/path_to/urls.txt"):
    #    start_urls.append(url)
    data = {}
    # location of csv file
    custom_settings = {
        #'FEED_URI': 'tmp/crypto.csv',
        'ITEM_PIPELINES': {
            'generalbot.pipelines.CryptobotPipeline': 300,
        }
    }
    start_crypto = None
    end_crypto = None
    count_crypto = 0

    def __init__(self, arg=None):
        if arg:
            start_end = arg.split(",")
            self.start_crypto = int(start_end[0])
            if len(start_end) > 1:
                self.end_crypto = int(start_end[1])
        else:
            print("No arg")

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)


    def parse(self, response):
        url = response.request.url
        reqinfo = {}
        #yield reqinfo
        # Extracting the content using css selectors(earlier logic)
        cryptos = response.css('.currency-name-container')

        items = []
        sel = Selector(response)
        sites = sel.css('.currency-name-container')#[0:5]
        parse_count = 0
        for path in sites.css('a::attr(href)').extract(): #sites.xpath('//a/@href').extract():
            if self.start_crypto:
                if parse_count < self.start_crypto:
                    parse_count += 1
                    continue
            if self.end_crypto:
                if parse_count >= self.end_crypto:
                    break
            parse_count += 1
            info("parse count:%s"%parse_count)
            coinurl = url + path
            yield scrapy.Request(coinurl, callback=self.parse_coin)



    def parse_coin(self,response):
        urlgroup = response.css('.list-unstyled')[0]
        name = response.css('.details-panel-item--name::text').extract()[1].strip()
        symbol = response.css('.text-large::text').extract()[0].replace('(','').replace(')','')
        rank = response.css('.label-success::text').extract()[0].replace("Rank","").strip()
        price = response.css('.details-panel-item--price__value::text').extract()[0]
        #change_perct = response.css('span.text-large2 span::text')[0].extract()
        #market_cap = response.css('.coin-summary-item-detail').extract()
        market_cap = response.css('.coin-summary-item-detail span::text').extract()[1]
        #1: market capital(USD)
        #6: market capital(BTC)
        #10: valumn(USD)
        #15: valumn(BTC)
        #17: circulating supply(XXX)
        #18(optional): max supply(XXX)

        #reddit = response.css(".reddit-title a::attr(href)").extraxt()
        print(response.url)
        urls = urlgroup.css('a::attr(href)').extract()
        keys = urlgroup.css("a::text").extract()
        info = { u'Name':name}
        info[u'Symbol'] = symbol
        info[u'Rank'] = int(rank)
        info[u'MarketCap'] = market_cap
        info[u'Price'] = price
        info[u'Date'] = datetime.now().strftime("%Y-%m-%d")
        for i, key in  enumerate(keys):
            info[key] = urls[i]

        if u'Website' in info:
            weburl = info[u'Website']
            #self.rank = rank
            yield scrapy.Request(weburl, callback=self.parse_website, meta={'rank': int(rank)} )
        yield info
        pass


    def parse_website(self,response):
        url = response.request.url
        rank = response.meta['rank']
        helper = CryptoHelper()
        #collect data into spider.data
        helper.process_coinsite(response, rank,self)

        info("processed web: %s, rank:%d"%(url,rank))
        pass

    def errback_httpbin(selfs):
        info("###Error processing call back")
        pass