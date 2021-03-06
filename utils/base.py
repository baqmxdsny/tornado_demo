import json
import tornado.web
from settings import db_engine, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

import logging
logger = logging.getLogger('boilerplate.' + __name__)

class NoResultError(Exception):
    pass

class BaseHandler(tornado.web.RequestHandler):
    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """
    @property
    def db(self):
        return self.application.orm_db

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.

        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                    "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg

    def row_to_obj(self, row, execute):
        """Convert a SQL row to an object supporting dict and attribute access."""
        obj = tornado.util.ObjectDict()
        for val, desc in zip(row, execute.cursor.description):
            obj[desc.name] = val
        return obj

    async def execute(self, stmt, *args):
        """Execute a SQL statement.
        Must be called with ``await self.execute(...)``
        """
        execute = self.db.execute(stmt, args)

    def query(self, stmt, *args):
        """Query for a list of results.
        Typical usage::
            results = await self.query(...)
        Or::
            for row in await self.query(...)
        """
        execute = self.db.execute(stmt, args)
        list = self.dictfetchall(execute)
        execute.close()
        return list

    def insert(self, stmt, *args):
        """Query for a list of results.
        Typical usage::
            results = await self.query(...)
        Or::
            for row in await self.query(...)
        """
        execute = self.db.execute(stmt, args)
        return execute
        # event_id = execute.lastrowid
        # return event_id

    async def queryone(self, stmt, *args):
        """Query for exactly one result.
        Raises NoResultError if there are no results, or ValueError if
        there are more than one.
        """
        results = await self.query(stmt, *args)
        if len(results) == 0:
            raise NoResultError()
        elif len(results) > 1:
            raise ValueError("Expected 1 result, got %d" % len(results))
        return results[0]

    async def prepare(self):
        # get_current_user cannot be a coroutine, so set
        # self.current_user in prepare instead.
        user_id = self.get_secure_cookie("blogdemo_user")
        if user_id:
            self.current_user = await self.queryone(
                "SELECT * FROM authors WHERE id = %s", int(user_id)
            )

    async def any_author_exists(self):
        return bool(await self.query("SELECT * FROM authors LIMIT 1"))

    def dictfetchall(self, execute):
        "将游标返回的结果保存到一个字典对象中"
        desc = execute.cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in execute.fetchall()
        ]


class BaseModel(Base):
    '''
        ORM模型基类

    '''
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, default=datetime.now)  # 该字段创建时间属性,不可被修改
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 该字段每一次更新数据,就会给出时间
