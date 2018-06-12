from dateutil import parser
from generalbot.items import *

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

    pass