# -*- coding: utf-8 -*-

from torweb.urls import url
from scloud.config import logger, thrownException
from scloud.handlers import Handler, AuthHandler
from tornado.web import asynchronous
from tornado import gen
from scloud.services.svc_login import LoginService
from scloud.utils.unblock import unblock


@url("/login", name="login", active="login")
class LoginHandler(Handler):
    u'登录'
    @asynchronous
    @gen.coroutine
    def get(self):
        raise gen.Return(self.render("admin/login.html"))

    @unblock
    def post(self):
        next = self.args.get("next", self.reverse_url('guide'))
        svc = LoginService(self.svc.db, self.args)
        result = svc.do_login()
        logger.info("++++++++++++++++++++ result ++++++++++++++++++++++++")
        logger.info(result)
        if result.return_code == 0:
            self.session["current_user"] = result.data
            logger.info("login success!")
            self.save_session()
            logger.info("login session saved!")
            self.add_message(u"欢迎%s,您已登录成功！" % result.data.username)
            if next:
                return self.redirect(next)
            else:
                return self.redirect(self.reverse_url('guide'))
        else:
            self.session["post_username"] = self.args.get("username", u"")
            self.save_session()
            return self.render_to_string("admin/login.html", result=result)
            # return self.redirect(self.reverse_url('login'))


@url("/logout", name="logout")
class LogoutHandler(AuthHandler):
    def get(self):
        return self.post()

    def post(self):
        next = self.request.headers.get("referer")
        self.cookies.clear()
        self.session.clear()
        self.save_session()
        return self.redirect(self.get_login_url(next))
