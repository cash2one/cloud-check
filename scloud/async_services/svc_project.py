#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

from scloud.config import logger
from scloud.celeryapp import celery
from scloud.models.project import Pro_Info
from scloud.models.base import DataBaseService


@celery.task
def get_project_list(kwargs={}):
    logger.info("------[celery task get_project_list]------")
    with DataBaseService(kwargs) as svc:
        projects = svc.db.query(Pro_Info).all()
        project_list = [i.as_dict() for i in projects]
        logger.info("project_list")
        res = {
            "return_code": 0,
            "return_message": "",
            "data": project_list
        }
    return res
