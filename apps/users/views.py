#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author:   chenjh
# @DateTime: 2020-03-05 14:40
# @Software: PyCharm
# @File:     views.py
from sqlalchemy import text
from settings import db
from utils.base import BaseHandler

from . import models

class DeptViewSet(BaseHandler):

    def get(self):
        '''
            获取
        :return:
        '''
        # new_dept = models.Dept(name='测试——陈军辉')

        result = self.query('select * from dept')
        self.write(result)

    def post(self):
        '''
            创建部门
        :return:
        '''
        name = str(self.get_argument('name', None))

        parent_id = self.get_argument('parent_id', None)
        sql = """insert into DEPT (name , parent_id) values (:name , :parent_id) """
        result = self.insert(text(sql), {"name":name, "parent_id":parent_id})
        self.write('ok')