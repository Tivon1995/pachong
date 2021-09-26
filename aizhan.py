import requests,time, threadpool
import random
import argparse,sys
from lxml import etree
import warnings
warnings.filterwarnings('ignore')


ua_list = ['Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']

def head():
    return {'User-Agent': random.choice(ua_list)}

def Getdomain(page):
    time.sleep(0.5)
    url = "https://top.aizhan.com/top/{}/p{}.html".format(args.type, page)
    try:
        res = requests.get(url, headers=head(), verify=False, timeout=10)
    except:
        pass
    site = etree.HTML(res.text).xpath('//div[@class="text"]//em//text()')
    rank = etree.HTML(res.text).xpath('//div[@class="alexa"]//a//text()')
    # print(site)
    # print(rank)
    for i in range(len(rank)):
        if(int(rank[i]) >= 1):
            # print(site[i])
            # f.write(site[i] + "\n")
            # f.flush()
            Subdomain(site[i])

def Subdomain(site):
    time.sleep(0.5)
    url = "https://rank.aizhan.com/{}/".format(site)
    try:
        res1 = requests.get(url, headers=head(), verify=False, timeout=10)
    except:
        pass
    subdomain = etree.HTML(res1.text).xpath('//td[@class="site"]//text()')
    print(subdomain)
    if subdomain:
        for i in subdomain:
            f.write(i + "\n")
            f.flush()



def th():
    pool = threadpool.ThreadPool(args.t) #建立线程池  开启20个线程
    req = threadpool.makeRequests(Getdomain, list(range(args.s, args.e + 1)))  #提交N个任务到线程池
    for r in req:#开始执行任务
        pool.putRequest(r)#提交  
    pool.wait()#等待完成

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t",type=int,help="Thread Numbers(Default 5)",default=5)
    parser.add_argument("-s",type=int,help="Start Page(Default 1)",default=1)
    parser.add_argument("-e",type=int,help="End Page(Default 2)",default=1)
    parser.add_argument("-type",help="site type(Default t3 休闲娱乐,t25 生活服务, t90 网上购物, t31 网络科技.....)", default="t3")
    args = parser.parse_args()
    f = open("url.txt", "a+", encoding="utf-8")
    th()
    f.close()