#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import simplejson
import _mysql_exceptions
from datetime import datetime
from torweb.db import CacheQuery
from scloud.config import CONF, logger, logThrown
from sqlalchemy import event
from sqlalchemy import Column, func
from sqlalchemy.sql import ClauseElement
from sqlalchemy.exc import DisconnectionError
from sqlalchemy import create_engine, MetaData
from sqlalchemy.types import Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from tornado_mysql import pools


db_engine = create_engine(
    CONF("DB.CONNECTION_STRING"),
    echo=False,
    pool_size=100,
    pool_recycle=3600,
    encoding="utf-8",
    isolation_level='REPEATABLE READ',
)

MYSQL_POOL = pools.Pool(dict(host='127.0.0.1', port=3306, user='scloud', passwd='scloud', db='scloud'), max_idle_connections=5, max_open_connections=10)


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
        sessionmaker(bind=db_engine, query_cls=CacheQuery, expire_on_commit=False, autoflush=False, autocommit=True))
    meta_data = MetaData(bind=db_engine)
    # db_session = __DB_Session = sessionmaker(bind=db_engine, query_cls=CacheQuery, expire_on_commit=False, autoflush=False, autocommit=True)

    def __init__(self, param_dict={}):
        self.param_dict = param_dict
        self.db = None

    def _db_init(self):
        self.db = self.__class__.__DB_Session()
        if CONF("DB.ENGINE").lower() == "myisam":
            try:
                self.db.begin()
                logger.info("====[begin transaction]====")
            except:
                logThrown()
        logger.info("====[INIT DB, DB.BEGIN]====")

    def __enter__(self):
        logger.info("====[ENTER]====")
        self._db_init()
        # self.db.begin()
        return self

    def __exit__(self, *args):
        logger.info(args)
        logger.info("====[EXIT]====")
        if isinstance(args[1], Exception):
            self.db.rollback()
            logger.info("====[ROLLBACK]====")
        else:
            self.db.commit()
            # self.db.flush()
            logger.info("====[COMMIT]====")
        # self.db.remove()
        self.db.close()
        logger.info("====[CLOSE]====")

    def db_flush(self):
        self.db.flush()  # write to database

    def db_commit(self):
        self.db.commit()


BaseModel = declarative_base()


class BaseModelMixin(object):
    __table_args__ = {'mysql_engine': CONF('DB.ENGINE')}
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

    @classmethod
    def get_or_create(cls, **kwargs):
        with DataBaseService({}) as svc:
            logger.info("============== [kwargs] ==============")
            logger.info(kwargs)
            instance = svc.db.query(cls).filter_by(**kwargs).first()
            logger.info("============== [instance] ==============")
            logger.info(instance)
            if instance:
                # 已有，无需创建
                created = False
            else:
                # 没有，需新创建
                params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
                logger.info("============== [kwargs] ==============")
                logger.info(kwargs)
                logger.info("============== [params] ==============")
                logger.info(params)
                instance_res = cls(**params)
                svc.db.add(instance_res)
                svc.db.flush()
                instance = svc.db.query(cls).filter_by(**kwargs).first()
                logger.info("instance for create result")
                logger.info(instance)
                created = True
        return instance, created

    @classmethod
    def get_or_create_obj(cls, db, **kwargs):
        logger.info("============== [kwargs] ==============")
        logger.info(kwargs)
        instance = db.query(cls).filter_by(**kwargs).first()
        logger.info("============== [instance] ==============")
        logger.info(instance)
        if instance:
            # 已有，无需创建
            created = False
        else:
            # 没有，需新创建
            params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
            logger.info("============== [kwargs] ==============")
            logger.info(kwargs)
            logger.info("============== [params] ==============")
            logger.info(params)
            instance_res = cls(**params)
            db.add(instance_res)
            db.flush()
            instance = db.query(cls).filter_by(**kwargs).first()
            logger.info("instance for create result")
            logger.info(instance)
            created = True
        return instance, created
