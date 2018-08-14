#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"
from utils.Database_Connext import connect_mysql

class Find(object):
    def __init__(self):
        print("chusi")
        self.con = connect_mysql()
        self.cursor = self.con.cursor()

    def findbeian(self,domain):

            domains = "www."+domain
            sql = "select * from beian where website_homepage=%s"
            num = self.cursor.execute(sql,(domains,))
            if num ==0:
                self.cursor.execute(sql, (domain,))
            result = self.cursor.fetchone()
            return result

    def findbusiness(self,companname):
        sql = "select * from business where eid=%s"
        num = self.cursor.execute(sql, (companname,))
        result = self.cursor.fetchone()
        return result

    def insertbeian(self,company_name,company_type,website_recard_num,website_homepage,website_name,check_date):
        sql = "insert ignore into beian(company_name,company_type,website_recard_num,website_homepage,website_name,check_date) VALUES (%s,%s,%s,%s,%s,%s)"
        try:
            num = self.cursor.execute(sql, (company_name,company_type,website_recard_num,website_homepage,website_name,check_date))
            if num==1:
                print(num,"插入成功")
            self.con.commit()
        except Exception as e:
            print(e)
            self.con.rallback()
        finally:
            self.con.close()





if __name__ =="__main__":
    aa = Find()
    # cc = aa.findbeian("3xyl.com")
    # print(cc)
    # bb = aa.findbusiness("1492a6d969a99da824139efc04d7157a")
    # print(bb)

    bb = aa.insertbeian("东莞市三加乐电子商务有限公司","企业","粤ICP备16005446号-5","www.3zqw.cnn","赚钱网站","2016-04-27")
