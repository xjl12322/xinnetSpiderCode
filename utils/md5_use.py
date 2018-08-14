#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/10/22 23:07"

import hashlib,time

def mad5_url(urls):
    '''mad加密功能
    '''

    if isinstance(urls,str):  #py3里全是uncode字符集 也就是str，md5前判断 因为py3 unicode不能直接md5必须转换utf-8，相反py2则不用
        urls = urls.encode("utf-8")
    md5_url = hashlib.md5()
    md5_url.update(urls)
    md5_url.hexdigest()
    # print(md5_url.hexdigest())
    return md5_url.hexdigest()

def getsecret():
    innerApp = "whois"
    secret = "5f6313dc-eedd-45b4-a2b1-2315bc5b98c4"
    ts = str(int(time.time()*1000))
    sign = "innerApp=" + innerApp + "&secret=" + secret + "&ts=" + ts
    singn = mad5_url(sign)
    return singn,innerApp,ts

def getsecret2(ts):
    innerApp = "whois"
    secret = "aef8f507-d1b3-4697-b6a7-6fd7d83b0ff7"
    sign = "innerApp=" + innerApp + "&secret=" + secret + "&ts=" + ts
    singn = mad5_url(sign)
    return singn,innerApp,ts



def getsecret_pythontool():
    innerApp = "pythontool"
    secret = "a6d903a2-dac5-4d9d-9e6b-e32caad1dafc"
    ts = str(int(time.time()*1000))
    sign = "innerApp=" + innerApp + "&secret=" + secret + "&ts=" + ts
    singn = mad5_url(sign)
    return singn,innerApp,ts


if __name__ =="__main__":
    ts = "111111"
    # print(ts.isdigit())
    a = mad5_url(ts)
    print(a)
    before = str(int(time.time()*1000))
    print(before)
    singn, innerApp, ts = getsecret2(before)
    print(singn+"#####")
    print(innerApp)
    print(ts)