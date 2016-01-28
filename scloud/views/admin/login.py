# -*- coding: utf-8 -*-

from torweb.urls import url
from scloud.config import logger
from scloud.handlers import Handler
from tornado.web import asynchronous
from tornado import gen


@url("/login", name="login", active="login")
class LoginHandler(Handler):
    u'登录'
    @asynchronous
    @gen.coroutine
    def get(self):
        raise gen.Return(self.render("admin/login.html"))

    @asynchronous
    @gen.coroutine
    def post(self):
        pass