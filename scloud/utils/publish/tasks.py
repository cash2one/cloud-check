# -*- coding: utf-8 -*-

import simplejson
from scloud.models.base import DataBaseService
from scloud.services.svc_pt_user import PtUserService
from scloud.services.svc_act import ActHistoryService
from scloud.const import STATUS_RESOURCE
from scloud.shortcuts import render_to_string
from scloud.utils.publish.base import r


def publish_notice_tasks(action, user_id=0, this_id=0):
    # user_id = self.args.get("user_id")
    user_ids = []
    # action = self.args.get("action")
    if action == "on_notice_user":
        user_ids.append(user_id)
        # imchecker = False
    elif action == "on_notice_checker":
        with DataBaseService({}) as DBSvc:
            svc = PtUserService(DBSvc)
            pt_users_res = svc.get_list()
            user_ids = [u.id for u in pt_users_res.data if "pro_resource_apply.check" in u.get_current_perms()]
            # imchecker = True

    for user_id in user_ids:
        publish_tasks(user_id)

    publish_tasks(this_id)
    return True

def publish_tasks(user_id):
    with DataBaseService({"user_id": user_id}) as DBSvc:
        user_svc = PtUserService(DBSvc, {"user_id": user_id})
        pt_user_res = user_svc.get_info()
        if "pro_resource_apply.check" in pt_user_res.data.get_current_perms():
            imchecker = True
        else:
            imchecker = False
        svc = ActHistoryService(DBSvc, {"user_id": user_id})
        tasks_res = svc.get_res_tasks()
        data = {
            "tasks_res": tasks_res,
            "imchecker": imchecker,
            "STATUS_RESOURCE": STATUS_RESOURCE
        }
        chat = {
            "user_id": user_id,
            "action": "on_task",
            "html": render_to_string("admin/notice/tasks.html", **data)
        }
        r.publish("test_realtime", simplejson.dumps(chat))
    return True

