import sqlite3
import sys
import json
from urlparse import urlparse
from automation.utilities.Cookie import SmartCookie

data_directory = '/home/openwpm/'

def dump_crawl(cid, curr):
    curr.execute('''SELECT DISTINCT url
    FROM http_requests
    WHERE crawl_id = ?  AND is_full_page = 1 AND is_third_party_window = 0
    AND content_policy_type = 6''', (cid,))
    pages = set([row[0].split('?')[0] for row in curr.fetchall()])
    with open(data_directory + 'data/pages_{}.txt'.format(cid), 'w') as fp:
        for page in pages:
            fp.write(page + '\n')

    curr.execute('''
    SELECT
        url,
        method,
        referrer,
        headers,
        content_policy_type,
        post_body,
        time_stamp,
        site_url,
        top_level_url,
        id
    FROM http_requests
    JOIN site_visits ON site_visits.visit_id = http_requests.visit_id AND site_visits.crawl_id = http_requests.crawl_id
    WHERE http_requests.crawl_id = ?
    ''', (cid, ))
    with open(data_directory + 'data/requests_{}.txt'.format(cid), 'w') as fp:
        for row in curr.fetchall():
            url_parts = urlparse(row[0])
            headers = json.loads(row[3])
            cookie = []
            for header in headers:
                if header[0] == 'Cookie':
                    sc = SmartCookie()
                    sc.load(str(header[1]))
                    for key in sc:
                        cookie.append([key, sc[key].value])
            request = {
                'url': row[0],
                'method': row[1],
                'referrer': row[2],
                'req_headers': headers,
                'type': row[4],
                'text': row[5],
                'ts': row[6],
                'visit_url': row[7],
                'top_level_url': row[8],
                'rid': row[9],
                'req_cookies': cookie,
                'host': url_parts.netloc,
                'path': url_parts.path,
                'scheme': url_parts.scheme
            }
            fp.write(json.dumps(request) + '\n')

if __name__ == '__main__':
    run_id = int(sys.argv[1])

    db = sqlite3.connect(data_directory + 'crawl-data.sqlite')
    curr = db.cursor()

    curr.execute('SELECT crawl_id FROM crawl')
    for cid, in curr.fetchall():
        print 'dump crawl', cid
        dump_crawl(cid, curr)
