'''
Created on 2018-03-06
@author: jjccforth
'''
import scrapy.cmdline
import sys

def main():
    sys_param = None
    if len(sys.argv) > 1:
        sys_param = sys.argv[1]
    #scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'redditbot'])
    if sys_param:
        scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'cryptobot','-a','arg='+ sys_param])
    else:
        scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'cryptobot'])
    #scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'techcrunch'])
    #scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'shopclues'])

if  __name__ =='__main__':
    main()