# -*- coding:utf-8 -*-
import requests
from lxml import etree
import base64
import re
import time

# 使用前请填入cookie，非fofa会员cookie只能爬取前五页
cookie = '672af411b4248f983f9d33c29cfef739'


def logo():
    print('''
                
            
             /$$$$$$$$ /$$$$$$  /$$$$$$$$ /$$$$$$                                   
            | $$_____//$$__  $$| $$_____//$$__  $$                                  
            | $$     | $$  \ $$| $$     | $$  \ $$                                  
            | $$$$$  | $$  | $$| $$$$$  | $$$$$$$$                                  
            | $$__/  | $$  | $$| $$__/  | $$__  $$                                  
            | $$     | $$  | $$| $$     | $$  | $$                                  
            | $$     |  $$$$$$/| $$     | $$  | $$                                  
            |__/      \______/ |__/     |__/  |__/                                  
                                                                                    
                                                                                    
                                                                                    
                                /$$$$$$            /$$       /$$                    
                               /$$__  $$          |__/      | $$                    
                              | $$  \__/  /$$$$$$  /$$  /$$$$$$$  /$$$$$$   /$$$$$$ 
                              |  $$$$$$  /$$__  $$| $$ /$$__  $$ /$$__  $$ /$$__  $$
                               \____  $$| $$  \ $$| $$| $$  | $$| $$$$$$$$| $$  \__/
                               /$$  \ $$| $$  | $$| $$| $$  | $$| $$_____/| $$      
                              |  $$$$$$/| $$$$$$$/| $$|  $$$$$$$|  $$$$$$$| $$      
                               \______/ | $$____/ |__/ \_______/ \_______/|__/      
                                        | $$                                        
                                        | $$                                        
                                        |__/                                        
                                
                                                                                version:1.0
    ''')


def spider():
    header = {
        "Connection": "keep-alive",
        "Cookie": "_fofapro_ars_session=" + cookie,
    }
    search = input('please input your key: \n')
    searchbs64 = (str(base64.b64encode(search.encode('utf-8')), 'utf-8'))
    print("spider website is :https://fofa.so/result?&qbase64=" + searchbs64)
    html = requests.get(url="https://fofa.so/result?&qbase64=" + searchbs64, headers=header).text
    pagenum = re.findall('>(\d*)</a> <a class="next_page" rel="next"', html)
    print("have page: "+pagenum[0])
    stop_page=input("please input stop page: \n")
    #print(stop_page)
    # file_name=input("please input output file name(eg: 1.txt): \n")
    file_name=input("请输入你想要输出的txt文件名(例如: 1.txt): \n")
    doc = open(file_name, "a+")
    for i in range(1,int(pagenum[0])):
        print("Now write " + str(i) + " page")
        pageurl = requests.get('https://fofa.so/result?page=' + str(i) + '&qbase64=' + searchbs64, headers=header)
        tree = etree.HTML(pageurl.text)
        urllist=tree.xpath('//div[@class="re-domain"]//text()')
        urllist = list(set(urllist))
        for j in urllist:
            if(j.strip() != ""):
                if((j.strip())[:5] != "https"):
                    doc.write("https://"+j.strip()+"\n")
                else:
                    doc.write(j.strip()+"\n")
        if i==int(stop_page):
            break
        time.sleep(5)
    doc.close()
    print("OK,Spider is End .")

def start():
    print("Hello!My name is Spring bird.First you should make sure _fofapro_ars_session!!!")
    print("And time sleep is 5s")

def main():
    logo()
    start()
    spider()


if __name__ == '__main__':
    main()
