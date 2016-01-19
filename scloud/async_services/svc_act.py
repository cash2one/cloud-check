#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.config import logger
from scloud.celeryapp import celery
from scloud.models.act import Act_History

from scloud.models.base import DataBaseService

act_actions = {
    1: u"新增%s数据",
    2: u"更新%s数据",
    3: u"删除%s数据",
}


@celery.task
def task_act_post(act_type=1, table_name="", table_doc=""):
    logger.info("------[celery task post act]------")
    with DataBaseService({}) as svc:
        act = Act_History()
        act.act_type = act_type
        act.desc = act_actions.get(act_type, u"") % table_doc
        svc.db.add(act)
