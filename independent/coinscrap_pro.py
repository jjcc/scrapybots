#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#import asyncio
#from pymarketcap import AsyncPymarketcap
#
##count = 0
#
#async def main():
#    count  = 0
#    mylist = ['BTC',"ETH","XRP",'BCH','EOS','XLM','LTC','ADA','USDT','MIOTA']
#    async with AsyncPymarketcap() as apym:
#        async for currency in apym.every_currency(mylist):
#            if count > 100:
#                break
#            print(currency)
#            print(",")
#            count +=1
#
#if __name__ == '__main__':
#    loop = asyncio.get_event_loop()
#    print('[\n')
#    loop.run_until_complete(main())
#    print('\n]')
#
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'f002af2a-3a0e-4d6f-860c-6a508130c647',
}
base_url = 'https://pro-api.coinmarketcap.com/v1/'
base_parameters = {
  'start':'1',
  'limit':'99',
}

api_list = {
    'listings':{
        'url':'cryptocurrency/listings/latest','extra':{'convert':'USD'}
    },
    'map':{
        'url':'cryptocurrency/map','extra':{'sort':'cmc_rank'}
    },
    'info':{
        'url':'cryptocurrency/info','extra':None
    },
}

session = Session()
session.headers.update(headers)

def call_api(apiname, injected = None, use_base_param=True):
    if apiname not in api_list.keys():
        print("wrong api name")    
        return
    current_api_info = api_list[apiname]
    url =  base_url + current_api_info['url']
    if use_base_param:
        parameters = base_parameters
    else:
        parameters = {}

    if current_api_info['extra'] != None:
        for k,v in current_api_info['extra'].items():
            parameters[k] = v

    if injected != None:
        for k,v in injected.items():
            parameters[k] =  v

    try:
      fname = apiname + '_info.json'
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
      with open(f"data\\{fname}", "w") as data_file:
        json.dump(data, data_file, indent=2)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

if __name__ == "__main__":
    #call_api('map')
    with open('data\\map_info.json','r') as file:
       crypto_map = json.load(file)
    data =  crypto_map['data']
    ids= [x['id'] for x in data]
    ids_str = ','.join([str(i) for i in ids])
    params = {'id':ids_str}
    call_api('info',injected = params, use_base_param=False)
