import scrapy
from misc.log import *
import re
from generalbot.items import *


class RedditSpider(scrapy.Spider):
    # spider name
    name = 'redditbot'
    # list of allowed domains
    allowed_domains = ['www.reddit.com/r/Nootropics/']
    # staring url for scraping
    start_urls = ['https://www.reddit.com/r/Nootropics/']
    # location of csv file
    custom_settings = {
        'FEED_URI': 'tmp/reddit.csv',
        'ITEM_PIPELINES': {
            'generalbot.pipelines.GeneralbotPipeline': 300,
        }
    }

    def parse(self, response):
        # Extracting the content using css selectors(earlier logic)
        titles = response.css('.title.may-blank::text').extract()
        votes = response.css('.score.unvoted::text').extract()
        times = response.css('time::attr(title)').extract()
        comments = response.css('.comments::text').extract()
        # Give the extracted content row wise.
        # subscribers = response.css('.subscribers>span:nth-child(1)::text').extract()
        users = response.css('.number::text').extract()  # 0: subscriber, 1: user online
        subscribers = users[0]
        onlineusers = users[1]
        including_subs = response.css('.md a::attr(href)').getall()
        # including_subs2 = response          .xpath("//div[@class='md']/a")
        info('subscribers: ' + subscribers[0])

        announcement_times = response.xpath("//*[contains(@class,'stickied-tagline')]/..").css(
            "time::attr(title)").extract()
        # if d(times) in announcment_times:
        #	continue

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
            yield itm
        # posts.append(itm)

        subredditInfo = RedditItem()
        subscribers_alt = subscribers.replace(",", "")
        onlineusers_alt = onlineusers.replace(",", "")
        subredditInfo['subscribers'] = subscribers_alt
        subredditInfo['users'] = onlineusers_alt
        subredditInfo['subreddit'] = "xxx"  # posts

        yield subredditInfo
