#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author:   chenjh
# @DateTime: 2020-03-03 14:31
# @Software: PyCharm
# @File:     tests.py

import requests,time

def geturl(url):
     s = time.time()
     r = requests.get(url)
     e = time.time()
     print(int(e-s))

getrul(r"http://127.0.0.1:8000/?q=yangyanxing")