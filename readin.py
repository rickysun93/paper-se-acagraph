import pymysql
import json
import re


def readin():
    db = pymysql.connect("localhost", "user", "incongruous", "paperse")
    cursor = db.cursor()

    i = 0
    for line in open("/root/data/aca-graph/aminer/aminer_papers_0.txt", 'r', encoding='utf-8').readlines():
        if i < 10000:
            jline = json.loads(line)
            if jline.get('lang') is None or jline['lang'] != "en":
                continue
            if jline.get('authors') is None or jline['authors'][0]['name'] == "":
                continue
            if jline.get('abstract') is None or jline['abstract'] == "":
                continue
            jline['authorsid'] = []
            for auth in jline['authors']:
                na = n_dis(db, cursor, auth)
                jline['authorsid'].append(na)
            savein(db, cursor, jline)
            i = i+1

    db.close()


def n_dis(db, cursor, auth):
    if 'org' not in auth:
        auth['org'] = ""
    name_low = auth['name'].lower()
    name_low = re.sub('[-.]', '', name_low)
    sql = "SELECT * FROM Author WHERE name_lower = '%s'" % name_low
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            if row[3].lower() == auth['org'].lower():
                return row[0]
    except:
        pass
    space = name_low.rfind(' ')
    if space > 0:
        name_ot = name_low[space+1:] + ' ' + name_low[0:space]
        sql = "SELECT * FROM Author WHERE name_lower = '%s'" % name_ot
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                if row[3].lower() == auth['org'].lower():
                    return row[0]
        except:
            pass
    sql = """INSERT INTO Author(name, name_lower, org)
          VALUES ('%s', '%s', '%s')""" % \
        (auth['name'], name_low, auth['org'])
    try:
        cursor.execute(sql)
        nid = db.insert_id()
        db.commit()
        return nid
    except:
        db.rollback()


def savein(db, cursor, jline):
    if 'doc_type' not in jline:
        jline['doc_type'] = ""
    if 'fos' not in jline:
        jline['fos'] = []
    if 'isbn' not in jline:
        jline['isbn'] = ""
    if 'keywords' not in jline:
        jline['keywords'] = []
    if 'n_citation' not in jline:
        jline['n_citation'] = 0
    if 'pdf' not in jline:
        jline['pdf'] = ""
    if 'publisher' not in jline:
        jline['publisher'] = ""
    if 'references' not in jline:
        jline['references'] = []
    if 'title' not in jline:
        jline['title'] = ""
    if 'url' not in jline:
        jline['url'] = []
    if 'vuene' not in jline:
        jline['vuene'] = ""
    if 'year' not in jline:
        jline['year'] = 0
    sql = """INSERT INTO Paper(abs, authors, authorsid, doctype, fos, isbn, keywords, ncite, 
                oriid, pdf, publisher, refs, title, url, vuene, year)
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', 
                '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d')""" % \
          (jline['abstract'], json.dumps(jline['authors']), json.dumps(jline['authorsid']), jline['doc_type'],
           json.dumps(jline['fos']), jline['isbn'], json.dumps(jline['keywords']), jline['n_citation'],
           jline['id'], jline['pdf'], jline['publisher'], json.dumps(jline['references']),
           jline['title'], json.dumps(jline['url']), jline['vuene'], jline['year'])
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
