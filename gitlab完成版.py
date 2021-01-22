import requests
import traceback
from retrying import retry
from lxml import etree
import re
import time
import random
import threadpool

# pip3 install retrying
# pip3 install requests
# pip3 install lxml
# pip3 install threadpool
# 安装以上依赖，运行即可


from requests.packages.urllib3.exceptions import InsecureRequestWarning	
#关闭安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def _result(result):
    return result is None
# 最多失败重连5次    
@retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=2000, retry_on_result=_result)
def My_Request_Get(url):
        response = requests.get(url, timeout=6, verify=False)
        if response.status_code != 200:
            raise requests.RequestException('my_request_get error!!!!')
        return response


def getlist(url, n):
    try:
        r = requests.get(url + "/explore/projects?non_archived=true&sort=name_asc&page="+str(n), timeout=3,verify=False)
    except:
        print("当前地址无法连接,请求超时~")
        return
    print(r.status_code,",",url)
    if(r.status_code != 200):
        print(r.status_code,",","网页请求失败！！！")
    else:
        # print(r.status_code)
        tree = etree.HTML(r.text)
        urllist=tree.xpath('//a[@class="text-plain"]/@href')
        if len(urllist) < 20:
            print("仓库剩1页,发现"+str(len(urllist))+"个项目")
            schflag(url, urllist)
            # time.sleep(2)
            print("抓取结束")
            return
        print("仓库存在多页,开始抓取第"+str(n)+"页")
        schflag(url, urllist)
        # time.sleep(2)
        print("抓取结束")
        n = n + 1
        getlist(url, n)

def schflag(url, urllist):
    doc = open(file_name[:-4]+"_end.txt", "a+",encoding="utf-8") # 打开要写入的文件
    for i in range(len(urllist)):
        try:
            r2 = My_Request_Get(url + str(urllist[i]))
            # print(r2.status_code)
            tree = etree.HTML(r2.text)
            flag_name=tree.xpath('//div[@class="sidebar-context-title"]/text()')[0] # 1.获取名字
            list_dir=tree.xpath('//p//text()')  # 2.获取项目简介
            flag_dir= "NULL"
            if(len(list_dir) >= 1):
                flag_dir = str(list_dir[0]).replace("\n", "")   # 去除项目简介中的换行符
            else:
                flag_dir = "NULL"
            flag_link = "NULL"
            list_link=tree.xpath('//@href')   # 3.获取.zip下载链接
            for j in list_link:
                if str(j.strip())[-4:] == ".zip":
                    flag_link =url + str(j.strip())
            end_str = str(flag_name).strip() + "," + flag_dir.strip() + "," + flag_link
            doc.write(end_str+"\n")
            print("正在抓取第" + str(i+1)+"/"+str(len(urllist))+"个标签~")
            time.sleep(0.2) # 设置延时，避免访问过于频繁
        except:
            print("当前flag抓取失败(项目可能为空)，抓取下一个~")
    doc.close
    print("当前页flag写入完毕")
    
def main():
    tmp_arr = []
    arr = []
    f = open(file_name, 'r')
    for line in f.readlines():
        tmp_arr.append(line.strip('\n'))
    f.close
    # print(tmp_arr)
    for i in range(len(tmp_arr)):
        # print(type((tmp_arr[i],i)))
        tmp = [tmp_arr[i],1]
        arr.append((tmp, None))
    del tmp_arr
    print("检测到"+str(len(arr))+"个地址,开始爬取~")

    pool = threadpool.ThreadPool(20) #建立线程池  开启20个线程

    req = threadpool.makeRequests(getlist,arr)  #提交N个任务到线程池

    for r in req:#开始执行任务
        pool.putRequest(r)#提交  
    pool.wait()#等待完成   

if __name__ == "__main__":
    print("爬虫启动,默认线程20")
    file_name=input("请输入存有gitlab链接的txt文件名(例如: 1.txt): \n")
    main()
    print("爬行结束，快打开\""+file_name[:-4]+"_end.txt"+"\"文件查看爬取结果吧~！")
