'''
Created on 2018-03-06
@author: jjccforth
'''
import pickle
from dateutil import parser as dparser

def calculate(list):
    #list = pickle.load(open("datan.pkl", "rb"))
    #list = pickle.load(open("generalbot/datan.pkl", "rb")) #if run with vscode open folder"SPCAPYBOT"
    metainfo = None
    for d in list:
        if not 'created_at' in d.keys():
            metainfo = d
            list.remove(d)
            continue
        d['created_at'] = dparser.parse(d['created_at'])
        vote  = 0 if  d['vote'] == u'\u2022' else d['vote']
        #print vote ,d['created_at']
    list0 =  list
    list_s = list.sort(key=lambda item:item['created_at'], reverse=True)
    #print "$$$$$$$$$$$$$\n"
    count  = 0
    dt_deltas = [0]
    dt_prev = None
    sec_in_hour = 3600
    
    sum_delta = 0
    sum_comments = 0
    for d in list:
        if count > 0:
            dt_delta = dt_prev - d['created_at']
            delta_as_day = dt_delta.total_seconds()/sec_in_hour#sec_in_day
            dt_deltas.append(delta_as_day)
            sum_delta += delta_as_day

        dt_prev = d['created_at']
        comments_no = d['comments'].split(' ')[0]
        if comments_no == "comment":
            comments_no = 0
        vote = d['vote'] if d['vote'] != u'\u2022' else 0 #"."
        #print vote ,d['created_at'],comments_no,dt_deltas[count]
        count += 1
        #get stats
        sum_comments += int(comments_no)

    #print "stats:total delta:%d, total comments:%d,count:%d"%(sum_delta,sum_comments,count)

    meta  = [ metainfo[k] for k in metainfo]
    #print "meta:%s"%".".join(meta)
    #dtdelta = dt2 - dt1
    #dtdelta.total_seconds()
    return (sum_delta,sum_comments,count,meta[1],meta[0])

if  __name__ =='__main__':

    data = pickle.load(open("datan.pkl", "rb"))
    for k, list in data.items():
        print ("############%s"%k)
        metrices = calculate(list)
        print ("total delta:%d, total comments:%d,count:%d, subscribers:%s,online:%s\n"%metrices)
        #print