from django.shortcuts import render,HttpResponse
from django import conf
import requests
import time
import re
import json
from bs4 import BeautifulSoup
from requests.packages import urllib3
urllib3.disable_warnings()
s = requests.Session()

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',"Referer":"https://wx.qq.com/","Upgrade-Insecure-Requests":"1"}

def ticket(html):
    ret={}
    soup = BeautifulSoup(html,'html.parser')
    for tag in soup.find(name="error").find_all():
        ret[tag.name] = tag.text
    return ret

def login(req):
    if req.method == "GET":
        uuid_time=int(time.time() * 1000)
        base_uuid_url="https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={0}"
        uuid_url=base_uuid_url.format(uuid_time)
        r1=s.get(uuid_url,headers=headers,verify=False)
        #print(r1.text)
        #window.QRLogin.code = 200; window.QRLogin.uuid = "YaV-_IUB0g==";
        result = re.findall('= "(.*)";',r1.text)
        uuid = result[0]
        #print(uuid)
        #return HttpResponse(".....")
        req.session["UUID_TIME"]=uuid_time
        req.session["UUID"]=uuid
        return render(req,'login.html',{'uuid':uuid})

TIP=1
def check_login(req):
    response ={'code':408,'data':""}
    c_time = int(time.time() * 1000)
    global TIP
    base_login_url="https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip={1}&r=2030070642&_={2}"
    login_url=base_login_url.format(req.session["UUID"],TIP,c_time)
    #print(login_url)
    r1 = s.get(login_url,headers=headers,verify=False)
    #print(r1.text)
    #print("执行到我了.....")
    #return json.dumps(response) 会出现异常
    if 'window.code=408' in r1.text:
        #表示无人扫码
        TIP=1
        response['code'] =408
    elif 'window.code=201' in r1.text:
        #表示扫码成功,返回头像,但是没有点击确定登录
        TIP=0
        response['code']=201
        response['data'] = re.findall("window.userAvatar = '(.*)';",r1.text)[0]
        req.session["USER_IMG"]=response['data']
    elif 'window.code=200' in r1.text:
        #扫码之后,并点击了确定按钮
        req.session["LOGIN_COOKIE"]=r1.cookies.get_dict()
        redirect_url=re.findall('redirect_uri="(.*)";',r1.text)[0]
        print(redirect_url)

        #获取登录用户凭证ticket
        cookie=req.session["LOGIN_COOKIE"]
        #allow_redirects = False
        r2=s.get(redirect_url,headers=headers,cookies=cookie,verify=False)
        print(r2.status_code)
        print(r2.text)

        #ticket_dict=ticket(r2.text)
        #print(ticket_dict)

        #req.session['TICKET_DICT']=ticket_dict
        #req.session["TICKET_COOKIE"]=r2.cookies.get_dict()

        #初始化,获取联系人信息,公众号
        #post方法如果是form-data 那么post方法中用data参数
        #如果是payload 那么就用json参数
        #一定要带上cookie否则获取不到用户数据

        # post_data={
        #     "BaseRequest":{
        #         "DeviceID":"e839448703423521",
        #         "Sid":ticket_dict["wxsid"],
        #         "Uin":ticket_dict["wxuin"],
        #         "Skey":ticket_dict["skey"]
        #     }
        # }
        # #初始化联系人和公众号信息
        # init_url="https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-2078742194"
        # cookie=req.session["TICKET_COOKIE"].update(req.session["LOGIN_COOKIE"])
        # print(cookie)
        # r3=requests.post(
        #     url=init_url,
        #     json=post_data,
        #     cookies=cookie,
        #     verify=False
        # )
        #
        # r3.encoding="utf-8"
        # init_dict = json.loads(r3.text)
        #
        # print(init_dict)
        # print(init_dict["User"])
        #
        # req.session['init_dict'] = init_dict
        #
        # response['code']=200

    return HttpResponse(json.dumps(response))

def index(req):

    '''显示最近联系人'''
    #img_url = "https://wx.qq.com" + req.session['init_dict']['User']['HeadImgUrl']
    #print(img_url)
    #res = requests.get(img_url, headers={'Referer': 'https://wx.qq.com/?&lang=zh_CN'})
    #print(res.text)
    return render(req,'index.html')
    #return HttpResponse("dddd")











