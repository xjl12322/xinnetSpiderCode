#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"
import datetime,time
from utils.md5_use import mad5_url,getsecret2
# class Validation(object):


def validarion(appkey,ts,sign):
    if appkey == "" or appkey == None:
        return {"message": "appkey不能为空"}
    if ts == "" or ts == None:
        return {"message": "ts不能为空"}
    if sign == "" or sign == None:
        return {"message": "sign不能为空"}
    if not ts.isdigit():
        return {"message":"ts格式不正确"}


    before = int(time.time()*1000)-3600000
    after = int(time.time()*1000)+3600000
    if not before<=int(ts)<=after:
        return {"message": "ts有效期不正确"}

    singn, innerApp, ts = getsecret2(ts)
    if singn != sign:
        return {"message": "appKey签名不正确"}
    return "yes"

if __name__ =="__main__":
    # appKey = "vhost"
    # secret = "4065819c-2991-4c75-b809-3798347ec372"

    appKey = "whois"
    secret = "aef8f507-d1b3-4697-b6a7-6fd7d83b0ff7"
    ts = str(int(time.time()*1000)+3000)
    # print(ts)
    print(ts)
    sign = "innerApp=" + appKey + "&secret=" + secret + "&ts=" + ts

    singn = mad5_url(sign)
    print(singn)
    a = validarion(appKey,ts,singn)
    print(a)
