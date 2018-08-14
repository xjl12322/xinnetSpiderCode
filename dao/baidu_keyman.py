#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"

from urllib.parse import quote
import requests
from lxml import etree
import re,threading
from tld import get_tld
from dao.findredis import Find_Redis

class Keymain(object):


    def __init__(self,keyman):
        self.find_redis = Find_Redis()
        self.keyman_dict = {'keyman':keyman,'index':{'quanwang':0,'baiduPc':0,'baiduMove':0,'360index':0,'sougouPc':0,'weixin':0,'shougouMove':0,'total':0,'top_domain':0,'context_page':0},'ranking':[],'top10':[],'baike':''}
        self.keyman = keyman
        self.keymans = quote(self.keyman)
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}


    def inquiry(self):
        # text = "商标注册"
        domainend = (
            '.com/', '.cn/', '.top/', '.co/', '.info/', '.net/', '.org/', '.xyz', '.mobi/',
            '.cx/', '.red/', 'gov/', 'edu/', '.mil/', '.biz/', '.name/','.ink/','.red/','.pub/','.CC/','.TV/','.mobi')
        header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
        i = 1
        whole_url = []
        domain_name = []
        for page in range(0,20,10):
            # print("第{}页".format(page))
            response = requests.get(url="https://www.baidu.com/s?wd={}&pn={}".format(self.keymans,page),headers=self.header)
            selecter = etree.HTML(response.text)
            num_text = selecter.xpath('string(//div[@class="nums"])').strip()
            num = re.search(r"约(.*?)个",num_text).group(1)
            if page == 10:
                i = 11
            for x in range(0,10):
                title= selecter.xpath('string(//div[@id="%s"]/h3)' %(x+i)).strip()

                url = selecter.xpath('//div[@id="%s"]/h3/a[1]/@href' %(x+i))[0]
                response1 = requests.get(url=url,headers = header,allow_redirects=False,timeout=16)

                if response1.status_code == 302:
                    url = response1.headers.get("location")

                    whole_url.append(url)
                    if url.endswith(domainend):


                        top_domain = re.sub(r"^http://www.|^https://www.|^http://|^https://|^www.|/$", "", url)
                        self.keyman_dict["ranking"].append({top_domain:title})
                        domain_name.append(top_domain)
                        # print(top_domain,title)
                    if len(self.keyman_dict["top10"])!=10:
                        url_url = get_tld(url=url)
                        self.keyman_dict["top10"].append({url_url:title+url})


        self.keyman_dict['index']['total'] = num

        self.keyman_dict['index']['top_domain']= len(domain_name)
        self.keyman_dict['index']['context_page'] = len(whole_url)-len(domain_name)
        # print("顶级域名/二级数量",len(domain_name))
        # print("内容页数量",len(whole_url)-len(domain_name))


    def china_z(self):
        url = "http://index.chinaz.com/?words={}".format(self.keymans)
        try:
            a = requests.get(url=url, headers=self.header, timeout=14)
            se = etree.HTML(a.text)
            title = se.xpath(
            'string(//div[@class="zs-wrap"]/ul[1])').split()  # 收录标题['关键词', '全网指数', 'PC搜索指数', '移动搜索指数', '360指数', '搜狗PC指数', '搜狗移动指数', '微信指数']
            zhishu = se.xpath('//div[@class="zs-wrap"]/ul[2]//div[@class="clearfix"]//strong/text()')

            self.keyman_dict['index']['quanwang'] = zhishu[0] if zhishu[0]!="未收录" else '0'
            self.keyman_dict['index']['baiduPc'] = zhishu[1] if zhishu[1]!="未收录" else '0'
            self.keyman_dict['index']['baiduMove'] = zhishu[2] if zhishu[2]!="未收录" else '0'
            self.keyman_dict['index']['360index'] = zhishu[3] if zhishu[3]!="未收录" else '0'
            self.keyman_dict['index']['sougouPc'] = zhishu[4] if zhishu[4]!="未收录" else '0'
            self.keyman_dict['index']['weixin'] = zhishu[5] if zhishu[5]!="未收录" else '0'
            self.keyman_dict['index']['shougouMove'] = zhishu[6] if zhishu[6]!="未收录" else '0'
        except Exception as e:
            pass
        # print(self.keyman_dict)




    def baike(self):
        # 发送请求

        base_url = "https://baike.baidu.com/item/{}".format(self.keymans)

        try:
            response = requests.get(url=base_url, headers=self.header, timeout=15)
            response.encoding = "utf-8"
            try:
                html = etree.HTML(response.text)
                descriptions = html.xpath('string(//div[@class="lemma-summary"])').strip()
                if descriptions is not None:
                    description = re.sub("\[\d+\]", "", descriptions)
                    description = re.sub(r"\n\xa0\n|\n|\xa0", "img", description)
                    description = description
                    self.keyman_dict['baike'] = description


            except Exception as e:
                print(e)
                print("html解析失败！！错误信息：{}".format(e))


        except Exception as e:
            print("请求失败！！错误信息：{}".format(e))

    def get_json(self):
        # threads = []
        # t1 = threading.Thread(target=self.baike)
        # threads.append(t1)
        # t2 = threading.Thread(target=self.china_z)
        # threads.append(t2)
        # t3 = threading.Thread(target=self.inquiry)
        # threads.append(t3)
        # for t in threads:
        #     t.start()
        # for s in threads:
        #     s.join()

        self.inquiry()
        self.china_z()
        self.baike()


        self.find_redis.inserkeymanranking(self.keyman,self.keyman_dict)
        # return self.keyman_dict
        # q.put(self.keyman_dict)
if __name__ == "__main__":
    kk = Keymain("股东")
    kk.get_json()
    # r = kk.get_json()
    # print(r,"333333333333333333")






