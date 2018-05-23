import pymongo
import json
from nltk import tokenize
import stop_words


def datafilter(ip="localhost", port=27017, dbname="papertest2"):
    conn = pymongo.MongoClient(ip, port)
    db = conn[dbname]
    mpaper = db.mPaper
    ids = {}
    dels = []
    i = 0
    pattern = r"""(?x)                   # set flag to allow verbose regexps
                  (?:[A-Z]\.)+           # abbreviations, e.g. U.S.A.
                  |\d+(?:\.\d+)?%?       # numbers, incl. currency and percentages
                  |\w+(?:[-']\w+)*       # words w/ optional internal hyphens/apostrophe
                """
    tokenizer = tokenize.RegexpTokenizer(pattern)
    en_stop = stop_words.get_stop_words('en')  # stop words
    for line in mpaper.find():
        tokens = tokenizer.tokenize(line['abs'])  # 分词
        low_tokens = [w.lower() for w in tokens]  # 转小写
        stopped_tokens = [w for w in low_tokens if w not in en_stop]  # 去除停用词
        if stopped_tokens:
            ids[line['oriid']] = 1
        else:
            dels.append(line['_id'])
    print("ok")
    for d in dels:
        mpaper.delete_one({'_id': d})
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
        if i % 1000 == 0:
            print(str(i))


def test():
    print('test')
