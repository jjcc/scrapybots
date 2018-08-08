#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

'''
List:
Return most volatile parameters other than id, name, symbols, website_slug.
['id', 'name', 'symbol', 'website_slug',
 'rank', 'circulating_supply', 'total_supply', 'max_supply', 'quotes', 'last_updated']


Details:
return
[
 'circulating_supply', 'max_supply', 'total_supply',
 'webs', 'explorers', 'source_code',
 'message_boards', 'chats', 'mineable',
 'rank', 'announcement', 'id',
 'name', 'symbol', 'website_slug'
 ]
 
 among which,
 ['webs', 'explorers', 'message_boards', 'chats']
 are lists

There are some overlaps with list. Useful information left are more stable ones:
[
 'webs', 'explorers', 
 'message_boards', 'chats',
 'source_code','mineable',
 'announcement', 
 ]



'''

from pymarketcap import Pymarketcap
import asyncio
from pymarketcap import AsyncPymarketcap

async def getdetail(mylist):
    count  = 0
    detail = []
    #mylist = ['BTC',"ETH","XRP",'BCH','EOS','XLM','LTC','ADA','USDT','MIOTA']
    async with AsyncPymarketcap() as apym:
        async for currency in apym.every_currency(mylist):
            if count > 100:
                break
            print(currency)
            print(",")
            count +=1
            detail.append(currency)
    return detail

def main():
    cmc = Pymarketcap()

    # Get all currencies ranked by volume
    currencies = cmc.ticker()
    num = currencies['metadata']['num_cryptocurrencies']
    data = currencies['data']

    file = "marketcap.csv"
    datain = []
    with open(file, 'w') as outfile:
        line = "id,name,symbol,website_slug,rank,circulating,total,max,market,last_update\n"
        outfile.write(line)
        for id, info in data.items():
            # for pd
            row = {}
            print("###%s"%info['symbol'])
            line = ""
            for key,value in info.items():
                if key != "quotes":
                    #print("%s:%s"%(key, value))
                    line = line + str(value) +  ","
                    row[key] = value
                else:
                    #print("market:%s"%value["USD"]["market_cap"])
                    line = line + str(value["USD"]["market_cap"]) + ","
                    row['market_cap'] = value["USD"]["market_cap"]
            outfile.write(line + "\n")
            datain.append(row)

    df = pd.DataFrame(datain)
    df["per"] = df['market_cap'] * 100 / df['market_cap'].sum()
    #subtotal
    subtotal = 0
    for k, v in df.iterrows():
        subtotal += v['per']
        print('per:' + str(v['per']) + ",assumulate:" + str(subtotal))

    symbols = df["symbol"].tolist()

    loop = asyncio.get_event_loop()
    #mylist = ['BTC', "ETH", "XRP", 'BCH', 'EOS', 'XLM', 'LTC', 'ADA', 'USDT', 'MIOTA']
    print('[\n')
    all = loop.run_until_complete(getdetail(symbols))
    print('\n]')
    # print(df.head())
    # print(df.tail())
    #for c in currencies:
    all.sort(key = lambda a: a['rank'])
    #Now, play with all:
    #[i['source_code'] if i['source_code'] is not None else "##NONE###" for i in all]
    # return source code list
    # ['https://github.com/bitcoin/',
    #  'https://github.com/ethereum',
    #  'https://github.com/ripple',
    #  'https://github.com/bitcoincashorg/',
    #  'https://github.com/eosio',
    #  'https://github.com/stellar',
    #  'https://github.com/litecoin-project/litecoin',
    #  'https://github.com/input-output-hk/cardano-sl/',
    #  '##NONE###',
    #  'https://github.com/iotaledger',
    #  .....

    #[i['chats'][0] if len(i['chats']) > 0 else "##NONE###" for i in all]
    # return chat list, slack,gitter,telegram,slack,discord
    # ['##NONE###',
    #  'https://gitter.im/orgs/ethereum/rooms',
    #  'https://t.me/Ripple',
    #  '##NONE###',
    #  'https://t.me/joinchat/AAAAAEQbOeucnaMWN0A9dQ',
    #  'http://slack.stellar.org/',
    #  'https://telegram.me/litecoin',
    #  'https://t.me/CardanoAnnouncements',
    #  '##NONE###',
    #  'https://discord.gg/7Gu2mG5',
    #  'https://discord.gg/HW4GckH',
    #  'https://tronfoundation.slack.com',
    #  'https://telegram.me/bitmonero',
    #  '##NONE###',
    # ...

    print(currencies)

if __name__ == "__main__":
    main()
