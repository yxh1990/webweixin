import requests
import hashlib
import time

appid="8888"
current_time = str(time.time())

m=hashlib.md5()
m.update(bytes(appid+current_time,encoding="utf-8"))
temp_appid = m.hexdigest()
print(temp_appid)

new_appid="%s|%s"%(temp_appid,current_time)
print(new_appid)

response = requests.get(
    "http://127.0.0.1:8000/asset/",
    params={"appid":appid},
    headers={"appid":"aa3280194decb78f542272f16c075e43|1526975940.4176583"}
)

print(response.text)