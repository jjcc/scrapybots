'''
Created on 2018-03-06
@author: jjccforth
'''
import pickle
import types
from dateutil import parser as dparser
import os

def main():
    #list = pickle.load(open("data.pkl", "rb"))
    list = pickle.load(open("generalbot/data.pkl", "rb")) #if run with vscode open folder"SPCAPYBOT"
    for d in list:
        d['created_at'] = dparser.parse(d['created_at'])
        if  d['vote'] == u'\u2022':
            print ".",d['created_at']
        else:
            print d['vote'],d['created_at']
#    print type(list)
    #print list['vote'],list['created_at']
    list0 =  list
    list_s = list.sort(key=lambda item:item['created_at'], reverse=True)
    print "$$$$$$$$$$$$$\n"
    count  = 0
    dt_deltas = [-1]
    dt_prev = None
    sec_in_hour = 3600
    for d in list:
        if count > 0:
            dt_delta = dt_prev - d['created_at']
            delta_as_day = dt_delta.total_seconds()/sec_in_hour#sec_in_day
            dt_deltas.append(delta_as_day)

        dt_prev = d['created_at']
        comments_no = d['comments'].split(' ')[0]
        if comments_no == "comment":
            comments_no = 0
        vote = d['vote'] if d['vote'] != u'\u2022' else "."
        print vote ,d['created_at'],comments_no,dt_deltas[count]
        count += 1

    #dtdelta = dt2 - dt1
    #dtdelta.total_seconds()

if  __name__ =='__main__':
    main()