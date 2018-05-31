from django.shortcuts import render,HttpResponse
from django import conf
import requests
import time
import re
import json
from bs4 import BeautifulSoup
from requests.packages import urllib3
urllib3.disable_warnings()

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',"Referer":"https://wx.qq.com/"}
ALL_COOKIE_DICT = {}

def ticket(html):
    ret={}
    soup = BeautifulSoup(html,'html.parser')
    for tag in soup.find(name="error").find_all():
        ret[tag.name] = tag.text
    return ret

#获取登录二维码
def login(req):
    if req.method == "GET":
        uuid_time=int(time.time() * 1000)
        base_uuid_url="https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx2.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={0}"
        uuid_url=base_uuid_url.format(uuid_time)
        r1=requests.get(uuid_url,headers=headers,verify=False)
        req.session['LOGIN_COOKIE'] = r1.cookies.get_dict()
        #print(r1.text)
        #window.QRLogin.code = 200; window.QRLogin.uuid = "YaV-_IUB0g==";
        result = re.findall('= "(.*)";',r1.text)
        uuid = result[0]
        req.session["UUID_TIME"]=uuid_time
        req.session["UUID"]=uuid
        return render(req,'login.html',{'uuid':uuid})

TIP=1  #必须为1,不然会重复发送请求
#检测手机确定登录
def check_login(req):
    response ={'code':408,'data':""}
    c_time = int(time.time() * 1000)
    global TIP
    #base_login_url="https://login.wx2.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip={1}&r={2}&_={3}"
    base_login_url = "https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip={1}&r={2}&_={3}"
    login_url=base_login_url.format(req.session["UUID"],TIP,c_time,c_time)
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
        #req.session['LOGIN_COOKIE'] = r1.cookies.get_dict()
        redirect_url=re.findall('redirect_uri="(.*)";',r1.text)[0]
        redirect_url = redirect_url + "&fun=new&version=v2"
        #必须添加&fun=new&version=v2否则会返回301不断发送请求
        #print(req.session["LOGIN_COOKIE"])



        #获取登录用户凭证ticket
        #从这里开始跳转到wx2.qq.com
        r2=requests.get(redirect_url,headers=headers,verify=False)
        r2.encoding = "utf-8"
        ticket_dict=ticket(r2.text)
        req.session['TICKET_DICT']=ticket_dict

        req.session["LOGIN_COOKIE"]=r2.cookies.get_dict()
        ALL_COOKIE_DICT.update(r2.cookies.get_dict())

        #print(ALL_COOKIE_DICT)

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

#获取最近联系人
def index(req):

    '''显示最近联系人'''
    return render(req,'index.html')

#获取所有联系人
def contact_all(req):
    base_url="https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?lang=zh_CN&pass_ticket={0}&r={1}&skey={2}"
    ctime = time.time()*1000
    url=base_url.format(req.session['TICKET_DICT']['pass_ticket'],ctime,req.session['TICKET_DICT']['skey'])
    r1=requests.get(url,cookies=ALL_COOKIE_DICT,verify=False)
    r1.encoding = "utf-8"
    contact_dict = json.loads(r1.text)

    #contact_dict["MemberList"] = contact_dict["MemberList"]
    #contact_dict["MemberList"]=contact_dict["MemberList"][0:1]

    return render(req,'contact_all.html',{'contact_dict':contact_dict})

#获取头像
def avatar(req):
    prev=req.GET.get("imgUrl")
    username=req.GET.get("username")
    skey=req.GET.get("skey")

    imgheaders={}
    imgheaders.update(headers)
    imgheaders["Accept"]="image/webp,image/apng,image/*,*/*;q=0.8"
    imgheaders["Referer"]="https://wx2.qq.com/"
    img_url= "https://wx2.qq.com{0}&username={1}&skey={2}".format(prev,username,skey)

    #img_url拼接的时候在qq.com后面多加了一个/ 导致请求图片的时候总是重定向到微信网页的首页
    #https://wx2.qq.com/ 变成了 https://wx2.qq.com//

    # ALL_COOKIE_DICT["MM_WX_NOTIFY_STATE"] = "1"
    # ALL_COOKIE_DICT["MM_WX_SOUND_STATE"] = "1"
    # ALL_COOKIE_DICT["last_wxuin"] = ALL_COOKIE_DICT["wxuin"]
    # ALL_COOKIE_DICT["login_frequency"] = "1"
    # ALL_COOKIE_DICT["wxpluginkey"] = "1527736172"
    # ALL_COOKIE_DICT["wxloadtime"]  = ALL_COOKIE_DICT["wxloadtime"]+"_expired"

    # for key,value in ALL_COOKIE_DICT.items():
    #     print(key,value)
    # testurl="https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxgeticon?seq=666282190&username=@f9c03c12e89387fd7e8087ec62cdd1840a7100c21b084c2f33e2c18989e373f5&skey=@crypt_7ec64e9b_9385cde7ae7071423f2a4ddceea9ea8a"


    r1 = requests.get(url=img_url,headers=imgheaders,cookies=ALL_COOKIE_DICT,verify=False)
    #print(r1.content)
    #服务端返回的图片格式是十六进制的数据
    #b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\
    # with open('a.jpg','wb') as f: 把字节内容写入本地磁盘
    #     f.write(r1.content)
    return HttpResponse(r1.content)


