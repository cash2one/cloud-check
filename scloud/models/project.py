#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from os.path import abspath, dirname, join
current_path = abspath(dirname(__file__))
import sys
sys.path.insert(0, join(current_path, '..', ".."))
sys.path.insert(0, join(current_path, '..'))
# sys.path.insert(0, current_path)
from pprint import pprint
# pprint(sys.path)
from scloud.models.act import Act_History
from scloud.models.base import BaseModel, BaseModelMixin, DataBaseService, DBSession
from scloud.config import logger, logThrown
from sqlalchemy import Column, func, event
from sqlalchemy.types import Unicode, Integer, Float, DateTime
from scloud.async_services.svc_act import task_act_post


class Pro_Info(BaseModel, BaseModelMixin):
    # u"""项目信息表"""
    __tablename__ = "pro_info"
    name = Column(Unicode, default=u'')
    owner_id = Column(Integer, default=0)
    env_id = Column(Integer, default=0)
    desc = Column(Unicode, default=u'')

    # def __commit_insert__(self):
    #     logger.info("-----[post_act_history.2]------")
    #     try:
    #         # act_history = Act_History()
    #         # act_history.act_type = 1
    #         # act_history.desc = u"新增变更"
    #         # DBSession.add(act_history)
    #         # DBSession.commit()
    #         # DBSession.remove()
    #         # DBSession.close()
    #         with DataBaseService({}) as svc:
    #             act_history = Act_History()
    #             act_history.act_type = 1
    #             act_history.desc = u"新增变更"
    #             svc.db.add(act_history)
    #     except:
    #         logger.info("-----[ERROR post_act_history]------")
    #         logThrown()


class Pro_Resource_Apply(BaseModel, BaseModelMixin):
    __tablename__ = "pro_resource_apply"
    computer = Column(Integer, default=0)
    cpu = Column(Integer, default=0)
    memory = Column(Integer, default=0)
    disk = Column(Integer, default=0)
    disk_backup = Column(Integer, default=0)
    out_ip = Column(Integer, default=0)
    snapshot = Column(Integer, default=0)
    loadbalance = Column(Integer, default=0)
    internet_ip = Column(Integer, default=0)
    internet_ip_ssl = Column(Integer, default=0)
    desc = Column(Unicode, default=u'创建项目')
    start_time = Column(DateTime, default=func.now())
    period = Column(Integer, default=0)
    due_time = Column(DateTime, default=func.now())
    fee_current_mouth = Column(Float, default=0.00)
    fee_total = Column(Float, default=0.00)
    fee_desc = Column(Unicode, default=u'')


class Pro_Environment(BaseModel, BaseModelMixin):
    __tablename__ = "pro_environment"
    name = Column(Unicode, unique=True, default=u'')
    desc = Column(Unicode, default=u'')


class Pro_Internet_Ip_Types(BaseModel, BaseModelMixin):
    __tablename__ = "pro_internet_ip_types"
    name = Column(Unicode, unique=True, default=u'')
    desc = Column(Unicode, default=u'')


def act_post(mapper, connect, target):
    logger.info("-----[after_insert act_post]------")
    logger.info(target.__class__.__name__)
    logger.info(target.__doc__)
    task_act_post.delay()
event.listen(Pro_Info, 'after_insert', act_post)


if __name__ == '__main__':
    import uuid
    logger.info("-----[0 post_act_history]------")
    # try:
    with DataBaseService({}) as svc:
        proj = Pro_Info()
        proj.name = unicode(uuid.uuid4())
        proj.env_id = 1
        proj.user_id = 0
        proj.desc = u"123123"
        svc.db.add(proj)
        # proj = Pro_Info()
        # proj.name = unicode(uuid.uuid4())
        # proj.env_id = 1
        # proj.user_id = 0
        # proj.desc = u"123123"
        # DBSession.add(proj)
        # DBSession.commit()
    # except:
    #     logger.info("-----[0.ERROR post_act_history]------")
    #     logThrown()
