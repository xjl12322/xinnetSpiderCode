#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"
import json
import threading
from flask import jsonify, Response
from flask_restful import Resource, reqparse,request
from dao.beianspider import beian_spider
# from flask.ext.restful import reqparse,Api,Resource
from dao.tdkspider import get_list_url

from dao.findbase import Find
from dao.findredis import Find_Redis
from dao.baidu_keyman import Keymain
from es_interface.es_crud import Es_crud
from utils.ValidationParameter import validarion
parser = reqparse.RequestParser()
# parser.add_argument("domainName",type=str,required=True,help="error",location = 'json')
# parser.add_argument("companyName",type=str,required=True,help="error",location = 'json')

find_data = Find()
find_redis = Find_Redis()
es = Es_crud()

class TDK(Resource):
    def get(self):
        domain = request.args.get("domainName")
        innerApp = request.args.get("innerApp")
        ts = request.args.get("ts")
        sign= request.args.get("sign")
        print("get请求 参数：" + str(domain))
        message = validarion(innerApp, ts, sign)

        print(message)
        if message=="yes":
            tdk = es.r_tdk(str(domain))
            print("es没有")
            if tdk == None or tdk == "":
                t1 = threading.Thread(target=get_list_url,args=(str(domain),es))
                t1.start()
                tdk = {
                    "domainName": domain,
                    "title": "",
                    "keywords": "",
                    "description": ""
                }
            tdk = json.dumps(tdk,ensure_ascii=False,indent=2)
            return Response(response=tdk,mimetype='application/json;charset=UTF-8',status=200)
        else:
            message = json.dumps(message,ensure_ascii=False,indent=2)
            return Response(response=message, mimetype='application/json;charset=UTF-8', status=200)




class Beian(Resource):
    def get(self):
        domain = request.args.get("domainName")
        innerApp = request.args.get("innerApp")
        ts = request.args.get("ts")
        sign= request.args.get("sign")
        print("get请求 参数：" + str(domain)+innerApp+ts+sign)
        message = validarion(innerApp,ts,sign)
        print(message)

        if message=="yes":
            result = find_data.findbeian(str(domain))
            if result==None:
                t1 = threading.Thread(target=beian_spider,args=(domain,))
                t1.start()
                result= {'company_name': '', 'company_type': '', 'website_recard_num': '',
                           'website_homepage': domain, 'website_name': '', 'check_date': '',"id":""}
            else:
                result['website_homepage'] = domain
            tlist = json.dumps(result,ensure_ascii=False,indent=2)
            # tlist = tlist("utf-8")
            return Response(response=tlist,mimetype='application/json;charset=UTF-8',status=200)
        else:
            message = json.dumps(message,ensure_ascii=False,indent=2)
            return Response(response=message, mimetype='application/json;charset=UTF-8', status=200)

class Business(Resource):
    def get(self):
        companyName = request.args.get("eid")
        innerApp = request.args.get("innerApp")
        ts = request.args.get("ts")
        sign= request.args.get("sign")
        print("get请求 参数：" + str(companyName)+innerApp+ts+sign)
        message = validarion(innerApp,ts,sign)
        print(message)
        if message=="yes":
            result = find_data.findbusiness(str(companyName))
            if result==None:
                result= {"eid":'',  'company_introduce': '',
 'tel': '', 'contacts_people': '', 'm_phone': '','eid':'','status':'','company_type':'','establish_date':'','expire_date':'','register_money':'','register_authority':'','business_scope':'','register_addpress':'','legal_representative':'','register_num':'','company_website':'','indutry_id':'','area_p':'','area_s':'','area_q':'','email':'','industry':''}
            result = json.dumps(result,ensure_ascii=False,indent=2)
            return Response(response=result,mimetype='application/json;charset=UTF-8',status=200)
        else:
            message = json.dumps(message,ensure_ascii=False,indent=2)
            return Response(response=message, mimetype='application/json;charset=UTF-8', status=200)


class KeymanRanking(Resource):
    def get(self):
        keyword = request.args.get("keyWord")
        innerApp = request.args.get("innerApp")
        ts = request.args.get("ts")
        sign= request.args.get("sign")
        print("get请求 参数：" + str(keyword))
        message = validarion(innerApp, ts, sign)

        if message=="yes":
            if keyword:
                result = find_redis.getkeymanranking(keyword)
                if result != None:

                    result_json = json.dumps(result, ensure_ascii=False, indent=2)
                    keyman_obj = Keymain(keyword)
                    t1 = threading.Thread(target=keyman_obj.get_json)
                    t1.start()
                    return Response(response=result_json, mimetype='application/json;charset=UTF-8', status=200)
                else:
                    keyman_obj = Keymain(keyword)
                    t1 = threading.Thread(target=keyman_obj.get_json)
                    t1.start()
                    keyman_dict = {'keyman': keyword,'index': {'quanwang': 0, 'baiduPc': 0, 'baiduMove': 0, '360index': 0, 'sougouPc': 0,'weixin': 0, 'shougouMove': 0, 'total': 0, 'top_domain': 0,'context_page': 0}, 'ranking': [], 'top10': [], 'baike': ''}
                    result_json = json.dumps(keyman_dict, ensure_ascii=False, indent=2)
                    return Response(response=result_json, mimetype='application/json;charset=UTF-8', status=200)
            else:
                keyman_dict = {'keyman': keyword,'index': {'quanwang': 0, 'baiduPc': 0, 'baiduMove': 0, '360index': 0, 'sougouPc': 0,'weixin': 0, 'shougouMove': 0, 'total': 0, 'top_domain': 0,'context_page': 0}, 'ranking': [], 'top10': [], 'baike': ''}
                result_json = json.dumps(keyman_dict,ensure_ascii=False,indent=2)
                return Response(response=result_json, mimetype='application/json;charset=UTF-8', status=200)

        else:
            message = json.dumps(message,ensure_ascii=False,indent=2)
            return Response(response=message, mimetype='application/json;charset=UTF-8', status=200)
