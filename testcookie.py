# GET https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=A7--cj3fndmszDg2uiR_E5yd@qrticket_0&uuid=AZG7lDveCg==&lang=zh_CN&scan=1527381997 HTTP/1.1

#GET https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=AypRubyfENpar1Lkn2HJLhDA@qrticket_0&uuid=gdMeV72XvQ==&lang=zh_CN&scan=1527382750 HTTP/1.1
# Host: wx2.qq.com
# Connection: keep-alive
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
# Referer: https://wx.qq.com/
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.9,en;q=0.8

cookie="RK=btz0ndMkSh; ptcz=1120e17cd9d85d47c70f81b8fe537034880d71ffeff148f7dce93b35f4636a8c; pgv_pvid=9584848604; o_cookie=1272724627; pac_uid=1_1272724627; pt2gguin=o1272724627; pgv_pvi=6202027008; webwxuvid=51f3f8655a395721855bc3affcf2b61f956cc2c978232555e298a71b293a06b91f5814620e552ab706083a7dd7a6777f; tvfe_boss_uuid=cbff0131fc4cf4ad; wxuin=2824284317"
import requests
url="https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=A7--cj3fndmszDg2uiR_E5yd@qrticket_0&uuid=AZG7lDveCg==&lang=zh_CN&scan=1527381997"
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',"Referer":"https://wx.qq.com/","Upgrade-Insecure-Requests":"1"}
cookies={}
for line in cookie.split(";"):
    name,value =line.split("=",1)
    cookies[name]=value

r3=requests.get(url,headers=headers,cookies=cookies,verify=False)
r3.encoding="utf-8"
print(r3.text)