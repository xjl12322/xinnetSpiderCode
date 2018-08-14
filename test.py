#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2017/11/6 20:09"
import json
import threading

from dao.baidu_keyman import Keymain


keyman_obj = Keymain("商标注册")
t1 = threading.Thread(target=keyman_obj.get_json)
t1.start()
kk = t1.join()
print(kk,"kkkkkkkkkkkkkkkkkkkkk")

