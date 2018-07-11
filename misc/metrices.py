'''
Created on 2018-03-06
@author: jjccforth
'''
import pickle
#from generalbot.generalbot.items import * #Normal run
from generalbot.items import *          #run under generalbot
from dateutil import parser as dparser
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from misc.dbcreate import Topic, RedditInfo, Base

def calculate( itemlist):
    comno_list = []
    crtdt_list = []
    for item in itemlist:
        if isinstance(item, GeneralbotItem):
            comments_no = 0
            comments = item['comments']
            created_at = item['created_at']
            title = item['title']
            comments = comments.split(' ')
            if len(comments) == 2:
                comno_list.append( int ( comments[0]))
            else:
                comno_list.append(0)

            #date time
            create_dt = parser.parse(created_at)
            crtdt_list.append(create_dt)

        if isinstance(item, RedditItem):
            pass

    return

def calculate0(list):
    metainfo = None
    for d in list:
        if not 'created_at' in d.keys():
            metainfo = d
            list.remove(d)
            continue
        d['created_at'] = dparser.parse(d['created_at'])
        vote = 0 if d['vote'] == u'\u2022' else d['vote']
        # print vote ,d['created_at']
    list0 = list
    list_s = list.sort(key=lambda item: item['created_at'], reverse=True)
    count = 0
    dt_deltas = [0] #date delta list
    votes = []     #vote list
    comments = []  #comment list
    dt_prev = None
    sec_in_hour = 3600

    sum_delta = 0
    sum_comments = 0
    for d in list: # it's sorted by the ".sort" method
        if count > 0:
            dt_delta = dt_prev - d['created_at']
            delta_as_day = dt_delta.total_seconds() / sec_in_hour  # sec_in_day
            dt_deltas.append(delta_as_day)
            sum_delta += delta_as_day

        dt_prev = d['created_at']
        comments_no = d['comments'].split(' ')[0]
        if comments_no == "comment":
            comments_no = 0
        vote = d['vote'] if d['vote'] != u'\u2022' else 0  # "."
        vote_as_num = int(vote)
        votes.append(vote_as_num)
        # print vote ,d['created_at'],comments_no,dt_deltas[count]
        count += 1
        # get stats
        sum_comments += int(comments_no)
        comments.append(int(comments_no))

    # print "stats:total delta:%d, total comments:%d,count:%d"%(sum_delta,sum_comments,count)

    meta = [metainfo[k] for k in metainfo]
    # print "meta:%s"%".".join(meta)
    # dtdelta = dt2 - dt1
    # dtdelta.total_seconds()
    return (sum_delta, sum_comments, count, meta[1], meta[0],dt_deltas,comments,votes,meta)


if __name__ == '__main__':

    engine = create_engine('sqlite:///bigdata.db')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    data = pickle.load(open("datan.pkl", "rb"))
    for k, list in data.items():
        reddit = RedditInfo(url=k)

        print ("############%s" % k)
        metrices = calculate0(list)
        print ("total delta:%d, total comments:%d,count:%d, online:%s,subscribers:%s\n" % (metrices[0:5]))
        reddit.online = metrices[3]
        reddit.subscribers = metrices[4]

        timinginfo = metrices[5]
        commentinfo = metrices[6]
        voteinfo = metrices[7]
        print ("better data")
        info = [timinginfo, commentinfo,voteinfo]
        strinfo = ['timing','comment','vote']
        count = 0
        for i in info:
            df = pd.DataFrame(i)
            print (strinfo[count])
            print ("count:%d,mean:%f, std:%f"%(df.count(),df.mean(),df.std()))
            if( count == 0):
                reddit.timedelta_mean = df.mean()
                reddit.timedelta_std = df.std()
            if (count == 1):
                reddit.comment_mean = df.mean()
                reddit.comment_std = df.std()
            if (count == 2):
                reddit.vote_mean = df.mean()
                reddit.vote_std = df.std()
            count += 1

        session.add(reddit)
        session.commit()
        #df.mean()
        #df.std()]
        #etc
        # print