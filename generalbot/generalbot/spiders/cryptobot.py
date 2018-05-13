# -*- coding: utf-8 -*-
import scrapy
from misc.log import *
import re
from scrapy.selector import Selector
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
    data2 = {}
    # location of csv file
    custom_settings = {
        #'FEED_URI': 'tmp/crypto.csv',
        'ITEM_PIPELINES': {
            'generalbot.pipelines.CryptobotPipeline': 300,
        }
    }

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

        for path in sites.css('a::attr(href)').extract(): #sites.xpath('//a/@href').extract():
            coinurl = url + path
            yield scrapy.Request(coinurl, callback=self.parse_coin)



    def parse_coin(self,response):
        urlgroup = response.css('.list-unstyled')[0]
        name = response.css('.text-large::text').extract()[3].strip()
        symbol = response.css('small.hidden-xs::text').extract()[0].replace('(','').replace(')','')
        rank = response.css('.label-success::text').extract()[0].replace("Rank","").strip()
        price = response.css('span.text-large2::text')[0].extract()
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
        print response.url
        urls = urlgroup.css('a::attr(href)').extract()
        keys = urlgroup.css("a::text").extract()
        info = { u'Name':name}
        info[u'Symbol'] = symbol
        info[u'Rank'] = int(rank)
        info[u'MarketCap'] = market_cap
        for i, key in  enumerate(keys):
            info[key] = urls[i]

        if info.has_key(u'Website'):
            weburl = info[u'Website']
            #self.rank = rank
            yield scrapy.Request(weburl, callback=self.parse_website, meta={'rank': int(rank)} )
        yield info
        pass


    def parse_website(self,response):
        url = response.request.url
        rank = response.meta['rank']
        helper = CryptoHelper()
        helper.process_coinsite(response, rank,self)

        print("web: %s, rank:%d"%(url,rank))
        pass

    def errback_httpbin(selfs):
        info("###Error processing call back")
        pass