import json


def process(file):
    fp = open(file,"rb");
    data = json.load(fp)
    for c in data:
       coininfo = c['coininfo']
       print coininfo['Name']
       if "extrainfo" in c:
           extrainfo = c['extrainfo']
           if "reddit" in extrainfo:
               print "\t",extrainfo["reddit"]
       else:
           print "\tno extrainfo"


if __name__ == '__main__':
    process("crypto_utf8a.json")


