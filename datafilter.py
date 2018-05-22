import pymongo
import json


def datafilter(ip="localhost", port=27017, dbname="papertest"):
    conn = pymongo.MongoClient(ip, port)
    db = conn[dbname]
    mpaper = db.mPaper
    for line in mpaper.find():
        refs = json.loads(line['refs'])
        nrefs = []
        for ref in refs:
            if mpaper.find_one({'oriid': ref}) is not None:
                nrefs.append(ref)
        line['refs'] = json.dumps(nrefs)
        mpaper.update_one({'oriid': line['oriid']}, {'$set': line})


def test():
    print('test')
