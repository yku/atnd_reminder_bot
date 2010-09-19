# coding: utf-8
# vim: fileencoding=utf-8
import twitter
import time
import datetime
import urllib2
import xml.dom.minidom

def event_search(twitter_id):
    ret = []
    url = 'http://api.atnd.org/events/?twitter_id=%s' % twitter_id
    doc = xml.dom.minidom.parseString(urllib2.urlopen(url).read())
    results = doc.getElementsByTagName('results_returned')[0].firstChild.data
    titles = doc.getElementsByTagName('title')
    started_at = doc.getElementsByTagName('started_at')
    urls = doc.getElementsByTagName('event_url')
    for i in xrange(0, int(results)):
        title = titles[i].firstChild.data
        start = datetime.datetime(*time.strptime(started_at[i].firstChild.data, "%Y-%m-%dT%H:%M:%S+09:00")[0:6])
        url = urls[i].firstChild.data
        ret.append((title, start, url))
    return ret

api = twitter.Api(
                username='', password='',
                access_token_key='',
                access_token_secret='')
users = api.GetFollowers()

for u in users:
    res = event_search(u.screen_name)
    for r in res:
        now = datetime.datetime.now()
        if now < r[1]:
            d = r[1] - now
            mes = '@' + u.screen_name.encode('utf_8') + ' ' + r[0].encode('utf_8') + 'まであと' + str(d.days) + '日です' + " " + r[2].encode('utf_8')
            print mes
            api.PostUpdate(mes)
            time.sleep(10)

