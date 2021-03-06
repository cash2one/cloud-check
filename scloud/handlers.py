#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>

import re
import time
import urllib
import urlparse
import functools
import simplejson
from tornado.web import HTTPError
from tornado import gen
from tornado.util import ObjectDict
from torweb.handlers import BaseHandler
from torweb.paginator import Paginator, InvalidPage
from scloud.shortcuts import env
from scloud.config import CONF, logger
from scloud.models.base import DataBaseService
from scloud.async_services.svc_act import task_post_action
# from sqlalchemy.exc import SQLAlchemyError
from scloud.utils.error_code import ERR
# from scloud.utils.error import SystemError
from scloud.const import (STATUS_RESOURCE, RESOURCE_BANDWIDTH,
    STATUS_PRO_TABLES, STATUS_PRIORITY, STATUS_YESNO,
    PLOT_LOADBALANCE, LOADBALANCE_HEALTH, PRO_USER_TYPES,
    env_colors)
from scloud.utils.permission import GROUP, OP
# from sqlalchemy.orm.session import SessionTransaction
from scloud.views.handlers_mixin import HandlersMixin


class HandlerMeta(type):
    """
     asynchronous handler meta class
    """
    __ASYNC_HANDLER = ('post', 'get', 'delete', 'put')  # 必须加逗号

    def __new__(mcs, name, bases, dct):
        for method in mcs.__ASYNC_HANDLER:
            if method in dct:
                # 检查url地址中的不合法参数，防跨域调用js
                # 检查函数运行时错误，遇到错误直接抛出
                # dct[method] = check_xget(dct[method])
                pass
        return type.__new__(mcs, name, bases, dct)


class Handler(BaseHandler, HandlersMixin):
    __metaclass__ = HandlerMeta

    def __str__(self):
        return self.__doc__ or self.__class__.__name__

    def initialize(self, **kwargs):
        super(Handler, self).initialize(**kwargs)
        self.svc = DataBaseService()
        self.svc.__enter__()
        self.db = self.svc.db
        logger.warning("<" + "=" * 25 + " [initialize] " + "=" * 25 + ">")
        self.handler_return_url()

    def init_messages(self):
        if "messages" not in self.session:
            self.session["messages"] = []
        self.messages = self.session.get("messages", [])
        self.save_session()

    def add_message(self, content, level="info", post_action=False, url=""):
        if post_action:
            self.post_action(content=content, level=level)
        self.session["messages"].append({"level": level, "content": content, "url": url})
        self.session["messages_request"] = len(self.session["messages"])
        self.save_session()
        # logger.info(self.session)

    def post_action(self, content="", level="info"):
        current_user = self.session.get("current_user")
        if current_user:
            user_id = current_user.id
        else:
            user_id = 0
        task_post_action.delay(act_type=1, content=content, user_id=user_id)

    def get_messages(self):
        self.messages = self.session["messages"]
        logger.info(self.messages)
        self.session["messages"] = []
        self.save_session()
        return self.messages

    def on_finish(self):
        # logger.info("\t" + "====[EXIT]====")
        # self.svc.__exit__(None, None, None)
        # try:
        #     # transaction = session_dict.get("transaction")
        #     # logger.error("transaction: %s" % transaction)
        #     #if transaction:
        #     # dispatch = session_dict.get("dispatch")
        #     self.db.commit()
        #     # self.db.flush()
        #     logger.info("\t" + "====[COMMIT]====")
        # except Exception:
        #     logThrown()
        #     self.db.rollback()
        #     logger.info("\t" + "====[ROLLBACK]====")
        # self.db.remove()
        self.db.close()
        logger.info("\t" + "====[CLOSE]====")
        # logger.info(self.db.is_active)
        # logger.info("====================== [http method (%s)] ======================" % self.request.method)
        # self.db.is_active
        # self.db.remove()
        # self.db.close()
        # logger.info(self.db)
        # logger.info(self.db.is_active)
        logger.critical("<" + "="*25 + " [finish] " + "="*25 + ">")

    def prepare(self):
        logger.warning("<" + "="*25 + " [prepare] " + "="*25 + ">")
        # self.svc._db_init()
        # self.svc.db.begin_nested()
        # self.svc.db.begin()
        # self.db = self.svc.db
        logger.info("\t" + "====================== [http method] ======================")
        logger.info("\t" + self.request.method)
        logger.info("\t" + "====================== [args] ======================")
        logger.info("\t %s" % self.args)
        self.init_messages()
        self.pjax = self.request.headers.get("X-PJAX")
        headers = self.request.headers
        x_requested_with = headers.get("X-Requested-With", "")
        self.ajax = x_requested_with == "XMLHttpRequest"
        if self.pjax:
            self.ajax = False

    def success(self, data):
        return self.failure(data=data)

    def failure(self, return_code=0, return_message="", data=None):
        result = ObjectDict()
        result.return_code = return_code
        result.return_message = return_message
        result.data = data
        return result

    def render_to_string(self, template, **kwargs):
        logger.info("\t [messages]:%s" % self.session["messages"])
        if self.pjax:
            title = self.__doc__ or self.__class__.__name__
            title = title.encode("utf-8")
            self.set_header("title", urllib.quote(title))
            self.set_header("active", self.kwargs.get("active", ""))
            template = "%s_pjax.html" % template.split(".html")[0]
        tmpl = env.get_template(template)
        s = "&".join(
            ["%s=%s" % (k, v) for k, v in self.args.items() \
            if k not in ["page", "_pjax", "_xsrf"]]
        )
        logger.info(s)
        kwargs.update({
            "CONF": CONF,
            "getattr": getattr,
            "dir": dir,
            "rand_time": time.time(),
            "handler": self,
            "request": self.request,
            "reverse_url": self.application.reverse_url,
            "ERR": ERR,
            "env_colors": env_colors,
            "STATUS_RESOURCE": STATUS_RESOURCE,
            "RESOURCE_BANDWIDTH": RESOURCE_BANDWIDTH,
            "STATUS_PRO_TABLES": STATUS_PRO_TABLES,
            "STATUS_PRIORITY": STATUS_PRIORITY,
            "STATUS_YESNO": STATUS_YESNO,
            "PRO_USER_TYPES": PRO_USER_TYPES,
            "PLOT_LOADBALANCE": PLOT_LOADBALANCE,
            "LOADBALANCE_HEALTH": LOADBALANCE_HEALTH,
            "GROUP": GROUP,
            "OP": OP,
            "s": s + "&" if s else ""
        })
        # logger.info("\t [render_to_string kwargs]: %s" % kwargs)
        template_string = tmpl.render(**kwargs)
        return template_string

    def render(self, template, **kwargs):
        template_string = self.render_to_string(template, **kwargs)
        self.write(template_string.strip())

    def getPage(self, objects, numsPerpage=8, total_count=0, page_name='page'):
        try:
            page_num = int(self.args.get(page_name, '1'))
        except ValueError:
            page_num = 1
        logger.info("[page_name]: %s" % page_name)
        logger.info("[page_name %s]: [page_num]: %s" % (page_name, self.args.get(page_name, '1')))
        logger.info("[page_num]: %s" % page_num)
        try:
            _total_count = total_count or objects.count()
        except Exception as e:
            _total_count = total_count or len(objects)
        paginator = Paginator(objects, numsPerpage, total_count=_total_count)
        try:
            page = paginator.page(page_num)
        except InvalidPage:
            raise HTTPError(404)
        if not page: raise HTTPError(404)
        return page

    # # @gen.coroutine
    def get_error_html(self, status_code, **kwargs):
        return ""
    #     logger.info(kwargs)
    #     exception = kwargs["exception"]
    #     traceback = kwargs["traceback"]
    #     self.render("admin/error/500.html", status_code=status_code, exception=exception, traceback=traceback)


