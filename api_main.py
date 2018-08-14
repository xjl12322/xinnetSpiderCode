#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2018/6/18 14:44"
from flask import Flask
from flask_restful import Api, reqparse

# from flask.ext.restful import reqparse,Api,Resource
from api_service import TDK,Beian,Business,KeymanRanking


app = Flask(__name__)
api = Api(app)


api.add_resource(TDK,"/getTdk")
api.add_resource(Beian,"/getBeian")
api.add_resource(Business,"/getBusiness")
api.add_resource(KeymanRanking,"/getKeymanRanking")

if __name__ == '__main__':
    # app.config['JSON_AS_ASCII'] = False
    # app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    # app.run(host='119.10.116.237',port=7081)
    app.run(host='127.0.0.1', port=5003)
