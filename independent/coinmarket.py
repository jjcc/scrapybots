#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine
import json
from misc.dbcreate import Base
from sqlalchemy.orm import *
from pymarketcap import Pymarketcap
import asyncio
from pymarketcap import AsyncPymarketcap


from misc.dbcreate import CoinBasic
'''
List:
Return most volatile parameters other than id, name, symbols, website_slug.
['id', 'name', 'symbol', 'website_slug',
 'rank', 'circulating_supply', 'total_supply', 'max_supply', 'quotes', 'last_updated']
The 'quotes' is a dictionary like:
{
    'USD': 
    {   
        'price': 13.7305664566,
        'volume_24h': 720701.786268124,
        'market_cap': 73527796.0,
        'percent_change_1h': -0.36,
        'percent_change_24h': -1.41,
        'percent_change_7d': -10.85} 
    },
    'last_updated': 1533615328
}

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


def process(file,file_amendment):
    fp = open(file,"rb")
    data = json.load(fp)
    fpa = open(file_amendment,'rb')
    data_a = json.load(fpa)

    coininfo_filtered = {}
    engine = create_engine('sqlite:///bigdata.db')


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
    INCLUDE_BASIC = True

    cmc = Pymarketcap()

    # Get all currencies ranked by volume
    currencies = cmc.ticker()
    num = currencies['metadata']['num_cryptocurrencies']
    data = currencies['data']

    file = "marketcap.csv"
    datain = []
    with open(file, 'w') as outfile:
        line = "id,name,symbol,website_slug,rank,circulating,total,max,price,vaolume_24h,market,percent_change_1h,percent_change_24h,percent_change_7d,last_update\n"
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
                    quote = value["USD"]
                    for q, qv in quote.items():
                        line = line + str(qv) + ","
                        row[q] = qv
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
    #symbols is not good now. Use name instead
    names = []
    #with some cheating: for special cases use symbols
    for id, info in data.items():
        if info['name'] == 'IOTA':
            info['name'] = 'MIOTA'
        if info['name'] == 'TRON':
            info['name'] = 'TRX'
        if info['name'] == 'NEM':
            info['name'] = 'XEM'
        if info['name'] == 'ODEM':
            info['name'] = 'ODE'
        if info['name'] == 'ICON':
            info['name'] = 'ICX'
        names.append(info['name'])


    if not INCLUDE_BASIC:
        return

    #Basic information, need to get details
    loop = asyncio.get_event_loop()
    #mylist = ['BTC', "ETH", "XRP", 'BCH', 'EOS', 'XLM', 'LTC', 'ADA', 'USDT', 'MIOTA']
    print('[\n')
    #all = loop.run_until_complete(getdetail(symbols))
    all = loop.run_until_complete(getdetail(names))


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


    #join the array items: webs, chats, explorers,message_boards

    engine = create_engine('sqlite:///bigdata2.db')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    for index, detail in enumerate(all):
        id = detail['id']
        if str(id) in data:
            datainfo = data[str(id)]
        else:
            print(str(id))

    #for index, row in enumerate(datain):
    #    assert (row['id'] == all[index]['id'])
        #TODO: assert failed at 42
    #    id  = row['id']
    #    detail = all[index]
        record = {}
        for k,v in detail.items():
            if k in ['webs', 'explorers', 'message_boards', 'chats']:
                vin = ",".join(v)
                record[k] = vin
            elif k in ['source_code','mineable', 'announcement','id','name','symbol']:
                record[k] = v
        #Good, now insert into DB
        crypto = CoinBasic()
        #Go through each column
        for k,v in record.items():
            if k in ["id","name","symbol","website_slug","webs","explorers","message_boards","chats","source_code","mineable","announcement"]:
                setattr(crypto, k, v)
                pass
        #insert a record
        session.add(crypto)
        session.commit()
        pass
 #       for k, v in detail.items():



    print(currencies)



if __name__ == "__main__":
    main()
