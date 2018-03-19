# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GeneralbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    vote = scrapy.Field()
    created_at = scrapy.Field()
    comments = scrapy.Field()
    pass


class RedditItem(scrapy.Item):
    subreddit = scrapy.Field()
    subscribers = scrapy.Field()
    users = scrapy.Field()
    pass