#发送微信消息
def send_msg(req):
    send=req.GET.get("send")
    recv =req.GET.get("recv")
    content = req.GET.get('content')
    # print(send)
    baseurl="https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=zh_CN&pass_ticket={0}"
    url = baseurl.format(req.session['TICKET_DICT']['pass_ticket'])
    ctime = time.time()*1000
    form_data = {
         "BaseRequest":{
                "DeviceID":"e839448703423521",
                "Sid":req.session['TICKET_DICT']["wxsid"],
                "Uin":req.session['TICKET_DICT']["wxuin"],
                "Skey":req.session['TICKET_DICT']["skey"]
            },
        "Msg":{
              "ClientMsgId":ctime,
              "Content":content,
              # "FromUserName":req.session['init_dict']["User"]["UserName"],
              "FromUserName":send,
              "LocalID":ctime,
              "ToUserName":recv,
              "Type":1
        },
        "Scene":0
    }
    #json.dumps(ensure_ascii=True) 导致中文乱码
    #如果是字符串则不会调用json.dumps
    r1=requests.post(
        url=url,
        data=bytes(json.dumps(form_data,ensure_ascii=False),encoding="utf-8"),
        headers={
            'Content-Type':'application/json'
        },
        cookies=ALL_COOKIE_DICT,
        verify=False
    )
    return HttpResponse("send msg sucess...")


#接收微信消息
def get_msg(req):
    #检测是否有消息到来
    check_msg_url="https://webpush.wx.qq.com/cgi-bin/mmwebwx-bin/synccheck"
    ctime = int(time.time()*1000)
    synckey_dict = req.session['init_dict']["SyncKey"]
    synckey_list=[]

    for item in synckey_dict["List"]:
        tmp ="%s_%s"%(item['Key'],item['Val'])
        synckey_list.append(tmp)
    synckey="|".join(synckey_list)

    r1=requests.get(url=check_msg_url,params={
        'r':ctime,
        'skey':req.session['TICKET_DICT']["skey"],
        'sid':req.session['TICKET_DICT']["wxsid"],
        'uin':req.session['TICKET_DICT']["wxuin"],
        '_':ctime,
        'synckey':synckey
    },cookies=ALL_COOKIE_DICT,verify = False)

    print(r1.text)
    if '{retcode:"1100",selector:"0"}' in r1.text:
        return HttpResponse("no msg ...")
    get_msg_url="https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsync?sid={0}&skey={1}&lang=zh_CN&pass_ticket={2}"
    get_msg_url = get_msg_url.format(req.session['TICKET_DICT']["wxsid"],req.session['TICKET_DICT']["skey"],req.session['TICKET_DICT']['pass_ticket'])
    form_data = {
        "BaseRequest": {
            "DeviceID": "e839448703423521",
            "Sid": req.session['TICKET_DICT']["wxsid"],
            "Uin": req.session['TICKET_DICT']["wxuin"],
            "Skey": req.session['TICKET_DICT']["skey"]
        },
       "SyncKey":req.session['init_dict']["SyncKey"]
    }
    r2=requests.post(
        url=get_msg_url,
        json = form_data,
        cookies=ALL_COOKIE_DICT,
        verify = False
    )
    r2.encoding="utf-8"
    msg_dict=json.loads(r2.text)
    for msg in msg_dict["AddMsgList"]:
        print("新的消息:   ",msg["Content"])

    init_dict = req.session['init_dict']
    init_dict['SyncKey'] = msg_dict['SyncKey']
    req.session['init_dict'] = init_dict

    return  HttpResponse("get over...")










