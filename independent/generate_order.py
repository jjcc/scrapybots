import pandas as pd
import json
import re
import datetime
import sqlite3
from coinscrap_pro import get_map_dict,  get_metainfo_dict, call_api



def load_json(file_name):
    with open(f'data/{file_name}','r') as f:
        data = json.load(f)
    return data

list = ['21-02-13','21-02-15','21-02-16','21-02-17']

def generate_info(start = 0 , limit=30):
    #dlist = []
    output = {}
    for i in range(4):
        file_name = f'map_20{list[i]}_info.json'
        d = load_json(file_name)['data']
        #dlist.append(d)
        curr_data=[]
        for itoken, v in enumerate(d):
            if itoken < start:
                continue
            if itoken - start >= limit:
                break
            rank = v['rank']
            name = v['name']
            symbol = v['symbol']
            curr_data.append({'name':name, 'rank':rank,'min':1,'max':rank,'symbol':symbol,'extra':{}})
        output[list[i]] = curr_data
    return output 


if __name__ == '__main__':
    start = 51
    limit = 30
    result = generate_info(start = start,limit=limit)
    with open(f'data/orderchart_s{start}_l{limit}.json','w') as fo:
        json.dump(result, fo)