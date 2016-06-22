#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import os
import requests
import simplejson
from scloud.const import act_actions
from scloud.config import logger, CONF
from scloud.celeryapp import celery
from scloud.models.base import DataBaseService
from scloud.services.svc_pt_user import PtUserService
from scloud.services.svc_act import ActHistoryService
from scloud.services.svc_apply_user import ProUserService
from scloud.services.svc_apply_publish import ApplyPublish
from scloud.services.svc_apply_balance import ApplyLoadBalance
from scloud.services.svc_apply_backups import ApplyBackups
from scloud.pubs.pub_tasks import TaskPublish
from scloud.const import STATUS_RESOURCE, STATUS_PRO_TABLES
from scloud.shortcuts import render_to_string
from scloud.utils.publish.base import r
from scloud.config import logger


@celery.task
def publish_notice_checker(this_id=0):
    # 获取审核员列表
    logger.info("#"*30+" [user %s notice_checker tasks] "%this_id+"#"*30)
    action = "on_notice_checker"
    with DataBaseService({}) as DBSvc:
        svc = PtUserService(DBSvc)
        pt_users_res = svc.get_list()
        user_ids = [u.id for u in pt_users_res.data if "pro_resource_apply.check" in u.get_current_perms()]
        pub_svc = TaskPublish(DBSvc)
        for user_id in user_ids:
            # 通知审核员
            if user_id == 10:
                logger.info("notice %s success"% user_id)
            pub_svc.publish_tasks(user_id, action=action)
        # 更新自己任务状态
        pub_svc.publish_tasks(this_id)
        logger.info("#"*30+" [user %s notice_checker tasks finish] "%this_id+"#"*30)
    return True

@celery.task
def publish_notice_user(user_id=0):
    logger.info("#"*30+" [user %s notice_user tasks] "%user_id+"#"*30)
    action = "on_notice_user"
    with DataBaseService({}) as DBSvc:
        svc = PtUserService(DBSvc)
        pt_users_res = svc.get_list()
        user_ids = [u.id for u in pt_users_res.data if "pro_resource_apply.check" in u.get_current_perms()]
        pub_svc = TaskPublish(DBSvc)
        pub_svc.publish_tasks(user_id, action=action)
        for this_id in user_ids:
            # 通知所有审核员
            pub_svc.publish_tasks(this_id)
        logger.info("#"*30+" [user %s notice_user tasks finish] "%user_id+"#"*30)
    return True

@celery.task
def publish_tasks(user_id, action="on_task", template="admin/notice/tasks.html"):
    with DataBaseService({"user_id": user_id}) as DBSvc:
        pub_svc = TaskPublish(DBSvc)
        pub_svc.publish_tasks(user_id)
    return True

