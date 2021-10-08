#!/usr/bin/python3
# by: s1g0day,tivon
'''
作用：用于自动提取vulbox公益SRC域名,已经剔除重复和空值，并直接提取跟域名
注意：若vulbox官方填写域名错误,可能会被自动剔除掉
      如：new.siemens.comcnzh.html实际域名为new.siemens.com,但这一类的字符串就会自动被剔除掉
      其他的问题暂时没有发现
'''
import re,requests
import tldextract
requests.packages.urllib3.disable_warnings()

s = requests.Session()

head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
}
data = {
    "account": "1376682691@qq.com",
    "password": "Lulu_595272424",
    "Token": "2",
    "code": "" 
}
res = s.post("https://www.vulbox.com/login/signIn",verify=False, timeout=10, data=data, headers=head)
res1 = s.get("https://www.vulbox.com/user/submit-72", verify=False, timeout=10, headers=head)
site = re.findall(r"'url':'(.*?)','typeName'", res1.text)

list_domain = []
# print(site)

for i in site:
    domain = tldextract.extract(i).registered_domain 
    if domain and not domain in list_domain:    # 去空值 将未重复的域名添加到 list_domain 中
        list_domain.append(domain)

f = open("vulbox_gov.txt", "a+", encoding="utf-8")
g = open("vulbox_nogov.txt", "a+", encoding="utf-8")

for j in list_domain:
    if "gov.cn" in j:
        f.write(j + "\n")
    else:
        g.write(j + "\n")

f.close()
g.close()
print("完成！")