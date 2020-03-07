#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    时间教会了我们很多东西，有些我们曾经认为根本没有的，后来发现它确确实实存在，有些我们深信不疑的，后来却明白根本就没有。
'''
import tornado.httpserver
import tornado.ioloop
import tornado.web
from sqlalchemy.orm import scoped_session, sessionmaker
from tornado.options import options

from settings import settings, db_engine
from urls import url_patterns

class TornadoBoilerplate(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, handlers=url_patterns, **settings)
        self.orm_db = scoped_session(sessionmaker(bind=db_engine,
                                              autocommit=True, autoflush=True,
                                              expire_on_commit=False))
        # self.orm_db = orm_db_session()


def main():
    app = TornadoBoilerplate()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
