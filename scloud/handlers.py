#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import urllib
import urlparse
import functools
import simplejson
from tornado.web import HTTPError
from tornado import gen
from torweb.handlers import BaseHandler
from scloud.shortcuts import env
from scloud.config import CONF, logger
from scloud.models.base import DataBaseService
from scloud.async_services.svc_act import task_post_action


class HandlerMeta(type):
    """
     asynchronous handler meta class
    """
    __ASYNC_HANDLER = ('post', 'get',)  # 必须加逗号

    def __new__(mcs, name, bases, dct):
        for method in mcs.__ASYNC_HANDLER:
            if method in dct:
                # 检查url地址中的不合法参数，防跨域调用js
                # 检查函数运行时错误，遇到错误直接抛出
                pass
        return type.__new__(mcs, name, bases, dct)


class Handler(BaseHandler):
    __metaclass__ = HandlerMeta

    def __str__(self):
        return self.__doc__ or self.__class__.__name__

    def init_messages(self):
        if "messages" not in self.session:
            self.session["messages"] = []
        self.messages = self.session.get("messages", [])
        self.save_session()

    def add_message(self, content, level="info"):
        self.post_action(content=content, level=level)
        self.session["messages"].append({"level": level, "content": content})
        self.session["messages_request"] = len(self.session["messages"])
        self.save_session()

    def post_action(self, content="", level="info"):
        current_user = self.session.get("current_user")
        if current_user:
            user_id = current_user.id
        else:
            user_id = 0
        task_post_action.delay(act_type=1, content=content, user_id=user_id)

    def get_messages(self):
        self.messages = self.session["messages"]
        self.session["messages"] = []
        self.save_session()
        return self.messages

    def on_finish(self):
        logger.info("====================== [http method (%s)] ======================" % self.request.method)
        self.svc.db.remove()
        self.svc.db.close()
        logger.info("====================== [finish] ======================")

    def prepare(self):
        self.svc = DataBaseService()
        self.svc._db_init()
        logger.info("====================== [http method] ======================")
        logger.info(self.request.method)
        logger.info("====================== [args] ======================")
        logger.info(self.args)
        self.init_messages()
        self.pjax = self.request.headers.get("X-PJAX")

    def render_to_string(self, template, **kwargs):
        tmpl = env.get_template(template)
        kwargs.update({
            "CONF": CONF,
            "handler": self,
            "request": self.request,
            "reverse_url": self.application.reverse_url
        })
        template_string = tmpl.render(**kwargs)
        return template_string

    def render(self, template, **kwargs):
        if self.pjax:
            title = self.__doc__ or self.__class__.__name__
            title = title.encode("utf-8")
            self.set_header("title", urllib.quote(title))
            self.set_header("active", self.kwargs.get("active", ""))
            template_string = self.render_to_string("%s_pjax.html" % template.split(".html")[0], **kwargs)
        else:
            template_string = self.render_to_string(template, **kwargs)
        logger.info(kwargs)
        self.write(template_string.strip())

    # @gen.coroutine
    def get_error_html(self, status_code, **kwargs):
        logger.info(kwargs)
        exception = kwargs["exception"]
        traceback = kwargs["traceback"]
        self.render("admin/error/500.html", status_code=status_code, exception=exception, traceback=traceback)


def authenticated(method):
    """Decorate methods with this to require that the user be logged in."""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "HEAD", "POST",):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urllib.urlencode(dict(next=next_url))
                headers = self.request.headers
                x_requested_with = headers.get("X-Requested-With", "")
                if x_requested_with == "XMLHttpRequest":
                    logger.info("return simplejson data: SESSION_FAILD")
                    if headers.get("X-PJAX"):
                        self.redirect(url)
                    else:
                        return self.write(simplejson.dumps(
                            {"return_code": -231030, "return_message": u"对不起会话已失效，请重新登录",
                             "data": {"redirect_url": url}}))
                else:
                    self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)

    return wrapper


class AuthHandlerMeta(HandlerMeta):
    """
     asynchronous handler meta class
    """
    __ASYNC_HANDLER = ('post', 'get', 'head')  # 必须加逗号

    def __new__(mcs, name, bases, dct):
        HandlerMeta.__new__(mcs, name, bases, dct)
        for method in mcs.__ASYNC_HANDLER:
            if method in dct:
                dct[method] = authenticated(dct[method])
        return type.__new__(mcs, name, bases, dct)


class AuthHandler(Handler):
    __metaclass__ = AuthHandlerMeta

    # def __init__(self, application, request, **kwargs):
    # super(AuthHandler, self).__init__(application, request, **kwargs)
    # self.current_perms = None

    def prepare(self):
        super(AuthHandler, self).prepare()
        self.expire_session()

    def get_current_user(self):
        current_user = self.session.get("current_user", None)
        logger.info("******[GET SESSION] %s" % current_user)
        # if current_user:
        #     user_roles = current_user.user_roles
        #     for user_role in user_roles:
        #         logger.info(user_role.role)
        return self.session.get("current_user", None)

    def get_login_url(self):
        redirect_url = self.reverse_url("login")
        next = self.request.full_url()
        return "%s?next=%s" % (redirect_url, urllib.quote(next))

    @property
    def session(self):
        '''根据session_sid值来获取session对象，或者初始化一个session对象'''
        session_store = self.application.session_store
        sid = self.cookies.get('session_id')
        if session_store.__class__.__name__ == 'RedisSessionStore':
            if sid is None:
                _sessionsid = self.application.session_store.generate_sid()
            else:
                _sessionsid = sid.value
            from torweb.sessions import RedisSession
            return RedisSession(self.application.session_store, _sessionsid)

    def expire_session(self):
        from datetime import datetime, timedelta
        expires = datetime.utcnow() + timedelta(seconds=60 * 60)
        try:
            self.set_cookie('session_id', self.session.sid, expires=expires)
            self.session["timestamp"] = datetime.now()
            self.save_session()
        except AttributeError:
            pass
