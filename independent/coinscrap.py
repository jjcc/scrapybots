#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from pymarketcap import AsyncPymarketcap

#count = 0

async def mainloop(mylist):
    count  = 0
    #mylist = ['BTC',"ETH","XRP",'BCH','EOS','XLM','LTC','ADA','USDT','MIOTA']
    async with AsyncPymarketcap() as apym:
        async for currency in apym.every_currency(mylist):
            if count > 100:
                break
            print(currency)
            print(",")
            count +=1

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    mylist = ['BTC', "ETH", "XRP", 'BCH', 'EOS', 'XLM', 'LTC', 'ADA', 'USDT', 'MIOTA']
    print('[\n')
    loop.run_until_complete(mainloop(mylist))
    print('\n]')
