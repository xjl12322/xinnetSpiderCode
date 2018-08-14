#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"
import requests
import json
from utils.md5_use import getsecret,getsecret_pythontool
'http://tagapi.xinnet.com/rest/cms'
class Es_crud(object):
    def r_tdk(self,domain):
        sign,innerApp,ts = getsecret_pythontool()
        response_tdk = requests.get(url="http://10.2.2.103:8081/rest/whois/findTdk?domainName={}&innerApp={}&ts={}&sign={}".format(domain,innerApp,ts,sign)).text
        return response_tdk

    def c_tdk(self,tdk):
        sign, innerApp, ts = getsecret_pythontool()
        response_tdk = requests.post(url="http://119.10.116.247:8081/rest/whois/addOrUpdateTdk?innerApp={}&ts={}&sign={}".format(innerApp,ts,sign),json=tdk)
        response_tdk = json.loads(response_tdk.text)
        return response_tdk["result"]



if __name__ =="__main__":
    es = Es_crud()
    re = es.r_tdk("xinnet.com")
    print(re)
#     cc = es.c_tdk({
#   "id" : "1",
#   "domainName" : "xinnet.com",
#   "title" : "云服务器_域名注册_虚拟主机-新网域名云服务器提供商",
#   "keywords" : "箭头云服务器,云服务器,域名注册,虚拟主机,域名交易,域名,主机托管租用,企业邮箱,xinnet,xinwang,新网",
#   "description" : "新网是提供云服务器,箭头云服务器,域名注册,虚拟主机,域名交易,域名购买续费,主机托管租用,企业邮箱等互联网基础应用服务提供商,新网箭头云服务器专为中小微企业成长而设计的云服务器.新网是全球TOP11域名注册商，中国注册商唯一入选。"
# })
#     print(cc)