#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import os
import requests
from scloud.const import act_actions
from scloud.config import logger, CONF
from scloud.celeryapp import celery
# from scloud.models.act import Act_History, Act_Pro_History
# from scloud.models.base import DataBaseService
# from scloud.shortcuts import render_to_string
# from scloud.utils.publish import publish_notice_checker, publish_notice_user
# 
# 
# @celery.task
# def task_notice_checker(user_id):
#     publish_notice_checker(user_id)
# 
# @celery.task
# def task_notice_user(user_id):
#     publish_notice_user(user_id)
# -*- coding: utf-8 -*-

import simplejson
from scloud.models.base import DataBaseService
from scloud.services.svc_pt_user import PtUserService
from scloud.services.svc_apply_user import ProUserService
from scloud.services.svc_act import ActHistoryService
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
    for user_id in user_ids:
        # 通知审核员
        if user_id == 10:
            logger.info("notice %s success"% user_id)
        publish_tasks(user_id, action)
    # 更新自己任务状态
    publish_tasks(this_id)
    logger.info("#"*30+" [user %s notice_checker tasks finish] "%this_id+"#"*30)
    return True

@celery.task
def publish_notice_user(user_id=0):
    logger.info("#"*30+" [user %s notice_user tasks] "%user_id+"#"*30)
    action = "on_notice_user"
    publish_tasks(user_id, action)
    with DataBaseService({}) as DBSvc:
        svc = PtUserService(DBSvc)
        pt_users_res = svc.get_list()
        user_ids = [u.id for u in pt_users_res.data if "pro_resource_apply.check" in u.get_current_perms()]
    for this_id in user_ids:
        # 通知所有审核员
        publish_tasks(this_id)
    logger.info("#"*30+" [user %s notice_user tasks finish] "%user_id+"#"*30)
    return True

@celery.task
def publish_tasks(user_id, action="on_task"):
    with DataBaseService({"user_id": user_id}) as DBSvc:
        user_svc = PtUserService(DBSvc, {"user_id": user_id})
        pt_user_res = user_svc.get_info()
        if "pro_resource_apply.check" in pt_user_res.data.get_current_perms():
            imchecker = True
        else:
            imchecker = False
        # 获取任务列表
        svc = ActHistoryService(DBSvc, {"user_id": user_id})
        tasks_res = svc.get_res_tasks()
        data = {
            "tasks_res": tasks_res,
            "imchecker": imchecker,
            "STATUS_RESOURCE": STATUS_RESOURCE
        }

        # 获取用户申请列表
        svc = ProUserService(DBSvc, {"user_id": user_id})
        pro_users_res = svc.get_list()
        if imchecker:
            pro_users = [i for i in pro_users_res.data[::-1] if i.status == STATUS_PRO_TABLES.APPLIED]
        else:
            pro_users = [i for i in pro_users_res.data[::-1] if i.status in [STATUS_PRO_TABLES.REFUSED, STATUS_PRO_TABLES.CHECKED]]
        data.update({
            "pro_users": pro_users,
            "imchecker": imchecker,
            "STATUS_PRO_TABLES": STATUS_PRO_TABLES
        })
        logger.info(pro_users)

        # 获取任务列表总和
        total = len(tasks_res.data) + len(pro_users)
        data["total"] = total
        logger.info("tasks length: %s" % len(tasks_res.data))
        logger.info("pro_users length : %s" % len(pro_users))
        logger.info("total: %s" % total)

        chat = {
            "user_id": user_id,
            "action": action,
            "html": render_to_string("admin/notice/tasks.html", **data)
        }
        # logger.info(chat)
        r.publish("test_realtime", simplejson.dumps(chat))
    return True

