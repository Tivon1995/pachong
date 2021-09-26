import requests,time, threadpool
import random
import argparse,sys
from lxml import etree


ua_list = ['Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']

def head():
    return {'User-Agent': random.choice(ua_list)}

def subdomain():
    time.sleep(0.5)
    url = "https://rank.aizhan.com/{}".format("baidu.com/")
    try:
        res = requests.get(url, headers=head(), verify=False, timeout=10)
    except:
        pass
    print(res.status_code)
    # f = open("2.txt", "a", encoding="utf-8")
    # f.write(res.text)
    # f.close()
    subdomain = etree.HTML(res.text).xpath('//td[@class="site"]//text()')
    print(subdomain)

if __name__ == "__main__":
    subdomain()