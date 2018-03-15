# Scrapy settings for hacker_news project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import sys
import os
from os.path import dirname
path = dirname(dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(path)
from misc.log import *

BOT_NAME = 'general_crawler'

SPIDER_MODULES = ['general_crawler.spiders']
NEWSPIDER_MODULE = 'general_crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hacker_news (+http://www.yourdomain.com)'

DOWNLOADER_MIDDLEWARES = {
   # 'misc.middleware.CustomHttpProxyMiddleware': 400,
    'misc.middleware.CustomUserAgentMiddleware': 401,
    'general_crawler.middlewares.TutorialDownloaderMiddleware': 543,
}

#SPIDER_MIDDLEWARES = {
#    'tutorial.middlewares.TutorialSpiderMiddleware': 543,
#}




ITEM_PIPELINES = {
    'general_crawler.pipelines.JsonWithEncodingPipeline': 300,
    #'gemeral_crawler.pipelines.RedisPipeline': 301,
}

LOG_LEVEL = 'DEBUG'

DOWNLOAD_DELAY = 1
