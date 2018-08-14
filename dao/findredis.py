#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"

from utils.Database_Connext import connect_redis
import json


class Find_Redis(object):
    def __init__(self):

        self.con = connect_redis()

    def inserkeymanranking(self,keyman,key_json):

        try:
            self.con.delete("keyman:" + keyman)
            num = self.con.sadd("keyman:"+keyman,key_json)
            if num==1:
                print("添加成功")
        except Exception:
            print("插入失败")



    def getkeymanranking(self,keyman):
        result = self.con.smembers("keyman:"+keyman)
        if not result:
            return None
        else:
            result_dict = eval(list(result)[0])
            return result_dict






if __name__ =="__main__":
    aa = Find_Redis()
    # cc = aa.findbeian("3xyl.com")
    # print(cc)
    # bb = aa.findbusiness("1492a6d969a99da824139efc04d7157a")
    # print(bb)
    key_json = {'keyman': '商标注册',
                'index': {'quanwang': '76,569', 'baiduPc': '1138', 'baiduMove': '2569', '360index': '286',
                          'sougouPc': '29,148', 'weixin': '43,228', 'shougouMove': '0', 'total': '8,970,000',
                          'top_domain': 11, 'context_page': 9},
                'ranking': [{'sbj.saic.gov.cn': '国家工商行政管理总局商标局_中国商标网'}, {'wsjs.saic.gov.cn': '商标网上检索系统'},
                            {'ctmo.gov.cn': '国家工商行政管理总局商标局_中华人民共和国国家工商行政管理总局'},
                            {'ipr.zbj.com': '商标注册|商标查询|专利申请|版权登记|代理机构-八戒知识产权[官网]'},
                            {'tmkoo.com': '商标查询 - 商标注册查询 - 中国商标网 - 标库网官网'}, {'quandashi.com': '商标查询|免费商标查询|商标注册-权大师官网'},
                            {'zhiguoguo.com': '商标注册_版权服务_专利服务-知果果'}, {'tm.cn': '免费商标注册,商标查询-易名科技'},
                            {'biaotianxia.com': '商标注册_商标查询_注册商标查询 - 标天下'},
                            {'bjgongteng.com': '商标查询|商标注册申请代理|商标注册流程及费用-共腾知识产权'},
                            {'chen7782.com': '商标注册查询免费|商标设计480元|商标起名380元 商标转让劲爆价'}],
                'top10': [{'sbj.saic.gov.cn': '国家工商行政管理总局商标局_中国商标网http://sbj.saic.gov.cn/'},
                          {'wsjs.saic.gov.cn': '商标网上检索系统http://wsjs.saic.gov.cn/'},
                          {'ctmo.gov.cn': '国家工商行政管理总局商标局_中华人民共和国国家工商行政管理总局http://www.ctmo.gov.cn/'},
                          {'ipr.zbj.com': '商标注册|商标查询|专利申请|版权登记|代理机构-八戒知识产权[官网]https://ipr.zbj.com/'},
                          {'tmkoo.com': '商标查询 - 商标注册查询 - 中国商标网 - 标库网官网http://www.tmkoo.com/'},
                          {'quandashi.com': '商标查询|免费商标查询|商标注册-权大师官网https://www.quandashi.com/'},
                          {'zhiguoguo.com': '商标注册_版权服务_专利服务-知果果https://www.zhiguoguo.com/'},
                          {'tm.cn': '免费商标注册,商标查询-易名科技https://www.tm.cn/'},
                          {'biaotianxia.com': '商标注册_商标查询_注册商标查询 - 标天下http://biaotianxia.com/'},
                          {'bjgongteng.com': '商标查询|商标注册申请代理|商标注册流程及费用-共腾知识产权http://www.bjgongteng.com/'}],
                'baike': '商标注册img是商标使用人取得商标专用权的前提和条件，只有经核准注册的商标，才受法律保护。商标注册原则是确定商标专用权的基本准则，不同的注册原则的选择，是各国立法者在这一个问题中对法律的确定性和法律的公正性二者关系进行权衡的结果。'}

    bb = aa.inserkeymanranking("商标注册",key_json)

    # cc = aa.getkeymanranking("商标注册")
