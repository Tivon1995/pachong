import requests
import traceback
from retrying import retry
from lxml import etree
import re
import time
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning	
#关闭安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# pip3 install retrying
# pip3 install requests
# pip3 install lxml
# 安装以上依赖，运行即可

def openfile():
    arr = []
    f = open(file_name, 'r')
    for line in f.readlines():
        arr.append(line.strip('\n'))
    f.close
    print("检测到"+ str(len(arr)) + "个地址，开始运行~！")
    for i in range(len(arr)):
        print("正在访问第"+str(i+1)+"/"+str(len(arr))+"个地址~")
        try:
            getlist(arr[i], 1)
        except:
            print("当前地址不是gitlab页，不存在gitlab仓库")

# 抓取项目仓库ALL下所有项目链接
def getlist(url, n):
    # print(url + "/explore/projects?non_archived=true&sort=name_asc&page="+str(n))
    r = My_Request_Get1(url + "/explore/projects?non_archived=true&sort=name_asc&page="+str(n))
    print(r.status_code)
    if(r.status_code != 200):
        print("网页请求失败！！！")
    else:
        tree = etree.HTML(r.text)
        urllist=tree.xpath('//a[@class="text-plain"]/@href')
        if len(urllist) < 20:
            print("仓库剩1页,发现"+str(len(urllist))+"个项目")
            schflag(url, urllist)
            # time.sleep(2)
            return
        print("仓库存在多页,开始抓取第"+str(n)+"页")
        schflag(url, urllist)
        # time.sleep(2)
        n = n + 1
        getlist(url, n)

# 抓取详情页flag(名字，简介，.zip下载链接)
def schflag(url, urllist):
    doc = open(file_name[:-4]+"_end.txt", "a+",encoding="utf-8") # 打开要写入的文件
    for i in range(len(urllist)):
        try:
            r2 = My_Request_Get2(url + str(urllist[i]))
            # print(r2.status_code)
            tree = etree.HTML(r2.text)
            flag_name=tree.xpath('//div[@class="sidebar-context-title"]/text()')[0] # 1.获取名字
            list_dir=tree.xpath('//p//text()')  # 2.获取项目简介
            flag_dir= "NULL"
            if(len(list_dir) >= 1):
                flag_dir = str(list_dir[0])
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
            time.sleep(0.2)
        except:
            print("当前flag抓取失败(项目可能为空)，抓取下一个~")
    doc.close
    print("当前页flag写入完毕")

#------------------------------------------------------------------------
# 自定义requests方法
# retry修饰器
# stop_max_attempt_number  最多失败重连次数，默认为5次
# verify=False  取消证书校验
def _result(result):
    return result is None
# 最多失败重连5次    
@retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=2000, retry_on_result=_result)
def My_Request_Get2(url):
        response = requests.get(url, timeout=6, verify=False)
        if response.status_code != 200:
            raise requests.RequestException('my_request_get error!!!!')
        return response

# 最多失败重连3次
@retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=2000, retry_on_result=_result)
def My_Request_Get1(url):
    response = requests.get(url, timeout=6, verify=False)
    return response
#------------------------------------------------------------------------

# 入口函数
if __name__ == "__main__":
    # file_name=input("Please enter the target file name(eg: 1.txt): \n")
    file_name=input("请输入存有链接的txt文件名(例如: 1.txt): \n")
    openfile()
    print("爬行结束，打开\""+file_name+"\"文件查看结果吧~！")
    # getlist("https://144.76.232.230")  #该地址有1页14个项目
    # getlist("https://159.93.223.249")  #该地址有n页gitlab仓库