
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import datetime
import time
from sqlalchemy import create_engine
import json
from misc.dbcreate import Base
from sqlalchemy.orm import *


import platform

import os
from misc.dbcreate import Topic

def process(file,file_amendment):
    fp = open(file,"rb");
    data = json.load(fp)
    fpa = open(file_amendment,'rb')
    data_a = json.load(fpa)

    coininfo_filtered = {}
    engine = create_engine('sqlite:///bigdata.db')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for d in data:
       c = d['coininfo']
       crypto = Topic(name = c['Name'])
       crypto.symbol = c['Symbol']
       crypto.web = c['Website']
       crypto.github = c['Source Code']
       chat1 = ''
       chat2 = ''
       if 'Chat' in c:
           chat1 = c['Chat']
       if 'Chat 2' in c:
           chat2 = c['Chat']
       for chat in [chat1,chat2]:
           if 't.me' in chat or 'telegram' in chat:
               crypto.telegram = chat
           if 'discord' in chat:
               crypto.discord = chat

       coininfo = d['coininfo']
       rank = coininfo['Rank']
       #print coininfo['Name']
       use_amendment = 1
       if "extrainfo" in d:
           extrainfo = d['extrainfo']
           if len(extrainfo) > 0:
               #pass #print "\t",extrainfo["reddit"]
               for info in extrainfo:
                   if 'reddit' in info:
                       crypto.reddit = info['reddit']
                   if 'telegram' in info:
                       crypto.telegram = info['reddit']
                   if 'discord' in info:
                       crypto.discord = info['reddit']
                   if 'linkedin' in info:
                       crypto.linkedin = info['linkedin']
                   if 'facebook' in info:
                       crypto.facebook = info['facebook']
                   if 'twitter' in info:
                       crypto.twitter = info['twitter']
               use_amendment = 0
           else:
               seq = ( coininfo['Name'],coininfo["Symbol"],"%d"%rank,coininfo['Website'] )
               print (",".join(seq))
       else:
           #print "\tno extrainfo"
           print (",".join((coininfo['Name'],coininfo["Symbol"],r"%d"%rank,coininfo['Website'],"*")))
           noextra = 1
       key = '%s'%rank
       coininfo_filtered[key] = {u"name": coininfo['Name'], u'symbol':coininfo['Symbol'],u'website':coininfo['Website']}#,u'noextra':noextra }
       if use_amendment == 1:
            amendmend = data_a[key]
            extrainfo = amendmend['extracted']
            for info in extrainfo:
                if 'reddit' in info:
                   crypto.reddit = info['reddit']
                if 'telegram' in info:
                   crypto.telegram = info['reddit']
                if 'discord' in info:
                   crypto.discord = info['reddit']
                if 'linkedin' in info:
                   crypto.linkedin = info['linkedin']
                if 'facebook' in info:
                   crypto.facebook = info['facebook']
                if 'twitter' in info:
                   crypto.twitter = info['twitter']

       session.add(crypto)
       session.commit()

    return coininfo_filtered

#if __name__ == '__main__':
#    file = "output/crypto_utf8_allonce.json"
#    process(file)


if __name__ == "__main__":
    file = "output/crypto_utf8_allonce.json"
    file2 = "output/amendment_inuse.json"
    infofromfile = process(file,file2)
    mis_info = infofromfile





    for k,v in mis_info.items():
        print(k)