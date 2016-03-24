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
from scloud.services.svc_pro_resource_apply import ProResourceApplyService
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
        return self.render_to_string("admin/apply/user/index.html", **data)


#@url("/apply/pro_(?P<pro_id>\d+)/user/add", name="apply.user.add", active="apply.user.add")
@url("/apply/user/add", name="apply.user.add", active="apply.user.add")
class GuideHandler(ApplyHandler):
    u'权限申请'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        pro_id = self.args.get("pro_id")
        data = self.get_pro_data(pro_id=pro_id)
        return self.render_to_string("admin/apply/user/add.html", **data)

    @check_perms('pro_info.view')
    @unblock
    def post(self):
        # svc = ApplyService(self)
        # pro_user_res = svc.do_pro_user()
        # if pro_user_res.return_code == 0:
            # self.add_message(u"用户信息添加成功！", level="success")
        # else:
            # self.add_message(u"用户信息添加失败！(%s)(%s)" % (pro_user_res,return_code, pro_user_res.return_message), level="warning")
        pro_id = self.args.get("pro_id")
        data = self.get_pro_data(pro_id=pro_id)
        # data.update({"pro_user_res": pro_user_res})
        tmpl = self.render_to_string("admin/apply/user/add_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
