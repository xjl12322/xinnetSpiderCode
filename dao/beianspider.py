#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"

import requests
from lxml import etree
from dao.findbase import Find

ag =  {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
find = Find()
def beian_spider(domain):

    d = {"urls": domain,
         "btn_search": "查询"}
    r = requests.post(url='http://icp.chinaz.com/searchs', data=d,headers=ag)
    print(r.status_code)
    # print(r.text)
    selector = etree.HTML(r.text)
    company_name=selector.xpath('//tbody[@id="result_table"]/tr/td[1]/text()')[0].strip()
    print(company_name,"2222222")
    if company_name == "--":
        pass
    else:
        company_type = selector.xpath('//tbody[@id="result_table"]/tr/td[2]/text()')[0].strip()
        website_recard_num = selector.xpath('//tbody[@id="result_table"]/tr/td[3]/text()')[0].strip()
        website_name = selector.xpath('//tbody[@id="result_table"]/tr/td[4]/text()')[0].strip()
        website_homepage = selector.xpath('//tbody[@id="result_table"]/tr/td[@class="Now"]/span/a/text()')[0].strip()
        check_date = selector.xpath('//tbody[@id="result_table"]/tr/td[6]/text()')[0].strip()
        # print("!~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # print(company_name, "111")
        # print(company_type)
        # print(website_recard_num)
        # print(website_homepage)
        # print(website_name)
        # print(check_date)
        # print("!~~~~~~~~~~~~~~~~~~~~~~~~~~~~!!!!!!!!!!!!!!!!")
        find.insertbeian(company_name,company_type,website_recard_num,website_homepage,website_name,check_date)
if __name__ == "__main__":
    beian_spider("17173.com")