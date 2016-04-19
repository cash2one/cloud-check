# -*- coding: utf-8 -*-

import scloud
#from torweb.urls import url
from scloud.shortcuts import url
from scloud.config import logger, thrownException
from scloud.const import pro_resource_apply_status_types, STATUS_RESOURCE
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
from scloud.async_services import svc_project
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from .base import ApplyHandler


@url("/apply/user/index", name="apply.user", active="apply.user")
class GuideHandler(ApplyHandler):
    u'权限申请'
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
    SUPPORTED_METHODS = AuthHandler.SUPPORTED_METHODS + ("CHECK", )
    u'事件详情'
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
        return self.render_to_string("admin/user/detail.html", **data)


#@url("/apply/pro_(?P<pro_id>\d+)/user/add", name="apply.user.add", active="apply.user.add")
@url("/apply/user/add", name="apply.user.add", active="apply.user.add")
class GuideHandler(ApplyHandler):
    u'权限申请'
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
        if pro_user_res.return_code == 0:
            self.add_message(u"用户信息%s成功！" % message, level="success", post_action=True)
            publish_notice_checker.delay(self.current_user.id)
        else:
            self.add_message(u"用户信息%s失败！(%s)(%s)" % (message, pro_user_res.return_code, pro_user_res.return_message), level="warning")
        pro_id = self.args.get("pro_id")
        data = self.get_pro_data(pro_id=pro_id)
        svc = ProUserService(self) 
        pro_users_res = svc.get_list() 
        data.update(pro_users_res=pro_users_res)
        data.update({"pro_user_res": pro_user_res})
        tmpl = self.render_to_string("admin/apply/user/add_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))


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
        pro_id = self.args.get("pro_id")
        data = self.get_pro_data(pro_id=pro_id)
        svc = ProUserService(self) 
        pro_users_res = svc.get_list() 
        data.update(pro_users_res=pro_users_res)
        data.update({"pro_user_res": del_res})
        tmpl = self.render_to_string("admin/apply/user/add_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
