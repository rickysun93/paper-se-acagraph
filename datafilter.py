import pymongo
import json


def datafilter(ip="localhost", port=27017, dbname="papertest2"):
    conn = pymongo.MongoClient(ip, port)
    db = conn[dbname]
    mpaper = db.mPaper
    ids = {}
    i = 0
    for line in mpaper.find():
        ids[line['oriid']] = 1
    print("ok")
    for line in mpaper.find():
        refs = json.loads(line['refs'])
        nrefs = []
        for ref in refs:
            if ref in ids:
                nrefs.append(ref)
        line['refs'] = json.dumps(nrefs)
        mpaper.update_one({'_id': line['_id']}, {'$set': line})
        i += 1
        if i%1000 == 0:
            print(str(i))


def test():
    print('test')
