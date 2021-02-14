# %%
import pandas as pd
import json
import re
import datetime
import sqlite3
from coinscrap_pro import get_map_dict,  get_metainfo_dict, call_api

def get_metainfo(data):
    df_info0 = pd.DataFrame.from_dict(data)
    df_info = df_info0.T
    return df_info

def get_mapinfo( data):
    df_info0 = pd.DataFrame.from_dict(data)

    junk_f = [ 'is_active','first_historical_data','last_historical_data','platform','slug','name']
    for f in junk_f:
        del df_info0[f]
    return df_info0


regexes= {'supply':r'has a current supply of ([\d|,|.]+)',
           'price':r'is\s*([\d|,|.]+)\s*USD',
           'change':r'([\d|,|.|-]+)\s*over the', 
           'volumn':r'([\d|,|.]+)\s*traded',
           'market':r'(\d+)\s*active' }

def get_num(desc, k) :
    res = re.search(regexes[k],desc)
    return res.group(1)


url_keys = ['website', 'twitter', 'message_board', 'chat', 'explorer', 'reddit', 'technical_doc', 'source_code', 'announcement']

def output( online = False):

    if online:
        map_dict = get_map_dict()
        info_dict = get_metainfo_dict(map_dict) #call online 
    else:
        with open('data\\info_info.json','r') as fin:
            data_j = json.load(fin)
        info_dict = data_j['data']
        with open('data\\map_info.json','r') as fin:
            data_j = json.load(fin)
        map_dict = data_j['data']
    # convert dict into df
    df_map = get_mapinfo(map_dict)
    df_info = get_metainfo(info_dict)
    
    pdm = pd.merge(df_map,df_info,on=['id','symbol'])
    
    # added extra column
    for k in regexes.keys():
        pdm[k] = 0
    for k in url_keys:
        pdm[k] = ''

    for index, row in pdm.iterrows():
        desc = row['description']

        for k,v in regexes.items():
            value = get_num(desc, k)
            pdm.loc[index,k] = value
            #row[k] = value
            #print(get_num(desc,k))

        urls =  row['urls']    
        for k in url_keys:
            value =  urls.get(k) 
            if len(value) > 0:
                val2 = [ r.replace('\r\n',' ') for r in value]
                pdm.loc[index,k] = ','.join(val2)
               # pdm.loc[index, k] = value
    

    pdm.to_csv('data\\merge_info6.csv',index=False)

#desc = 'Mirrored Invesco QQQ Trust (mQQQ) is a cryptocurrency and operates on the Ethereum platform. Mirrored Invesco QQQ Trust has a current supply of 13,986.610708. The last known price of Mirrored Invesco QQQ Trust is 380.57680721 USD and is down -2.73 over the last 24 hours. It is currently trading on 2 active market(s) with $163,101.15 traded over the last 24 hours. More information can be found at https://mirror.finance. '

table_fields = ['id','symbol','name','category','slug','logo','subreddit','tag-names','twitter_username','website','message_board','chat','explorer','reddit','technical_doc','source_code','announcement']

SQL_CREATE_TABLE = '''
CREATE TABLE basic (
	id INTEGER PRIMARY KEY,
	symbol 			TEXT NOT NULL,
	name 			TEXT NOT NULL,
	category 		TEXT,
	slug			TEXT,
	logo			TEXT,
	subreddit		TEXT,
	tag_names		TEXT, 
	twitter_username TEXT,
	website 		TEXT,
	message_board	TEXT,
	chat			TEXT,
	explorer		TEXT,
	reddit			TEXT,
	technical_doc	TEXT,
	source_code		TEXT,
	announcement	TEXT
)
'''

unwanted = ['rank', 'description', 'notice', 'tags', 'tag-groups', 'urls', 'platform', 
            'date_added', 'is_hidden', 'supply', 'price', 'change', 'volumn', 'market', 'twitter','logo']
            #'logo' can be deducted. put into unwanted list to reduce the size of table


def load_basic_to_db(df, connection = None):
    '''
    load data into a table with only static information
    '''
    today = datetime.datetime.today()
    if connection is None:
        conn = sqlite3.connect('data\\crypto.db')
    else:
        conn = connection

    c = conn.cursor()
    for k in unwanted:
        del df[k]

    df.to_sql('basic1', conn,index=True)
    return df

  
    #conn.commit()
    #c.close()

def compare_id(df_new, conn):
    dff = pd.read_sql('select id from basic', conn)
    old_ids = dff['id'].to_list()
    new_ids = df_new['id'].to_list()
    diff = [ id for id in new_ids if not id in old_ids ]
    return diff # the id list not in old list

table_fields = ['id','symbol','name','category','slug','subreddit','tag-names','twitter_username','website','message_board','chat','explorer','reddit','technical_doc','source_code','announcement']
def insert_new(df,id_list, conn, append=False):
    '''
    Insert new id in case there are other coins get into the 2000 list
    '''
    if append:
        del table_fields[0] # remove 'id' because it's index of data frame
    df_new= df.loc[id_list,table_fields]
    c = conn.cursor()
    df_new.to_sql('basic', conn,if_exists='append')

def test_insert_new():
    df = pd.read_csv('data\merge_info5.csv',index_col='id')
    ids = [5115,2400]
    conn = sqlite3.connect('data\\crypto.db')
    insert_new(df,ids,conn,append=True)

if __name__ == '__main__':
    #collect data from online
    #output(online=True)
    #load data into db
    df = pd.read_csv('data\merge_info6.csv',index_col='id')
    df_reduced = load_basic_to_db(df)
    print(df.head())
    
    pass

    