def authenticated(method):
    """Decorate methods with this to require that the user be logged in."""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            logger.info("[authenticated]: %s" % self.current_user)
            if self.request.method in ("GET", "HEAD", "POST", "CHECK", "XGET"):
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
    __ASYNC_HANDLER = ('post', 'get', 'head', 'check', 'xget')  # 必须加逗号

    def __new__(mcs, name, bases, dct):
        HandlerMeta.__new__(mcs, name, bases, dct)
        for method in mcs.__ASYNC_HANDLER:
            if method in dct:
                dct[method] = authenticated(dct[method])
        return type.__new__(mcs, name, bases, dct)


class AuthHandler(Handler):
    __metaclass__ = AuthHandlerMeta
    SUPPORTED_METHODS = Handler.SUPPORTED_METHODS + ("CHECK", "XGET")

    # def __init__(self, application, request, **kwargs):
    # super(AuthHandler, self).__init__(application, request, **kwargs)
    # self.current_perms = None

    def prepare(self):
        self.expire_session()
        super(AuthHandler, self).prepare()
        if self.current_user and self.request.method == "GET" and not self.ajax:
            if not self.current_user.username:
                logger.error(u"\t 您还没有设置用户名，请设置用户名")
                self.add_message(u"您还没有设置用户名，请设置用户名", level="warning", url=self.reverse_url('user_profile'))
            if not self.current_user.email:
                self.add_message(u"您还没有设置邮箱，请设置邮箱", level="warning", url=self.reverse_url('user_profile'))

    def get_current_user(self):
        current_user = self.session.get("current_user", None)
        # logger.info("******[GET SESSION] %s" % current_user)
        if current_user:
            logger.info("\t [current_user]: %s(%s)-perms:(%s)" % (current_user.id, current_user.username, current_user.get_current_perms()))
        else:
            logger.info("\t [current_user]: None")
        return current_user

    def get_login_url(self, next=''):
        redirect_url = self.reverse_url("login")
        if not next:
            next = self.request.full_url()
        return "%s?next=%s" % (redirect_url, urllib.quote(next))

    # @property
    # def session(self):
    #     '''根据session_sid值来获取session对象，或者初始化一个session对象'''
    #     session_store = self.application.session_store
    #     sid = self.cookies.get('session_id')
    #     if session_store.__class__.__name__ == 'RedisSessionStore':
    #         if sid is None:
    #             _sessionsid = self.application.session_store.generate_sid()
    #         else:
    #             _sessionsid = sid.value
    #         from torweb.sessions import RedisSession
    #         return RedisSession(self.application.session_store, _sessionsid)

    def expire_session(self):
        from datetime import datetime, timedelta
        expires = datetime.utcnow() + timedelta(seconds=60 * 60)
        try:
            self.set_cookie('session_id', self.session.sid, expires=expires)
            self.session["timestamp"] = datetime.now()
            self.save_session()
        except AttributeError:
            pass
