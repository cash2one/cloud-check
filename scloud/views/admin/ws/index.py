# -*- coding: utf-8 -*-

import simplejson
from scloud.shortcuts import url
from scloud.shortcuts import env
from scloud.config import logger, logThrown, CONF
from scloud.utils.error_code import ERR
from scloud.handlers import AuthHandler
from tornado.websocket import WebSocketHandler
from scloud.models.base import DataBaseService
from scloud.services.svc_pro_resource_apply import ProResourceApplyService
from scloud.services.svc_pt_user import PtUserService
from scloud.services.svc_act import ActHistoryService
from scloud.const import STATUS_RESOURCE

class MySocketHandler(WebSocketHandler):
    def initialize(self, **kwargs):
        super(MySocketHandler, self).initialize()
    @property
    def args(self):
        return {}
    def render_to_string(self, template, **kwargs):
        tmpl = env.get_template(template)
        s = "&".join(["%s=%s" % (k, v) for k, v in self.args.items() if k not in ["page", "_pjax"]])
        kwargs.update({
            "CONF": CONF,
            "handler": self,
            "request": self.request,
            "reverse_url": self.application.reverse_url,
            "ERR": ERR,
            "s": s+"&" if s else ""
        })
        # logger.info("\t [render_to_string kwargs]: %s" % kwargs)
        template_string = tmpl.render(**kwargs)
        return template_string

@url("/ws/demo", name="ws.demo")
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
        logger.error("====[index onmessage]====")
        self.svc = DataBaseService()
        self.svc.__enter__()
        logger.error("\t WebSocket message: %s" % message)
        json_message = simplejson.loads(message)
        if json_message["action"] == "pro_resource_apply":
            self.do_notice_user(json_message)
        elif json_message["action"] == "notice_checker":
            self.do_notice_checker(json_message)
        elif json_message["action"] == "join":
            self.do_online(json_message)
        elif json_message["action"] == "offline":
            EchoWebSocket.users.pop(str(json_message["user_id"]))
        else:
            self.write_message(u"You said: " + message)
        self.svc.db.commit()
        self.svc.db.close()
        logger.error("====[index finish]====")

    def on_close(self):
        logger.info("WebSocket closed")

    def do_online(self, json_message):
        user_id = json_message["user_id"]
        svc = PtUserService(self, {"user_id": user_id})
        pt_user_res = svc.get_info()
        pt_user = pt_user_res.data
        logger.info("pt_user: %s"% pt_user)
        data = {
            "level": "info",
            "content": u"%s已经上线！" % (pt_user.username or pt_user.email or pt_user.mobile),
        }
        try:
            html = self.render_to_string("admin/notice/online.html", **data)
        except Exception as e:
            logThrown()
            html = ""
        chat = {
            "user_id": pt_user.id,
            "html": html
        }
        chat.update(json_message)
        EchoWebSocket.users.update({user_id: self})
        EchoWebSocket.send_all(chat)
        logger.info("**users: %s" % EchoWebSocket.users)
        # self.on_finish()

    def do_notice_user(self, json_message):
        svc = ProResourceApplyService(self, {"res_id": json_message["res_id"]})
        resource_res = svc.get_resource()
        user_id = resource_res.data.user_id
        svc = ActHistoryService(self, {"user_id": user_id})
        tasks_res = svc.get_res_tasks()
        logger.info(resource_res.data.user_id)
        logger.info(resource_res.data.checker_id)
        data = {
            "tasks_res": tasks_res,
            "imchecker": False,
            "STATUS_RESOURCE": STATUS_RESOURCE
        }
        chat = {
            "user_id": user_id,
            "data": resource_res.data.as_dict(),
            "html": self.render_to_string("admin/notice/tasks.html", **data)
        }
        logger.error(chat)
        chat.update(json_message)
        EchoWebSocket.send_message(chat)
        # self.on_finish()
        # self.write_message(u"You said: " + message)

    def do_notice_checker(self, json_message):
        logger.info("-----------------------------NOTICE CHECKER-----------------------------")
        svc = PtUserService(self)
        pt_users_res = svc.get_list()
        user_ids = [u.id for u in pt_users_res.data if "pro_resource_apply.check" in u.get_current_perms()]

        for user_id in user_ids:
            svc = ActHistoryService(self, {"user_id": user_id})
            tasks_res = svc.get_res_tasks()
            data = {
                "tasks_res": tasks_res,
                "imchecker": True,
                "STATUS_RESOURCE": STATUS_RESOURCE
            }
            chat = {
                "user_id": user_id,
                "html": self.render_to_string("admin/notice/tasks.html", **data)
            }
            chat.update(json_message)
            logger.error(chat)
            EchoWebSocket.send_message(chat)
        # self.on_finish()
        # self.write_message(u"You said: " + message)
