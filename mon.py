import urllib, urllib2
from lxml.html import fromstring
import datetime
import time

user_agent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)'
headers = { 'User-Agent' : user_agent }

TIMEOUT = 120
TIME_INTERVAL = 1 #In days
SLEEP_TIME = 60*60*12 #In seconds
ITEM_URL = 'http://www.amazon.com/Apple-MacBook-MD231LL-13-3-Inch-VERSION/dp/B005CWJB5G/ref=sr_1_1?ie=UTF8&qid=1345380761&sr=8-1&keywords=macbook+air'
PRICE_TAG_ID = "actualPriceValue"
LOG_FILE = "pricelog.txt"

def visit(url):
    try:
        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request, timeout = TIMEOUT)
    except Exception, detail: 
        print(str(detail) + " " + url)
        return
    return response

def parse(url):
    try:
        response = visit(url)
        page = unicode(response.read(), 'utf8', errors='ignore')
    except Exception, e:
        print(str(traceback.format_exc()))
        print(e)
        raise
    finally:
        response.close()

    doc = fromstring(page)

    price = doc.get_element_by_id(PRICE_TAG_ID).text_content()
    now = datetime.datetime.now()

    f = open(LOG_FILE, "a")
    f.write(str(now))
    f.write(price)
    f.close()
    print price

last = datetime.datetime.now()-datetime.timedelta(days=TIME_INTERVAL)

while True:
    now = datetime.datetime.now()
    #print now
    #print last
    print now - last
    if (now - last).days >= TIME_INTERVAL:
        print "Working"
        parse(ITEM_URL)
        last = now
    else:
        #print "Condition not satisfied"
        pass
    time.sleep(SLEEP_TIME)
