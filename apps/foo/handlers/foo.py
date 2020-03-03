import time

import tornado
import asyncio

from utils.base import BaseHandler
from tornado import gen, web

from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
import tcelery
from apps.foo import tasks

import logging
logger = logging.getLogger('boilerplate.' + __name__)

tornado.options.parse_command_line()
tcelery.setup_nonblocking_producer()

class FooHandler(BaseHandler):
    def get(self):
        raise tornado.web.HTTPError(403)
        self.write({
            'a':'dddd',
            'b': 'ffff'
        })


class SyncSleepHandler(BaseHandler):
    """
    同步的方式,一个延时10s的接口
    """
    def get(self):
        print(3)
        time.sleep(10)
        print(4)
        self.write("when i sleep 10s")


class SleepHandler(BaseHandler):
    """
    异步的延时10秒的接口
    """
    @gen.coroutine
    def get(self):
        print(1)
        yield gen.sleep(10)
        print(2)
        self.write("when i sleep 10s")


class NoSleepHandler(BaseHandler):
    """
    time库不支持Tornado异步
    """
    @gen.coroutine
    def get(self):
        print(5)
        yield time.sleep(5)
        print(6)
        self.write("when i sleep 10s")


class ThreadSleepHandler(BaseHandler):
    """
    time库不支持Tornado异步
    """
    # 必须定义一个executor的属性，然后run_on_executor 注解才管用。
    executor = ThreadPoolExecutor(max_workers=4)

    @gen.coroutine
    def get(self):
        print(5)
        yield self.sleep_fun()
        print(6)
        self.write("when i sleep 10s")

    @run_on_executor
    def sleep_fun(self):
        time.sleep(5)


class CelerySleepHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        print(7)
        response = yield gen.Task(tasks.sleep_fun.apply_async, args=[5])
        print(8)

        self.write("when i sleep 10s")

class AsynchronousSleepHandler(BaseHandler):


    async def get(self):
        print(5)
        await asyncio.sleep(5)
        print(6)
        self.write("when i sleep 10s")



