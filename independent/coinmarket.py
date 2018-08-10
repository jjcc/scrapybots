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
    """
    asynchronized process to get detail information about a list of coins
    :param mylist: list of ids (or symbols,names but not relialbe
    :return: the scraped coin info
    """
    count  = 0
    detail = []
    #mylist = ['BTC',"ETH","XRP",'BCH','EOS','XLM','LTC','ADA','USDT','MIOTA']
    async with AsyncPymarketcap() as apym:
        async for currency in apym.every_currency(mylist):
            if count > 100:
                break
            #print(currency)
            #print(",")
            count +=1
            detail.append(currency)
    return detail

def detailresult(mylist):
    '''
    call the async method getdetail to get all results
    :param mylist:
    :return:
    '''
    loop = asyncio.get_event_loop()
    all = loop.run_until_complete(getdetail(mylist))
    return all

def save_coin():

    INCLUDE_BASIC = True
    cmc = Pymarketcap()
    # Get scrapedinfo currencies ranked by volume
    currencies = cmc.ticker()
    num = currencies['metadata']['num_cryptocurrencies']
    data = currencies['data']
    #symbols is not good now. Use name instead
    names = []
    ids = []
    #with some cheating: for special cases use symbols
    for id, info in data.items():
        # special = {'IOTA’：‘MIOTA','TRON':'TRX','NEM':'XEM','ODEM':'ODE','ICON':'ICX'}
        # if info['name'] in ['IOTA','TRON','NEM','ODEM','ICON']:
        #    info['name'] = special[info['name']]
        #names.append(info['name'])
        ids.append(info['id'])

    #save list data to a file
    save_file(data)

    if not INCLUDE_BASIC:
        return

    #use scrap to get more details
    scrapedinfo = detailresult(ids)

    scrapedinfo.sort(key = lambda a: a['rank'])

    #Now, play with scrapedinfo:
    #[i['source_code'] if i['source_code'] is not None else "##NONE###" for i in scrapedinfo]
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

    #[i['chats'][0] if len(i['chats']) > 0 else "##NONE###" for i in scrapedinfo]
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

    engine = create_engine('sqlite:///bigdata2.db')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    for index, detail in enumerate(scrapedinfo):
        id = detail['id']
        if str(id) in data:
            datainfo = data[str(id)]
        else:
            print(str(id))

    #for index, row in enumerate(datain):
        #assert (row['id'] == scrapedinfo[index]['id'])
        #TODO: assert failed at 42
        record = {}
        for k,v in detail.items():
            if k in ['webs', 'explorers', 'message_boards', 'chats']:
                vin = ",".join(v)
                record[k] = vin
            elif k in ['source_code','mineable', 'announcement','id','name','symbol','website_slug']:
                record[k] = v
        #get existing ids from DB so there will be no conflicts
        dbids = [id[0] for id in  session.query(CoinBasic.id).all()]

        crypto = CoinBasic()
        #Go through each column
        for k,v in record.items():
            if k in ["id","name","symbol","website_slug","webs","explorers","message_boards","chats","source_code","mineable","announcement"]:
                setattr(crypto, k, v)

        #insert a record
        if crypto.id in dbids:
            pass #skip if exists, maybe update in future
        else:
            session.add(crypto)
            session.commit()
        pass



    print(currencies)


def save_file(data):
    file = "marketcap.csv"
    datain = []
    with open(file, 'w') as outfile:
        line = "id,name,symbol,website_slug,rank,circulating,total,max,price,vaolume_24h,market,percent_change_1h,percent_change_24h,percent_change_7d,last_update\n"
        outfile.write(line)
        for id, info in data.items():
            # for pd
            row = {}
            # print("###%s"%info['symbol'])
            line = ""
            for key, value in info.items():
                if key != "quotes":
                    # print("%s:%s"%(key, value))
                    line = line + str(value) + ","
                    row[key] = value
                else:
                    # print("market:%s"%value["USD"]["market_cap"])
                    quote = value["USD"]
                    for q, qv in quote.items():
                        line = line + str(qv) + ","
                        row[q] = qv
            outfile.write(line + "\n")
            datain.append(row)
    df = pd.DataFrame(datain)
    df["per"] = df['market_cap'] * 100 / df['market_cap'].sum()
    # subtotal
    subtotal = 0
    for k, v in df.iterrows():
        subtotal += v['per']
        # print('per:' + str(v['per']) + ",assumulate:" + str(subtotal))
    symbols = df["symbol"].tolist()


if __name__ == "__main__":
    save_coin()
