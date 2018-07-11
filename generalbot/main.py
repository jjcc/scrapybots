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
    '''
    To collect crypto information.
    1.Run main() to collect crypto information following the list and details, along with those that have
      normal web site. Output will be "crypto_utf8_allonce.json"
    2.Complement the collected info with running simple_crawler.py to collect extra info with SPA web
     (There are some exceptions using Angular contain some static info but others dynamic. Tether is an example)
      Output will be "amendment_xxx.json"
    3.Run insert_intdb.py to combine above 2 output and integrate the result into DB 
    '''
    main()