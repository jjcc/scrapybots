# -*- coding: utf-8 -*-
import scrapy


class JspiderSpider(scrapy.Spider):
    name = 'jspider'
    allowed_domains = ['targetweb.com']
    start_urls = ['http://targetweb.com/']

    def parse(self, response):
        pass
