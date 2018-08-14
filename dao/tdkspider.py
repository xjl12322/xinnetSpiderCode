#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"

import requests,redis
import json,sys
import re
from lxml import etree
dict_encode = {"utf-8": "utf-8", "GB2312": "gbk", "Windows-": "utf-8"}
# def return_code(url):
#     data = {
#         "domain": url,
#         "title": "",
#         "description": "",
#         "keywords": ""
#     }
#     jsondata = json.dumps(data)
#     return -1, jsondata
def get_list_url(url,es):

    '''发送网页请求'''
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    # r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)
    # r = redis.StrictRedis(host="10.2.1.173", port=17480, password="J9O543637e5SYaymJge", db=0)
    try:
        response = requests.get(url="http://www.{}".format(url),headers=header,timeout=6)
    except Exception as e:
        # return return_code(url)
        return None
    if response.status_code!=200:
        return None
    try:
        judgment = response.apparent_encoding
        if judgment in dict_encode:
            response.encoding = dict_encode[judgment]
        elif judgment.startswith("ISO-"):
            response.encoding = dict_encode["gbk"]
        elif judgment.startswith("Windows-"):
            response.encoding = dict_encode["utf-8"]
        else:
            return None
    except:
        return None
    '''解析详情页'''
    try:
        selector = etree.HTML(response.text)
    except:
        return None
    try:
        title = selector.xpath("//title/text()")[0].strip()
    except:
        title = ""
    try:
        keywords = selector.xpath("//*[contains(@name,'keywords')]/@content|//*[contains(@name,'Keywords')]/@content")[0].strip()
    except:
        keywords = ""
    try:
        description = selector.xpath("//*[contains(@name,'Description')]/@content|//*[contains(@name,'description')]/@content")[0].strip()
    except:
        description = ""
    keywords = keywords.replace("\xa0", "").replace("\r", "").replace("\n","").replace("\t", "").replace("_", ",")\
               .replace("、", ",").replace("|", ",").replace("，", ",").replace(" ", ",").replace("'", r"\'").replace('"', r"\"")
    description = description.replace("\xa0", "").replace("\r", "").replace("\n", "").replace("\t", "") \
        .replace("，", ",").replace(" ", ",").strip()

    data = {

        "domainName": url,
        "title": title,
        "description": description,
        "keywords": keywords
    }
    # jsondata = json.dumps(data,ensure_ascii=False)
    # print(data)
    jsondata = data
    jsondata["domainName"] = url
    boolean = es.c_tdk(jsondata)
    if boolean == True:
        print("插入成功")



if __name__ =="__main__":
    # domainname = "hao123.com"
    # domainname = domainname.strip()
    # realdomain = domainname
    # try:
    #     c = re.search(u"[\u4e00-\u9fa5]+", domainname).group()
    #     if c:
    #         domainname = domainname.split(".")
    #         realdomain = domainname[0].encode("utf-8").encode("punycode")
    #         index = 1
    #         while index < len(domainname):
    #             realdomain += "."
    #             c1 = re.search(u"[\u4e00-\u9fa5]+", domainname[index]).group()
    #             if c1:
    #                 realdomain1 = domainname[index].encode("utf-8")
    #                 realdomain = realdomain + "xn--" + realdomain1
    #             else:
    #                 realdomain = realdomain + domainname[index]
    #             index += 1
    #         realdomain = "xn--" + realdomain
    # except:
    #     pass
    # domain = realdomain
    domain = "meituan.com"
    rtcode, jsondata = get_list_url(domain)
    print(jsondata)

