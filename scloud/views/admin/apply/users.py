# -*- coding: utf-8 -*-

import scloud
#from torweb.urls import url
from scloud.shortcuts import url
from scloud.config import logger, thrownException
from scloud.const import pro_resource_apply_status_types, STATUS_RESOURCE, admin_emails
from scloud.handlers import Handler, AuthHandler
import requests
import urlparse
import urllib
import urllib2
import simplejson
import time
from tornado.web import asynchronous
from tornado import gen
from scloud.utils.permission import check_perms
from scloud.services.svc_project import ProjectService
from scloud.services.svc_apply_user import ProUserService 
from scloud.services.svc_pro_resource_apply import ProResourceApplyService
from scloud.async_services.publish_task import publish_notice_checker
from scloud.async_services.svc_mail import sendMail
from scloud.async_services import svc_project
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from .base import ApplyHandler


@url("/apply/user/index", name="apply.user", active="apply.user")
class GuideHandler(ApplyHandler):
    u'权限用户'

    @property
    def bread_list(self):
        if self.args.get("pro_id"):
            _bread_list = [
                {"urlspec": url.handlers_dict.get('guide'), "icon": "cubes"},
                {"urlspec": url.handlers_dict.get('apply.project.detail'), "url": "%s?pro_id=%s" % (self.reverse_url('apply.project.detail'), self.args.get("pro_id")), "icon": "cube"},
            ]
        else:
            _bread_list = []
        return _bread_list

    @check_perms('pro_info.view')
    @unblock
    def get(self):
        data = self.get_pro_data()
        svc = ProUserService(self, {"user_id": self.current_user.id})
        pro_users_res = svc.get_list()
        page = self.getPage(pro_users_res.data)
        data.update(page=page)
        return self.render_to_string("admin/apply/user/index.html", **data)


@url("/apply/user/detail", name="apply.user.detail", active="apply.user.index")
class ProUserDetailHandler(ApplyHandler):
    u'权限用户详情'
    SUPPORTED_METHODS = AuthHandler.SUPPORTED_METHODS + ("CHECK", )

    @property
    def bread_list(self):
        if self.args.get("pro_id"):
            _bread_list = [
                {"urlspec": url.handlers_dict.get('guide'), "icon": "cubes"},
                {"urlspec": url.handlers_dict.get('apply.project.detail'), "url": "%s?pro_id=%s" % (self.reverse_url('apply.project.detail'), self.args.get("pro_id")), "icon": "cube"},
                {"urlspec": url.handlers_dict.get('apply.user'), "url": self.session.get("from_url"), "icon": "users"},
            ]
        else:
            _bread_list = [
                {"urlspec": url.handlers_dict.get('apply.user'), "url": self.session.get("from_url"), "icon": "users"},
            ]
        return _bread_list

    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = ProUserService(self)
        pro_user_res = svc.get_info()
        if pro_user_res.return_code < 0:
            raise SystemError(pro_user_res.return_code, pro_user_res.return_message)
        logger.info(pro_user_res)
        data = {
            "pro_user_res": pro_user_res,
        }
        return self.render_to_string("admin/apply/user/detail.html", **data)


@url("/apply/user/add", name="apply.user.add", active="apply.user.add")
@url("/apply/user/edit", name="apply.user.edit", active="apply.user.edit")
class GuideHandler(ApplyHandler):
    u'权限申请'

    @property
    def bread_list(self):
        if self.args.get("pro_id"):
            _bread_list = [
                {"urlspec": url.handlers_dict.get('guide'), "icon": "cubes"},
                {"urlspec": url.handlers_dict.get('apply.project.detail'), "url": "%s?pro_id=%s" % (self.reverse_url('apply.project.detail'), self.args.get("pro_id")), "icon": "cube"},
                {"urlspec": url.handlers_dict.get('apply.user'), "url": self.session.get("from_url"), "icon": "users"},
            ]
        else:
            _bread_list = [
                {"urlspec": url.handlers_dict.get('apply.user'), "url": self.session.get("from_url"), "icon": "users"},
            ]
        return _bread_list

    @check_perms('pro_info.view')
    @unblock
    def get(self):
        # pro_id = self.args.get("pro_id")
        # user_id = self.args.get("user_id", 0)
        data = self.get_pro_data()
        svc = ProUserService(self)
        pro_users_res = svc.get_list()
        pro_user_res = svc.get_info()
        data.update(pro_users_res=pro_users_res, pro_user_res=pro_user_res)
        return self.render_to_string("admin/apply/user/add.html", **data)

    @check_perms('pro_info.view')
    @unblock
    def post(self):
        svc = ProUserService(self)
        pro_user_res = svc.do_pro_user()
        user_id = self.args.get("user_id")
        if user_id:
            message = u"修改"
        else:
            message = u"添加"
        data = {"pro_user_res": pro_user_res}
        if pro_user_res.return_code == 0:
            self.add_message(u"权限用户信息%s成功！" % message, level="success", post_action=True)
            tmpl = self.render_to_string("admin/guide/_step_3_user_detail.html", **data)
            publish_notice_checker.delay(self.current_user.id)
            mail_title = u"%s申请的权限用户信息%s成功！待受理" % (
                self.current_user.username or self.current_user.email,
                message
            )
            mail_html = self.render_to_string("admin/mail/pro_user.html", mail_title=mail_title, **data)
            sendMail.delay("scloud@infohold.com.cn", admin_emails, mail_title, mail_html)
        else:
            pro_data = self.get_pro_data()
            data.update(pro_data)
            self.add_message(u"权限用户信息%s失败！(%s)(%s)" % (message, pro_user_res.return_code, pro_user_res.return_message), level="warning")
            tmpl = self.render_to_string("admin/guide/_step_3_user.html", **data)

        messages_tmpl = self.render_to_string("admin/base/base_messages.html")
        return simplejson.dumps(self.success(data={"tmpl": tmpl, "messages_tmpl": messages_tmpl}))


@url("/apply/user/del", name="apply.user.del", active="apply.user.del")
class ApplyUserDelHandler(ApplyHandler):
    u'删除用户'
    @check_perms('pro_info.view')
    @unblock
    def post(self):
        user_id_list = self.get_arguments("user_id")
        svc = ProUserService(self, {"user_id_list": user_id_list})
        del_res = svc.do_del_pro_user()
        logger.info(del_res)
        if del_res.return_code == 0:
            self.add_message(u"用户信息删除成功！", level="success")
            publish_notice_checker.delay(self.current_user.id)
        else:
            self.add_message(u"用户信息删除失败！(%s)(%s)" % (del_res.return_code, del_res.return_message), level="warning")
        data = self.get_pro_data()
        svc = ProUserService(self, {"user_id": self.current_user.id})
        pro_users_res = svc.get_list()
        page = self.getPage(pro_users_res.data)
        data.update(page=page)
        tmpl = self.render_to_string("admin/apply/user/index_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
