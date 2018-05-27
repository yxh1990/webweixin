from django.shortcuts import render,HttpResponse
from django import conf
import requests
import time
import re
import json
from bs4 import BeautifulSoup
from requests.packages import urllib3
urllib3.disable_warnings()

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',"Referer":"https://wx.qq.com/","Upgrade-Insecure-Requests":"1"}
ALL_COOKIE_DICT = {}

def ticket(html):
    ret={}
    soup = BeautifulSoup(html,'html.parser')
    for tag in soup.find(name="error").find_all():
        ret[tag.name] = tag.text
    return ret

def login(req):
    if req.method == "GET":
        uuid_time=int(time.time() * 1000)
        base_uuid_url="https://login.wx2.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx2.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={0}"
        uuid_url=base_uuid_url.format(uuid_time)
        r1=requests.get(uuid_url,headers=headers,verify=False)
        #print(r1.text)
        #window.QRLogin.code = 200; window.QRLogin.uuid = "YaV-_IUB0g==";
        result = re.findall('= "(.*)";',r1.text)
        uuid = result[0]
        req.session["UUID_TIME"]=uuid_time
        req.session["UUID"]=uuid
        return render(req,'login.html',{'uuid':uuid})

TIP=1  #必须为1,不然会重复发送请求
def check_login(req):
    response ={'code':408,'data':""}
    c_time = int(time.time() * 1000)
    global TIP
    r = 1609646858
    base_login_url="https://login.wx2.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip={1}&r={2}&_={3}"
    login_url=base_login_url.format(req.session["UUID"],TIP,r,c_time)
    #（其中c_time这个值是当前距离林威治标准时间的毫秒）
    r1 = requests.get(login_url,headers=headers,verify=False)
    if 'window.code=408' in r1.text:
        #表示无人扫码
        response['code'] =408
    elif 'window.code=201' in r1.text:
        #表示扫码成功,返回头像,但是没有点击确定登录
        response['code']=201
        response['data'] = re.findall("window.userAvatar = '(.*)';",r1.text)[0]
        req.session["USER_IMG"]=response['data']
    elif 'window.code=200' in r1.text:
        #扫码之后,并点击了确定按钮
        req.session["LOGIN_COOKIE"]=r1.cookies.get_dict()
        redirect_url=re.findall('redirect_uri="(.*)";',r1.text)[0]
        redirect_url = redirect_url + "&fun=new&version=v2"
        #必须添加&fun=new&version=v2否则会返回301不断发送请求
        ALL_COOKIE_DICT.update(r1.cookies.get_dict())

        #获取登录用户凭证ticket
        r2=requests.get(redirect_url,headers=headers,verify=False)
        r2.encoding = "utf-8"
        ticket_dict=ticket(r2.text)
        req.session['TICKET_DICT']=ticket_dict

        req.session["TICKET_COOKIE"]=r2.cookies.get_dict()
        ALL_COOKIE_DICT.update(r2.cookies.get_dict())

        #初始化,获取联系人信息,公众号
        #post方法如果是form-data 那么post方法中用data参数
        #如果是payload 那么就用json参数
        #一定要带上cookie否则获取不到用户数据
        post_data={
            "BaseRequest":{
                "DeviceID":"e839448703423521",
                "Sid":ticket_dict["wxsid"],
                "Uin":ticket_dict["wxuin"],
                "Skey":ticket_dict["skey"]
            }
        }
        # #初始化联系人和公众号信息
        init_url="https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-2078742194"

        # cookies=" RK=btz0ndMkSh; ptcz=1120e17cd9d85d47c70f81b8fe537034880d71ffeff148f7dce93b35f4636a8c; pgv_pvid=9584848604; o_cookie=1272724627; pac_uid=1_1272724627; pt2gguin=o1272724627; pgv_pvi=6202027008; webwxuvid=51f3f8655a395721855bc3affcf2b61f956cc2c978232555e298a71b293a06b91f5814620e552ab706083a7dd7a6777f; tvfe_boss_uuid=cbff0131fc4cf4ad; wxuin=2824284317; mm_lang=zh_CN; MM_WX_NOTIFY_STATE=1; MM_WX_SOUND_STATE=1; wxpluginkey=1527393026; refreshTimes=5; wxsid=lJJlX/9erc9BRGNS; wxloadtime=1527401730; webwx_data_ticket=gSdddXvjpZf84UPAJDckkw66; webwx_auth_ticket=CIsBEIvN+bwJGoAB1rLWXJEPTvBKJqbZVSOyugUCLJItyi1YXmW8mZORDesv5K9Urykl3VvDcpetEnQmzMpu1TYCqeCrEKMCQx8N7Nc0r43wclNNq8CoPtHrkOhMWTRFAXXjO/O07KLWQ8MTbFmVB6pG6B3f1vpazZrqGM4KAhxuVUTYGIEGzWZhc2I=; login_frequency=1; last_wxuin=2824284317"
        # mycookie={}
        # for line in cookies.split(";"):
        #     name, value = line.split("=", 1)
        #     mycookie[name] = value
        #cookie参数是很重要的必须提交,否则获取不到用户的数据
        r3=requests.post(
            url=init_url,
            json=post_data,
            cookies=ALL_COOKIE_DICT,
            verify=False
        )

        r3.encoding="utf-8"
        init_dict = json.loads(r3.text)
        req.session['init_dict'] = init_dict
        response['code']=200

    return HttpResponse(json.dumps(response))

def index(req):

    '''显示最近联系人'''
    #img_url = "https://wx.qq.com" + req.session['init_dict']['User']['HeadImgUrl']
    #print(img_url)
    #res = requests.get(img_url, headers={'Referer': 'https://wx.qq.com/?&lang=zh_CN'})
    #print(res.text)
    return render(req,'index.html')
    #return HttpResponse("dddd")











