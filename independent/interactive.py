# %%
import pandas as pd
import json
import re

def get_metainfo():
    with open('data\\info_info.json','r') as fin:
        data_j = json.load(fin)

    data = data_j['data']
    df_info0 = pd.DataFrame.from_dict(data)
    df_info = df_info0.T
    return df_info

def get_mapinfo():
    with open('data\\map_info.json','r') as fin:
        data_j = json.load(fin)

    data = data_j['data']
    df_info0 = pd.DataFrame.from_dict(data)

    junk_f = [ 'is_active','first_historical_data','last_historical_data','platform','slug','name']
    for f in junk_f:
        del df_info0[f]
    return df_info0



def output():
    df_map = get_mapinfo()
    df_info = get_metainfo()
    
    pdm = pd.merge(df_map,df_info,on=['id','symbol'])
    pdm.to_csv('data\\merge_info.csv',index=False)

desc = 'Mirrored Invesco QQQ Trust (mQQQ) is a cryptocurrency and operates on the Ethereum platform. Mirrored Invesco QQQ Trust has a current supply of 13,986.610708. The last known price of Mirrored Invesco QQQ Trust is 380.57680721 USD and is down -2.73 over the last 24 hours. It is currently trading on 2 active market(s) with $163,101.15 traded over the last 24 hours. More information can be found at https://mirror.finance. '

regexes= {'supply':r'has a current supply of ([\d|,|.]+)',
           'price':r'is\s*([\d|,|.]+)\s*USD',
           'change':r'([\d|,|.]+)\s*over the', 
           'volumn':r'([\d|,|.]+)\s*traded' }
def get_num(desc, k) :
    res = re.search(regexes[k],desc)
    return res.group(1)

for k,v in regexes.items():
    print(get_num(desc,k))
    
#res1= re.search(r'has a current supply of ([\d|,|.]+)',desc)
#res2= re.search(r'is\s*([\d|,|.]+)\s*USD',desc)
#res3= re.search(r'([\d|,|.]+)\s*over the',desc)
#res4= re.search(r'([\d|,|.|+]+)\s*over the',desc)
#res4= re.search(r'([\d|,|.]+)\s*traded',desc)
pass
