from django.shortcuts import render,HttpResponse
from django.views import View
import hashlib
import time

APPID="8888"
visited = []

class AssetView(View):

    def get(self,request,*args,**kwargs):
        appid=request.META.get("HTTP_APPID")
        if not appid:
            return HttpResponse("没有提供appid")

        clientappid, client_time = appid.split("|")

        #clientappid是由appid和client_time一起做md5运算得到的唯一摘要
        #client_time没有做md5运算 clientappid|client_time
        #所以在后面可以直接参与时间的计算

        current_time = time.time()
        f_client_time = float(client_time)
        print(appid)
        current_client={'encrypt':clientappid,'time':client_time}
        if current_time-10 > f_client_time: #第一关时间是否超时
            return HttpResponse("请求超时")
        if current_client in visited:  #第二关合法的客户端key是否已经用过
            return HttpResponse("appkey已经超时失效")

        m=hashlib.md5()
        m.update(bytes(APPID+client_time,encoding="utf-8"))
        #第三关采用md5机制必须按照原来的字符串(appid+client_time)进行密文验证
        #此处没有解密按照原文比较,而是直接采用比对加密后的字符串
        new_appid = m.hexdigest()

        if new_appid == clientappid:
            visited.append({'encrypt': new_appid, 'time': f_client_time})
            limit_timestamp = float(time.time()-10) #超过10秒的记录自动删除
            del_keys = []
            for k, v in enumerate(visited):
                m = v['time']
                n = v['encrypt']
                if m < limit_timestamp:
                    del_keys.append(v)
                    continue

            print("****************************************")
            print(visited)
            print(del_keys)
            print("***************************************")

            for k in del_keys:
                visited.remove(k)
            print("当前还有%d个访问记录" % (len(visited)))
            return HttpResponse("验证成功")
        else:
            return HttpResponse("验证失败")











