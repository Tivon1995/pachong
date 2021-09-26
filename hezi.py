import re

f = open("hezi.txt", "r",encoding='utf-8')
arr = re.findall(r'http(.*?)\t', f.read())
f.close()
open("heziurl.txt", 'w').close()
f = open("heziurl.txt", "a+", encoding="utf-8")
for i in arr:
    f.write(i+"\n")
f.close()
print("转换完成!")




