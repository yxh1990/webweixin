import requests

purl="https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=1876395664"

#
{"BaseRequest":{"Uin":"2824284317","Sid":"wBD6VxT6k5g9Y/C/","Skey":"","DeviceID":"e165626745889970"}}
post_data = {
    "BaseRequest": {
        "DeviceID": "e165626745889970",
        "Sid": "wBD6VxT6k5g9Y/C/",
        "Uin": "2824284317",
        "Skey": ""
    }
}

cookie="RK=btz0ndMkSh; ptcz=1120e17cd9d85d47c70f81b8fe537034880d71ffeff148f7dce93b35f4636a8c; pgv_pvid=9584848604; o_cookie=1272724627; pac_uid=1_1272724627; pt2gguin=o1272724627; pgv_pvi=6202027008; webwxuvid=51f3f8655a395721855bc3affcf2b61f956cc2c978232555e298a71b293a06b91f5814620e552ab706083a7dd7a6777f; tvfe_boss_uuid=cbff0131fc4cf4ad; wxuin=2824284317; wxsid=JEKO5IQnrYHMxg7b; mm_lang=zh_CN; webwx_data_ticket=gScqzq6TrCSMI9mOS9U3T7j1; webwx_auth_ticket=CIsBEL3Sla8MGoABhvZ/huti2jSZNZEvE8M/+wUCLJItyi1YXmW8mZORDesv5K9Urykl3VvDcpetEnQmzMpu1TYCqeCrEKMCQx8N7Nc0r43wclNNq8CoPtHrkOhMWTRFAXXjO/O07KLWQ8MTyeDJaWfSR0Csc7y8M92Ym4QwmidAPfGyoEaCCJCI68s=; MM_WX_NOTIFY_STATE=1; MM_WX_SOUND_STATE=1; wxloadtime=1526978562_expired; wxpluginkey=1526978489"
cookies={}
for line in cookie.split(";"):
    name,value =line.split("=",1)
    cookies[name]=value

r3=requests.post(
            url=purl,
            json=post_data
        )
r3.encoding="utf-8"

print(r3.text)