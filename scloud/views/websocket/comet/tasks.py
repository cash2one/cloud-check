# -*- coding: utf-8 -*-

import os
import scloud
import simplejson
from scloud.handlers import Handler, AuthHandler
from scloud.shortcuts import url
from scloud.config import CONF, logger
from tornado import gen
from tornado.web import asynchronous
from tornado.websocket import websocket_connect
from scloud.utils.unblock import unblock
from scloud.views.admin.ws.pubsub import r
from scloud.services.svc_pro_resource_apply import ProResourceApplyService
from scloud.services.svc_pt_user import PtUserService
from scloud.services.svc_act import ActHistoryService
from scloud.const import STATUS_RESOURCE

ws_host = CONF("WS_HOST")

@url("/comet/online", name="comet.online")
class CometTaskHandler(Handler):
    @asynchronous
    @gen.coroutine
    def get(self):
        user_id = self.args.get("user_id")
        ws = yield websocket_connect(os.path.join(ws_host, self.reverse_url("ws.comet")[1:]))
        ws.write_message(simplejson.dumps({
            "action": "online",
            "user_id": user_id
        }))
        raise gen.Return(ws.read_message())


@url("/comet/tasks", name="comet.tasks")
class CometTaskHandler(Handler):
    @unblock
    def post(self):
        self.get()

    @unblock
    def get(self):
        logger.info("*"*20)
        logger.info("----------------self.current_user------------------")
        user_id = self.args.get("user_id")
        user_ids = []
        action = self.args.get("action")
        if action == "on_notice_user":
            user_ids.append(user_id)
            imchecker = False
        else:
            svc = PtUserService(self)
            pt_users_res = svc.get_list()
            user_ids = [u.id for u in pt_users_res.data if "pro_resource_apply.check" in u.get_current_perms()]
            imchecker = True

        for user_id in user_ids:
            res_id = self.args.get("res_id")
            svc = ActHistoryService(self, {"user_id": user_id})
            tasks_res = svc.get_res_tasks()
            data = {
                "tasks_res": tasks_res,
                "imchecker": imchecker,
                "STATUS_RESOURCE": STATUS_RESOURCE
            }
            chat = {
                "user_id": user_id,
                "action": "on_task",
                "html": self.render_to_string("admin/notice/tasks.html", **data)
            }
            r.publish("test_realtime", simplejson.dumps(chat))
        logger.info("*"*20)
        this_id = self.args.get("this_id")
        svc = ActHistoryService(self, {"user_id": this_id})
        tasks_res = svc.get_res_tasks()
        data = {
            "tasks_res": tasks_res,
            "imchecker": False if imchecker else True,
            "STATUS_RESOURCE": STATUS_RESOURCE
        }
        chat = {
            "user_id": this_id,
            "action": "on_task",
            "html": self.render_to_string("admin/notice/tasks.html", **data)
        }
        r.publish("test_realtime", simplejson.dumps(chat))
        return simplejson.dumps({"success": True})

