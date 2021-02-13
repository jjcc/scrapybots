#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dotenv import load_dotenv
import os
import datetime
import sqlite3

load_dotenv()

headers = {
  'Accepts': 'application/json',
}

base_url = 'https://pro-api.coinmarketcap.com/v1/'
base_parameters = {
  'start':'1',
  'limit':'1000',
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

headers['X-CMC_PRO_API_KEY'] = os.getenv('API_KEY')
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
    data = None
    try:
      strdate = str(datetime.datetime.today())[:10]
      fname = apiname + f'_{strdate}_info.json'
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
      with open(f"data\\{fname}", "w") as data_file:
        json.dump(data, data_file, indent=2)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    return data

def get_map_dict():
    '''
    call 'map' api to get map inf
    return dictionary
    '''
    #with open('data\\map_info.json','r') as file:
    #   crypto_map = json.load(file)
    crypto_map = call_api('map',injected={"limit":1000})
    data =  crypto_map['data']
    return data

def get_metainfo_dict(data):
    '''
    call 'info' api to get meta info
    return dictionary
    '''
    ids= [x['id'] for x in data]
    ids_str = ','.join([str(i) for i in ids])
    params = {'id':ids_str}
    crypto_info = call_api('info',injected = params, use_base_param=False)
    return crypto_info['data']

def load_main_table(connection=None):
    '''
    load data into a table with only static information
    '''

    today = datetime.datetime.today()
    if connection is None:
        conn = sqlite3.connect('data\\crypto.db')
    else:
        conn = connection

    c = conn.cursor()
    ##c.execute("SELECT max(date(date)) as latest FROM class1_index;")
    ##latest_str = c.fetchone()[0]


    with open("data\\bak1\\map_info.json","r") as fin:
        dj = json.load(fin)
    data = dj['data']
    keys = ['id','name','symbol','slug','first_historical_data']
    for d in data:
        key = []
        val = []
        c.execute(
            "INSERT INTO basic([id],[name], [symbol],[slug],[first_historical_data]) values(?,?,?,?,?)",
            (d['id'], d['name'], d['symbol'], d['slug'], d['first_historical_data']))

#        for k in keys:
#            key.append(k)
#            val.append(v)
#        for i in range(4):
#            print(val[i]) 
    conn.commit()
    c.close()

def test_db(connection = None):
    if connection is None:
        conn = sqlite3.connect('data\\crypto.db')
    else:
        conn = connection

    c = conn.cursor()
    ##c.execute("SELECT max(date(date)) as latest FROM class1_index;")
    ##latest_str = c.fetchone()[0]
    c.execute("SELECT * FROM basic")
    for i in range(10):
        row = c.fetchone()
        print(f'id:{row[0]},name:{row[1]}')

if __name__ == "__main__":
    #load_main_table()
    #test_db()
    #call_api('map') # cost only 1 credit
    get_metainfo_dict(get_map_dict())