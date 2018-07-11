# -*- coding: utf-8 -*-
import scrapy
from misc.log import *
import re
from generalbot.items import *
import datetime

from sqlalchemy import create_engine
from misc.dbcreate import Base
from sqlalchemy.orm import *

from misc.dbcreate import Topic

class RedditSpider(scrapy.Spider):
    # spider name
    name = 'redditbot'
    # list of allowed domains
    allowed_domains = ['www.reddit.com']
    # staring url for scraping
    start_urls = [{'url':'https://www.reddit.com/r/Nootropics/','id' :1},
                  {'url':'https://www.reddit.com/r/eos/','id':2}]

    #for url in open("/path_to/urls.txt"):
    #    start_urls.append(url)
    engine = create_engine('sqlite:///bigdata.db')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # location of csv file
    custom_settings = {
        'FEED_URI': 'tmp/reddit.csv',
        'ITEM_PIPELINES': {
            'generalbot.pipelines.RedditbotPipeline': 300,
        }
    }

    def start_requests(self):
        cryptos =self.session.query(Topic).all()
        #for u in self.start_urls:
        for u in cryptos:
            if u.reddit:
                info("requesting:%s, id:%d, symbol:%s"%(u.reddit, u.id, u.symbol))
                if not "http" in u.reddit:
                    u.reddit = "https:" + u.reddit
                yield scrapy.Request(u.reddit, callback=self.parse,
                                    errback=self.errback_httpbin,
                                    dont_filter=True,
                                    meta = {'tid': u.id})


    def parse(self, response):
        info(">>>parsing start")
        url = response.request.url
        reqinfo = {}
        reqinfo['mark'] = "IIIIII"
        reqinfo['url'] = url

        #For debug purpose
        #response_text = response.text
        #topic = url.split('/')[-2]
        #fn =  "output/" + topic + "_" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + "_response.html"
        #with open(fn, "w",encoding='utf-8') as fout:
        #    fout.write(response_text)

        #yield reqinfo
        # Extracting the content using css selectors(earlier logic)
        titles = response.css('.title.may-blank::text').extract()
        votes = response.css('.score.unvoted::text').extract()
        times = response.css('time.live-timestamp ::attr(title)').extract()
        comments = response.css('.comments::text').extract()
        # Give the extracted content row wise.
        # subscribers = response.css('.subscribers>span:nth-child(1)::text').extract()
        users = response.css('.number::text').extract()  # 0: subscriber, 1: user online
        if len(users) < 2:
            yield response.follow( url,  callback=self.parse)
            return
        subscribers = users[0]
        onlineusers = users[1]
        including_subs = response.css('.md a::attr(href)').getall()
        # including_subs2 = response          .xpath("//div[@class='md']/a")
        info('subscribers: ' + subscribers[0])

        announcement_times = response.xpath("//*[contains(@class,'stickied-tagline')]/..").css(
            "time::attr(title)").extract()

        # subs = including_subs.getall()
        subs = [x for x in including_subs if re.search(r'^\/r\/', x)]

        posts = []
        for item in zip(titles, votes, times, comments):
            # create a dictionary of title, vote, publish date and comments
            scraped_info = {
                'title': item[0],
                'vote': item[1],
                'created_at': item[2],
                'comments': item[3],
            }
            # skip the announcement items
            if item[2] in announcement_times:
               continue

            itm = GeneralbotItem()
            itm['title'] = item[0]
            itm['vote'] = item[1]
            itm['created_at'] = item[2]
            itm['comments'] = item[3]

            # yield or give the scraped info to scrapy
            # yield scraped_info
            yield { "url":url,"item": itm}
        # posts.append(itm)

        subredditInfo = RedditItem()
        subscribers_alt = subscribers.replace(",", "")
        onlineusers_alt = onlineusers.replace(",", "")
        subredditInfo['subscribers'] = subscribers_alt
        subredditInfo['users'] = onlineusers_alt
        subredditInfo['subreddit'] = "xxx"  # posts
        subredditInfo['topicid'] = response.meta['tid']
        yield {'url':url, 'item':subredditInfo}


    def errback_httpbin(selfs):
        info("###Error processing call back")
        pass