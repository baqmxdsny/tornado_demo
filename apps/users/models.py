#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author:   chenjh
# @DateTime: 2020-03-04 10:14
# @Software: PyCharm
# @File:     models.py
from sqlalchemy import create_engine,Column,Integer,Float,Boolean,DECIMAL,Enum,Date,DateTime,Time,String,Text,Table,ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
# 在Python3中才有这个enum模块，在python2中没有
import enum
from datetime import datetime
from utils.base import BaseModel

#   人员角色中间表
user_role = Table(
    'user_role', BaseModel.metadata,
    Column('role_id',Integer,ForeignKey('Role.id')),
    Column('profile_id',Integer,ForeignKey('Profile.id')),
    )
#   菜单角色中间表
menu_role = Table(
    'menu_role', BaseModel.metadata,
    Column('menu_id',Integer,ForeignKey('Menu.id')),
    Column('role_id',Integer,ForeignKey('Role.id')),
    )


class User(BaseModel):
    USER_STATUS = (
        (1, "在职"),
        (2, "离职"),
        (3, "密码失效")
    )
    __tablename__ = 'Profile'
    name = Column(String(20))
    usercode = Column(String(50), unique=True)
    password = Column(String(50))
    phone = Column(String(50))
    dept_id = Column( Integer, ForeignKey('DEPT.id'))
    dept = relationship("Dept", backref="User")
    job = Column(String(50))
    status = Column(Integer, default=1)
    token = Column(String(500), default='')
    active = Column(Integer, default=1)
    pwd_uptime = Column(DateTime, default=datetime.now)

    roles = relationship('Role', secondary=user_role, backref='Profile')
    # User通过roles关联Role表，Profile通过字段secondary去查第三张表：user_role
    # backref='Profile'用来反向查一个作者有多少本书


class Dept(BaseModel):
    """
    部门信息
    """
    __tablename__ = 'DEPT'
    dept_name = Column(String(50))

    parent_id = Column( Integer, ForeignKey('DEPT.dept_id'))
    parent = relationship("Dept", remote_side=[id], backref="Dept")



class Role(BaseModel):
    """
    角色
    """
    ROLE_TYPE = (
        (1, '是'),
        (0, '否')
    )
    ROLE_STATUS = (
        (0, '正常'),
        (1, '删除'),
        (2, '停用')
    )
    __tablename__ = 'Role'

    name = Column(String(50), unique=True)
    is_sys = Column(Integer, default=1)
    status = Column(Integer, default=1)
    remarks = Column(String(1000))

    menu = relationship('Menu', secondary=menu_role, backref='Role')

    create_user_id = Column( Integer, ForeignKey('Profile.id'))
    updata_user_id = Column( Integer, ForeignKey('Profile.id'))
    create_user = relationship("User", backref="create_roles", foreign_keys=[create_user_id])
    updata_user = relationship("User", backref="update_roles", foreign_keys=[updata_user_id])
    # 这个关系允许在Role表中使用create_user 来显示 表User中所有内容
    # 在表User中使用create_role来显示 Role表中所有内容
    # 这个relationship 是orm自己的东西，和oracle无关，是类之间的调用

#
class Menu(BaseModel):
    """
    菜单
    """
    IS_SHOW = (
        (1, '显示'),
        (0, '隐藏')
    )
    MENU_STATUS = (
        (0, '正常'),
        (1, '删除'),
        (2, '停用')
    )
    MENU_TYPE = (
        (0, '菜单'),
        (1, '按钮')
    )
    __tablename__ = 'Menu'

    menu_name = Column(String(255))
    parent_id = Column( Integer, ForeignKey('Menu.id'))
    parent = relationship("Menu", remote_side=[id], backref="Menu")
    menu_href = Column(String(255))
    menu_icon = Column(String(255))
    tree_sort = Column(Integer)
    tree_level = Column(Integer, default=1)
    is_show = Column(Integer, default=1)
    status = Column(Integer, default=0)
    remarks = Column(String(255))
    menu_type = Column(Integer, default=0)