
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
browser = webdriver.Chrome(chrome_path)
#launch browser
#browser.get("http://ottawa.craigslist.ca")




def get_info_by_url( browser, url,dir = ""):
    '''
    '''
    try:
        browser.set_page_load_timeout(30)
        browser.get(url)
    except :
        print "**wrong",url
        return {}
    # wait up to 10 seconds for page to load
    timeout = 10
    datestring = datetime.date.today().strftime("%Y%m%d")
    browser.execute_script("window.scrollTo(0,1000);")
    time.sleep(5)
    count = 0
    hrefs = browser.find_elements_by_xpath("//a[@href]")

    targetlinks = ["reddit","github","twitter","facebook","t.me","discord"]

    exinfo = {}
    for h in hrefs:
        link = h.get_attribute("href")
        for t in targetlinks:
            if t in link:
                print t, link
                exinfo[t] = link
    return exinfo

    #browser.find_elements_by_xpath("//a[@href]")

    return ""

if __name__ == "__main__":
    iconinfo = {}
    with open("missed2.txt","r") as input:
        for line in input:
            line1 = line.replace("* ","")
            tri = line1.split(" ")
            print tri[0],tri[1],tri[2]
            key = int(tri[1])
            iconinfo[key] = {u"Name":tri[0],u"Website":tri[2]}


    urls = ["https://www.icon.foundation/"]

    for k,v in iconinfo.iteritems():
        u = v[u"Website"]
        extracted = get_info_by_url(browser, u )
        v[u"extracted"] = extracted
    fout = open("amendment.json","wb")
    data = json.dumps(iconinfo,sort_keys=True,indent=4)
    fout.write(data)
    fout.close()