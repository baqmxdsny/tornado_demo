#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Author:   chenjh
# @DateTime: 2020-02-28 11:22
# @Software: PyCharm
# @File:     urlparse.py
from importlib import import_module


def include(module):
    '''
        导入包，获取其中数据
    :param module:
    :return:
    '''
    res = import_module(module)
    urls = getattr(res, 'urls', res)
    return urls

def url_wrapper(urls):
    '''
        解析包中数据，进行拼装
    :param urls:
    :return:
    '''
    wrapper_list = []
    for url in urls:
        path, handles = url
        if isinstance(handles.url_patterns, (tuple, list)):
            for handle in handles.url_patterns:
                pattern, handle_class = handle
                wrap = ('{0}{1}'.format(path, pattern), handle_class)
                wrapper_list.append(wrap)
        else:
            wrapper_list.append((path, handles))
    return wrapper_list