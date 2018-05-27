import requests
import re
import time

#必须先获取uuid
c_time = int(time.time() * 1000)
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',"Referer":"https://wx2.qq.com/?&lang=zh_CN"}

oneurl="https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_=1527293427993"
r1=requests.get(oneurl,verify=False)
print(r1.text)

result = re.findall('= "(.*)";',r1.text)
uuid = result[0]

twourl="https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip={1}&r=2030070642&_={2}"
twourl=twourl.format(uuid,0,c_time)
r2=requests.get(twourl,verify=False)
cook=r2.cookies.get_dict()
print(r2.text)
print(cook)


# r408=requests.get(twourl,headers=headers,cookies=cook,verify=False)
# print(r408.text)

# url="https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_=1527293427993"
# uuid=requests.get(url,verify=False)
# uuid.encoding="utf-8"

#print(uuid.text)
# result = re.findall('= "(.*)";',uuid.text)
# uuid2 = result[0]

# ticket_url="https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}==&tip=0&r=1714683825&_=1527293428004"
# ticket_url=ticket_url.format(uuid2)
# cookie_dict=uuid.cookies.get_dict()


# print(cookie_dict)
# ticket=requests.get(ticket_url,verify=False,cookies=cookie_dict)
# print(ticket.text)