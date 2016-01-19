#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import simplejson
import _mysql_exceptions
from datetime import datetime
from torweb.db import CacheQuery
from scloud.config import CONF, logger
from sqlalchemy import event
from sqlalchemy import Column, func
from sqlalchemy.exc import DisconnectionError
from sqlalchemy import create_engine, MetaData
from sqlalchemy.types import Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


db_engine = create_engine(
    CONF("DB.CONNECTION_STRING"),
    echo=False,
    pool_size=100,
    pool_recycle=3600,
    isolation_level='REPEATABLE READ',
)


def my_on_checkout(dbapi_conn, connection_rec, connection_proxy):
    try:
        dbapi_conn.cursor().execute('select now()')
    except _mysql_exceptions.OperationalError:
        raise DisconnectionError


class ModelServiceMixin(object):

    @staticmethod
    def __get_pagination_and_items(query, page=1, pagesize=10):
        pagination = Pagination(page, pagesize, query.count())
        items = query.offset(pagination.start_num).limit(pagesize)
        return pagination, items

    def get_page_items(self, ModelCls, page=1, pagesize=10):
        query = self.db.query(ModelCls).order_by(ModelCls.id.desc())
        return self.__get_pagination_and_items(query, page, pagesize)

    def get_by_pk(cls, ModelCls, pk):
        return cls.db_session.query(ModelCls).filter(ModelCls.id == pk).first()


class DataBaseService(ModelServiceMixin):
    event.listen(db_engine, 'checkout', my_on_checkout)
    db_session = __DB_Session = scoped_session(
        sessionmaker(bind=db_engine, query_cls=CacheQuery, expire_on_commit=False, autoflush=False))
    meta_data = MetaData(bind=db_engine)

    def __init__(self, param_dict):
        self.param_dict = param_dict
        self.db = None

    def _db_init(self):
        self.db = self.__class__.__DB_Session

    def __enter__(self):
        logger.info("====[ENTER]====")
        self._db_init()
        return self

    def __exit__(self, *args):
        logger.info("====[EXIT]====")
        if isinstance(args[1], Exception):
            self.db.rollback()
            logger.info("====[ROLLBACK]====")
        else:
            self.db.commit()
            # self.db.flush()
            logger.info("====[COMMIT]====")
        self.db.remove()
        self.db.close()
        logger.info("====[CLOSE]====")

    def db_flush(self):
        self.db.flush()  # write to database

    def db_commit(self):
        self.db.commit()


BaseModel = declarative_base()


class BaseModelMixin(object):
    id = Column(Integer, autoincrement=True, primary_key=True)
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, default=func.now(), onupdate=func.now())

    json_columns = []

    def dump_column(self, column_name):
        value = getattr(self, column_name)
        column_value = value.encode("utf-8") if type(value) == str else value
        if column_name in self.json_columns:
            try:
                column_value = simplejson.loads(value)
            except:
                column_value = value
        if type(value) == datetime:
            column_value = value.strftime("%Y-%m-%d %H:%M:%S")
        return column_value

    def as_dict(self, col_name_list=[]):
        data = {}
        if len(col_name_list) > 0:
            for i, c in enumerate(self.__table__.columns):
                if c.name not in col_name_list:
                    continue
                if not hasattr(self, c.name):
                    continue
                data[c.name] = self.dump_column(c.name)
        else:
            for c in self.__table__.columns:
                data[c.name] = self.dump_column(c.name)
        return data