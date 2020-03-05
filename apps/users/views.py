#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author:   chenjh
# @DateTime: 2020-03-05 14:40
# @Software: PyCharm
# @File:     views.py
from utils.base import BaseHandler

from . import models

class DeptViewSet(BaseHandler):

    def get(self):
        '''
            创建部门
        :return:
        '''
        # new_dept = models.Dept(name='测试——陈军辉')

        data = self.db.query(models.Dept).all()
        for item in data:
            print(item.content)
