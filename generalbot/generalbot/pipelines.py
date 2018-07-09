# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import pickle
from collections import OrderedDict
from misc.log import *
from misc.metrices import *
import json

class RedditbotPipeline(object):
    def __init__(self):
        self.file = codecs.open('data_utf8n.cvs', 'w', encoding='utf-8')
        self.pickle = open("datan.pkl","wb")
        #self.data = []
        self.data2 = {}
        info(">>>RedditBotPipeline Starting")

    def process_item(self, item, spider):
        line =  [ item['item'][v] for v in item['item']]
        l = ",".join(line) +'\n'#json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        ll = item['url'] + "," + l
        #self.file.write(ll)
        if item['url'] not in self.data2:
            self.data2[item['url']] = []
        self.data2[item['url']].append(item['item'])

        #self.data.append(item)
        return item

    def close_spider(self, spider):
        #for kurl,v in self.data2.iteritems():
        for kurl, v in self.data2.items():
            for item in v:
                line = [item[i] for i in item ]
                l = ",".join(line)
                ll = kurl + " ," + l + "\n"
                self.file.write(ll)

            print ("############%s"%kurl)
            #metrices = calculate(v)
            #print ("total delta:%d, total comments:%d,count:%d, subscribers:%s,online:%s\n"%metrices)
        self.file.close()

        #copy from the test code in metrics
        engine = create_engine('sqlite:///bigdata.db')
        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        data = self.data2 #pickle.load(open("datan.pkl", "rb"))
        for k, list in data.items():
            reddit = RedditInfo(url=k)

            print("############%s" % k)
            metrices = calculate0(list)
            print("total delta:%d, total comments:%d,count:%d, online:%s,subscribers:%s\n" % (metrices[0:5]))
            reddit.online = metrices[3]
            reddit.subscribers = metrices[4]

            timinginfo = metrices[5]
            commentinfo = metrices[6]
            voteinfo = metrices[7]
            print("better data")
            info = [timinginfo, commentinfo, voteinfo]
            strinfo = ['timing', 'comment', 'vote']
            count = 0
            for i in info:
                df = pd.DataFrame(i)
                print(strinfo[count])
                print("count:%d,mean:%f, std:%f" % (df.count(), df.mean(), df.std()))
                if (count == 0):
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
            # df.mean()

        pickle.dump(self.data2,self.pickle)
        self.pickle.close()

        info("<<<GeneralPipeline Closing")

class CryptobotPipeline(object):
    OUTPUT = "output/"
    PKL = OUTPUT + "crypton.pkl"
    FILE_ALLONCE = OUTPUT + "crypto_utf8_allonce.json"
    def __init__(self):
        self.pickle = open(self.PKL,"wb")
        self.data = {}
        info(">>>CryptoPipeline Starting")

    def process_item(self, item, spider):
        if item['Rank'] not in spider.data.keys():
            spider.data[item['Rank']] = {}
        spider.data[item['Rank']]['coininfo'] = item
        data = json.dumps(OrderedDict(item),sort_keys=True, indent=4) + ",\n"
        return data

    def close_spider(self, spider):

        # pickle.dump(self.data2,self.pickle)
        #ranklist = spider.data2.keys()
        #ranklist.sort()
        ranklist = sorted(spider.data)
        #add missing info
        iconinfox = { } # missing extra info
        for rank in ranklist:
            c = spider.data[rank]
            coininfo = c['coininfo']
            rank = coininfo['Rank']
            #print coininfo['Name']
            if "extrainfo" in c:
                extrainfo = c['extrainfo']
                if len(extrainfo) > 0:
                    pass #print "\t",extrainfo["reddit"]
                else:
                    iconinfox[rank] ={u"Name":coininfo['Name'],u"Website":coininfo['Website']}
                    print( coininfo['Name'],rank,coininfo['Website'])
            else:
                #print "\tno extrainfo"
                iconinfox[rank] ={u"Name":coininfo['Name'],u"Website":coininfo['Website']}
                print(coininfo['Name'],"*",rank,coininfo['Website'])


        fileOnceAtEnd  = codecs.open(self.FILE_ALLONCE, 'w', encoding='utf-8')
        fileOnceAtEnd.write("[\n")
        datax = [json.dumps(OrderedDict(spider.data[r]),sort_keys=True, indent=4) for r in ranklist]
        fileOnceAtEnd.write(",\n".join(datax))
        fileOnceAtEnd.write("]\n")
        fileOnceAtEnd.close()




        info("<<<CryptoPipeline Closing")
        self.pickle.close()
