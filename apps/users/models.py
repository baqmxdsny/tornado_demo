#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author:   chenjh
# @DateTime: 2020-03-04 10:14
# @Software: PyCharm
# @File:     models.py
from sqlalchemy import create_engine,Column,Integer,Float,Boolean,DECIMAL,Enum,Date,DateTime,Time,String,Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# 在Python3中才有这个enum模块，在python2中没有
import enum
from datetime import datetime
from utils.base import BaseModel


class User(BaseModel):
    __tablename__ = 'Profile'
    name = Column(String(20), unique=True)