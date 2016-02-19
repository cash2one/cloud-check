# -*- coding: utf-8 -*-

import scloud
from torweb.urls import url
from scloud.config import logger
from scloud.const import pro_resource_apply_status_types
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


@url("/resource/(?P<res_id>\d+)", name="resource_view", active="guide")
class ProResourceHandler(AuthHandler):
    u'资源申请/变更 步骤1'
    @check_perms('pro_resource_apply.view')
    @unblock
    def get(self, **kwargs):
        kw = {}
        kw.update(self.args)
        kw.update(kwargs)
        svc = ProResourceApplyService(self.svc.db, kw)
        resource_res = svc.get_resource()
        if isinstance(resource_res, Exception):
            raise pro_info_res
        data = {
            "resource_res": resource_res,
        }
        return self.render_to_string("admin/pro_resource/index.html", **data)


@url("/resource/(?P<res_id>\d+)/revoke", name="resource_revoke", active="guide")
class ProResourceRevokeHandler(AuthHandler):
    u"""撤销资源申请"""
    def post(self, **kwargs):
        kw = {"user_id": self.current_user.id}
        kw.update(self.args)
        kw.update(kwargs)
        svc = ProResourceApplyService(self.svc.db, kw, handler=self)
        revoke_res = svc.do_revoke()
        kw.update({"pro_id": revoke_res.data.pro_id if revoke_res.return_code == 0 else 0})
        pro_svc = ProjectService(self.svc.db, kw, handler=self)
        pro_info_res = pro_svc.get_project()
        data = {
            "pro_info_res": pro_info_res,
            "post_apply_res": revoke_res
        }
        if revoke_res.return_code == 0:
            self.add_message(u"资源申请已撤销！", level="success")
            return self.render("admin/guide/step2.html", **data)
        else:
            self.add_message(u"资源申请撤销失败！(%s)%s" % (post_apply_res.return_code, post_apply_res.return_message), level="warning")
            return self.render("admin/guide/step1.html", **data)
