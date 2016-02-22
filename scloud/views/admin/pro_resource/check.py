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
from scloud.const import STATUS_RESOURCE


@url("/pro/resource/check_list", name="resource_check_list", active="resource_check_list")
class ResourceCheckListHandler(AuthHandler):
    u'待审核资源'
    @check_perms('pro_resource_apply.check')
    @unblock
    def get(self, **kwargs):
        kw = {}
        kw.update(self.args)
        kw.update(kwargs)
        svc = ProResourceApplyService(self.svc.db, kw)
        resource_res = svc.get_resources_by_status()
        if isinstance(resource_res, Exception):
            raise resource_res
        page = self.getPage(resource_res.data.resource_list, 3)
        data = {
            "page": page,
            "resource_res": resource_res,
            "STATUS_RESOURCE": STATUS_RESOURCE,
            "STATUS_RESOURCE_RANGE": [i for i in STATUS_RESOURCE.keys() if str(i).isdigit()]
        }
        return self.render_to_string("admin/pro_resource/check_list.html", **data)
