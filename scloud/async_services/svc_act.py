#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.config import CONF, cache, logger
from scloud.celeryapp import celery
from scloud.models.act import Act_History
# from scloud.models.project import Pro_Info
from scloud.models.base import DataBaseService
from sqlalchemy import func, and_, or_, event
from datetime import datetime


@celery.task
def task_act_post():
    logger.info("------[celery task post act]------")
    with DataBaseService({}) as svc:
        act = Act_History()
        act.act_type = 1
        act.desc = u"添加数据"
        svc.db.add(act)


# def act_post(mapper, connect, target):
#     logger.info("-----[after_insert act_post]------")
#     logger.info(target.__class__.__name__)
#     logger.info(target.__doc__)
#     task_act_post.delay(target)
# event.listen(Pro_Info, 'after_insert', act_post)
