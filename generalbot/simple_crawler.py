
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import datetime
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import json


import platform

import os

class SimpleCrawler(object):
    chrome_path = r"E:\Software\ChromeDriver\chromedriver.exe"
    #target_url =
    #stock1 = "http://www.investertech.com/tkchart/tkchart.asp?logo=&home=/default.asp&banner=&stkname=MSFT+INTC+DELL+CSCO+JDSU+ORCL+AMAT+GOOG+IBM+BRCM+AAPL+SYMC"

    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.Accept-Language'] = 'en-US,en'
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] \
        = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    if platform.system() == 'Linux':
        phantom_location = '/usr/local/bin/phantomjs'
    else:
        phantom_location = 'E:/software/phantomjs-2.1.1-windows/bin/phantomjs.exe'
#browser = webdriver.PhantomJS(executable_path=phantom_location)

    #define driver
    driver = webdriver.Chrome(chrome_path)
    #launch browser
    #browser.get("http://ottawa.craigslist.ca")

    def get_info_by_url(self,  url,dir = ""):
        browser = self.driver
        '''
        '''
        try:
            browser.set_page_load_timeout(30)
            browser.get(url)
        except :
            print ("**wrong",url)
            return {}
        # wait up to 10 seconds for page to load
        timeout = 10
        datestring = datetime.date.today().strftime("%Y%m%d")
        browser.execute_script("window.scrollTo(0,1000);")
        time.sleep(5)
        count = 0
        hrefs = browser.find_elements_by_xpath("//a[@href]")

        targetlinks = ["reddit","github","twitter","facebook","t.me","discord","linkedin","youtu","wechat"]
        print(">>>%s"%url)
        exinfo = {}
        for h in hrefs:
            link = h.get_attribute("href")
            for t in targetlinks:
                if t in link:
                    #special for github
                    if t =="github":
                        if "github.io" in link: #ignore github.io address
                            continue
                        match =  re.search("github.com/",link)
                        if match:
                            post = match.string[match.end():]
                            segs = post.split('/')
                            if len(segs) > 1 and segs[1] != "":
                                if t in exinfo:
                                    continue
                                else:
                                    exinfo[t] = "https://github.com/" + segs[0]
                                    print(t,link)
                                    continue
                    print (t, link)
                    exinfo[t] = link
        return exinfo

    #browser.find_elements_by_xpath("//a[@href]")

        return ""

def process(file):
    fp = open(file,"rb");
    data = json.load(fp)
    coininfo_filtered = {}
    for c in data:
       coininfo = c['coininfo']
       rank = coininfo['Rank']
       #print coininfo['Name']
       noextra = 0
       if "extrainfo" in c:
           extrainfo = c['extrainfo']
           if len(extrainfo) > 0:
               #pass #print "\t",extrainfo["reddit"]
               continue
           else:
               seq = ( coininfo['Name'],coininfo["Symbol"],"%d"%rank,coininfo['Website'] )
               print (",".join(seq))
       else:
           #print "\tno extrainfo"
           print (",".join((coininfo['Name'],coininfo["Symbol"],r"%d"%rank,coininfo['Website'],"*")))
           noextra = 1
       key = rank
       coininfo_filtered[key] = {u"name": coininfo['Name'], u'symbol':coininfo['Symbol'],u'website':coininfo['Website'],u'noextra':noextra }


    return coininfo_filtered

#if __name__ == '__main__':
#    file = "output/crypto_utf8_allonce.json"
#    process(file)


if __name__ == "__main__":
    file = "output/crypto_utf8_allonce.json"
    infofromfile = process(file)
    iconinfo = infofromfile
    # iconinfo = {}
    # with open("missed2.txt","r") as input:
    #     for line in input:
    #         #line1 = line.replace("* ","")
    #         tri = line.split(",")
    #         print (tri[0],tri[1],tri[2],tri[3])
    #         key = int(tri[2])
    #         iconinfo[key] = {u"Name":tri[0],u'Symbol':tri[1],u"Website":tri[3].strip()}



    urls = ["https://www.icon.foundation/"]

    sc = SimpleCrawler()
    for k,v in iconinfo.items():
        u = v[u"website"]
        extracted = sc.get_info_by_url( u )
        v[u"extracted"] = extracted
    outputfile = "output/amendment" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+ ".json"
    fout = open(outputfile,"w")
    data = json.dumps(iconinfo,sort_keys=True,indent=4)
    fout.write(data)
    fout.close()