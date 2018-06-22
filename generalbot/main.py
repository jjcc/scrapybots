'''
Created on 2018-03-06
@author: jjccforth
'''
import scrapy.cmdline


def main():
    #scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'redditbot'])
    scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'cryptobot'])
    #scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'techcrunch'])
    #scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'shopclues'])

if  __name__ =='__main__':
    main()