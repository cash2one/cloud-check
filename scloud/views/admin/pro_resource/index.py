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
from scloud.views.admin.guide import GuideStepGetHandler


@url("/resource/(?P<res_id>\d+)", name="resource_view", active="guide")
class ProResourceHandler(AuthHandler):
    u'资源申请/变更 步骤1'
    @check_perms('pro_resource_apply.view')
    @unblock
    def get(self, **kwargs):
        kw = {}
        kw.update(self.args)
        kw.update(kwargs)
        svc = ProResourceApplyService(self, kw)
        resource_res = svc.get_resource()
        if isinstance(resource_res, Exception):
            raise resource_res
        data = {
            "resource_res": resource_res,
        }
        return self.render_to_string("admin/pro_resource/index.html", **data)


