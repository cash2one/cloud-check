# -*- coding: utf-8 -*-

import os
import requests
import threading
import simplejson
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import redis
from scloud.shortcuts import url
from scloud.config import logger, logThrown, CONF
from scloud.views.admin.ws.index import MySocketHandler
from scloud.utils.publish.base import r
# from scloud.utils.publish.tasks import publish_tasks
from scloud.async_services.publish_task import publish_tasks
# from scloud.utils.publish.publish_pro_user import publish_pro_user
# from scloud.const import STATUS_PRO_TABLES


LISTENERS = dict()


def redis_listener():
    p = r.pubsub()
    p.subscribe('test_realtime')
    for message in p.listen():
        message_data = unicode(message['data'])
        json_message = simplejson.loads(message_data, encoding="utf-8")
        # logger.info(json_message)
        if isinstance(json_message, dict) and "user_id" in json_message.keys():
            user = LISTENERS.get(str(json_message["user_id"]))
            if user:
                user.write_message(unicode(message_data))
        else:
            for element in LISTENERS.values():
                element.write_message(unicode(message['data']))


@url("/ws/pubsub", name="ws.pubsub")
class RealtimeHandler(MySocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        self.user_id = self.get_argument("user_id", 0)
        LISTENERS[str(self.user_id)] = self
        logger.info(LISTENERS)
        # data = {
        #     "this_id": self.user_id
        # }
        # params = "&".join(["%s=%s" % (k, v) for k, v in data.items()])
        logger.info("#" * 30 + " [user %s init tasks] " % self.user_id + "#" * 30)
        # request_result = publish_tasks(self.user_id)
        request_result = publish_tasks.delay(self.user_id)
        # logger.info(request_result)
        logger.info("#" * 30 + " [user %s init tasks finished] %s " % (self.user_id, request_result) + "#" * 30)

    def on_message(self, message):
        # if message == "on_init_profile_tasks":
        #     logger.info("#"*30+" [user %s %s] "%(self.user_id, message)+"#"*30)
        #     # request_result = publish_tasks(self.user_id)
        #     request_result = publish_tasks.delay(self.user_id, action="on_init_profile_tasks", template="admin/notice/profile_tasks.html")
        #     logger.info(request_result)
        #     logger.info("#"*30+" [user %s %s finished] "%(self.user_id, message)+"#"*30)
        pass

    def on_close(self):
        del LISTENERS[str(self.user_id)]
