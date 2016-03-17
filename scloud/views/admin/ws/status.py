# -*- coding: utf-8 -*-

import simplejson
from scloud.shortcuts import url
from scloud.config import logger, logThrown
from scloud.handlers import AuthHandler
from tornado.websocket import WebSocketHandler
from scloud.models.base import DataBaseService
from scloud.services.svc_pro_resource_apply import ProResourceApplyService
from scloud.services.svc_pt_user import PtUserService
from scloud.services.svc_act import ActHistoryService
from scloud.const import STATUS_RESOURCE
from scloud.views.admin.ws.index import MySocketHandler

# class MySocketHandler(WebSocketHandler):
#     def initialize(self, **kwargs):
#         super(MySocketHandler, self).initialize()
#         # self.svc = DataBaseService()
#         # self.svc.__enter__()
#         logger.info("==[initialize]==")

@url("/ws/status", name="ws.status")
class EchoWebSocket(MySocketHandler):
    users = dict()
    def check_origin(self, origin):
        return True

    def open(self):
        logger.info("WebSocket opened")
        # current_user = self.current_user
        # from code import interact
        # interact(local=locals())
        # EchoWebSocket.users.update({current_user.id: self})

    @classmethod
    def send_message(cls, chat):
        waiter = cls.users.get(str(chat["user_id"]))
        if waiter:
            waiter.write_message(simplejson.dumps(chat))

    @classmethod
    def send_all(cls, chat):
        for waiter in cls.users.values():
            waiter.write_message(simplejson.dumps(chat))

    def on_message(self, message):
        logger.error("====[status onmessage]====")
        self.svc = DataBaseService()
        self.svc.__enter__()
        logger.error("\t WebSocket message: %s" % message)
        json_message = simplejson.loads(message)
        if json_message["action"] == "init_status":
            # svc = ProResourceApplyService(self, {"res_id": json_message["res_id"]})
            # resource_res = svc.get_resource()
            # user_id = resource_res.data.user_id
            user_id = json_message["user_id"]
            svc = PtUserService(self, {"user_id": user_id})
            pt_user_res = svc.get_info()
            if pt_user_res.return_code == 0:
                current_perms = pt_user_res.data.get_current_perms()
                if "pro_resource_apply.view" in current_perms:
                    imchecker = False
                else:
                    imchecker = True
                svc = ActHistoryService(self, {"user_id": user_id})
                tasks_res = svc.get_res_tasks()
                data = {
                    "tasks_res": tasks_res,
                    "imchecker": imchecker,
                    "STATUS_RESOURCE": STATUS_RESOURCE
                }
                chat = {
                    "user_id": user_id,
                    "task_html": self.render_to_string("admin/notice/tasks.html", **data)
                }
                chat.update(json_message)
                logger.error(chat)
                self.write_message(chat)
            # self.on_finish()
            # chat.update(json_message)
            # EchoWebSocket.send_message(chat)
            # self.write_message(u"You said: " + message)
        elif json_message["action"] == "offline":
            EchoWebSocket.users.pop(str(json_message["user_id"]))
        else:
            self.write_message(u"You said: " + message)
        self.svc.db.commit()
        self.svc.db.close()
        logger.error("====[status finish]====")

    def on_close(self):
        logger.info("WebSocket closed")
