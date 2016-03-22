# -*- coding: utf-8 -*-

import threading
import simplejson
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import redis
from scloud.shortcuts import url
from scloud.config import logger, logThrown
from scloud.views.admin.ws.index import MySocketHandler


LISTENERS = dict()

r = redis.Redis(host='127.0.0.1', db=2)


def redis_listener():
    p = r.pubsub()
    p.subscribe('test_realtime')
    for message in p.listen():
        message_data = unicode(message['data'])
        json_message = simplejson.loads(message_data, encoding="utf-8")
        logger.info(json_message)
        if isinstance(json_message, dict) and "user_id" in json_message.keys():
            user = LISTENERS.get(str(json_message["user_id"]))
            if user:
                user.write_message(unicode(message_data))
        else:
            for element in LISTENERS.values():
                element.write_message(unicode(message['data']))


# class NewMsgHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write(TEMPLATE)
# 
#     def post(self):
#         data = self.request.arguments['data'][0]
#         r = redis.Redis(host='127.0.0.1', db=2)
#         r.publish('test_realtime', data)
        

@url("/ws/pubsub", name="ws.pubsub")
class RealtimeHandler(MySocketHandler):
    def check_origin(self, origin):
        return True
    def open(self, *args, **kwargs):
        self.user_id = self.get_argument("user_id", 0)
        LISTENERS[str(self.user_id)] = self
        logger.info(LISTENERS)

    def on_message(self, message):
        pass

    def on_close(self):
        del LISTENERS[str(self.user_id)]

