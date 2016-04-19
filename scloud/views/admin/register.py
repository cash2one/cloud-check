# -*- coding: utf-8 -*-

import simplejson
from scloud.shortcuts import url
from scloud.config import logger, thrownException
from scloud.handlers import Handler
# from tornado.web import asynchronous
# from tornado import gen
from scloud.services.svc_register import RegisterService
from scloud.utils.unblock import unblock


@url("/register", name="register", active="register")
class RegisterHandler(Handler):
    u'注册'
    @unblock
    def get(self):
        return self.render_to_string("admin/register.html")

    @unblock
    def post(self):
        next = self.args.get("next", self.reverse_url('user_profile'))
        svc = RegisterService(self)
        result = svc.do_register()
        logger.info("++++++++++++++++++++ result ++++++++++++++++++++++++")
        logger.info(result)
        if result.return_code == 0:
            self.session["current_user"] = result.data
            logger.info("login success!")
            self.save_session()
            logger.info("login session saved!")
            self.add_message(u"欢迎%s,您已注册成功！" % result.data.username)
            if next:
                return simplejson.dumps(self.success(data=next))
            else:
                return simplejson.dumps(self.success(data=self.reverse_url('pt_user')))
        else:
            # self.session["post_email"] = self.args.get("email", u"")
            # self.session["post_mobile"] = self.args.get("mobile", u"")
            # self.session["post_agree"] = self.args.get("agree", 0)
            # self.save_session()
            tmpl = self.render_to_string("admin/register_pjax.html", result=result)
            result["data"] = tmpl
            return simplejson.dumps(result)
            # return self.redirect(self.reverse_url('login'))
