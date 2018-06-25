from dateutil import parser
import pickle
from generalbot.items import *
from dateutil import parser as dparser

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
    # list = pickle.load(open("datan.pkl", "rb"))
    # list = pickle.load(open("generalbot/datan.pkl", "rb")) #if run with vscode open folder"SPCAPYBOT"
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
    # print "$$$$$$$$$$$$$\n"
    count = 0
    dt_deltas = [0]
    dt_prev = None
    sec_in_hour = 3600

    sum_delta = 0
    sum_comments = 0
    for d in list:
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
        # print vote ,d['created_at'],comments_no,dt_deltas[count]
        count += 1
        # get stats
        sum_comments += int(comments_no)

    # print "stats:total delta:%d, total comments:%d,count:%d"%(sum_delta,sum_comments,count)

    meta = [metainfo[k] for k in metainfo]
    # print "meta:%s"%".".join(meta)
    # dtdelta = dt2 - dt1
    # dtdelta.total_seconds()
    return (sum_delta, sum_comments, count, meta[1], meta[0])


if __name__ == '__main__':

    data = pickle.load(open("datan.pkl", "rb"))
    for k, list in data.iteritems():
        print
        "############%s" % k
        metrices = calculate(list)
        print
        "total delta:%d, total comments:%d,count:%d, subscribers:%s,online:%s\n" % metrices
        # print