#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.const import act_actions
from scloud.config import logger
from scloud.celeryapp import celery
from scloud.models.act import Act_History
from scloud.models.base import DataBaseService


@celery.task
def task_act_post(act_type=1, table_name="", table_doc=""):
    logger.info("------[celery task post act]------")
    logger.info("------[ act type %s ]------" % act_type)
    with DataBaseService({}) as svc:
        act = Act_History()
        act.act_type = act_type
        act.desc = act_actions[act_type].value % table_doc
        svc.db.add(act)
