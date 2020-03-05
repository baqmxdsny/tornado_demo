#!/usr/bin/env python

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
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))



def main():
    app = TornadoBoilerplate()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
