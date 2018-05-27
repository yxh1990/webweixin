import time
c_time = int(time.time() * 1000)
print(c_time)
import random
num=random.randint(1600000000,1700000000)
print(num)

baseurl = "https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=zh_CN&pass_ticket={0}"
url = baseurl.format("eee")
print(url)