import scrapy
from misc.log import *
import re
from scrapy.selector import Selector
from generalbot.items import *


class RedditSpider(scrapy.Spider):
    # spider name
    name = 'cryptobot'
    # list of allowed domains
    allowed_domains = ['coinmarketcap.com']
    # staring url for scraping
    start_urls = ['https://coinmarketcap.com']
    #for url in open("/path_to/urls.txt"):
    #    start_urls.append(url)

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
        sites = sel.css('.currency-name-container')[0:5]

        for path in sites.css('a::attr(href)').extract(): #sites.xpath('//a/@href').extract():
            coinurl = url + path
            yield scrapy.Request(coinurl, callback=self.parse_site)



    def parse_site(self,response):
        urlgroup = response.css('.list-unstyled')[0]
        print response.url
        urls = urlgroup.css('a::attr(href)').extract()
        keys = urlgroup.css("a::text").extract()
        info = {}
        for i, key in  enumerate(keys):
            info[key] = urls[i]

        yield info
        pass



    def errback_httpbin(selfs):
        info("###Error processing call back")
        pass