# -*- coding: utf-8 -*-

import scloud
from scloud.shortcuts import url
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
from scloud.services.svc_pro_resource_apply import ProResourceCheckService
from scloud.services.svc_env import EnvService
from scloud.async_services import svc_project
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from scloud.views.admin.guide import GuideStepGetHandler
from scloud.const import STATUS_RESOURCE


@url("/pro/resource/(?P<res_id>\d+)/detail", name="resource_check_detail", active="resource_check_list")
class ResourceCheckListHandler(AuthHandler):
    u'待审核资源'
    @check_perms('pro_resource_apply.check')
    @unblock
    def get(self, **kwargs):
        # res_status = self.args.get()
        svc = ProResourceCheckService(self, kwargs)
        resource_apply = svc.get_resource()
        resource_res = svc.get_resources_by_status()
        if isinstance(resource_res, Exception):
            raise resource_res
        data = {
            "resource_apply": resource_apply.data,
            "resource_res": resource_res,
            "getattr": getattr,
            "STATUS_RESOURCE": STATUS_RESOURCE,
            "STATUS_RESOURCE_RANGE": [i for i in STATUS_RESOURCE.keys() if isinstance(i, int)]
        }
        return self.render_to_string("admin/check/check_detail.html", **data)


@url("/pro/resource/check_list", name="resource_check_list", active="resource_check_list")
class ResourceCheckListHandler(AuthHandler):
    u'待审核资源'
    @check_perms('pro_resource_apply.check')
    @unblock
    def get(self, **kwargs):
        kw = {}
        kw.update(self.args)
        kw.update(kwargs)
        # res_status = self.args.get()
        svc = ProResourceCheckService(self, kw)
        resource_res = svc.get_resources_by_status()
        if isinstance(resource_res, Exception):
            raise resource_res
        svc = EnvService(self)
        env_list_res = svc.get_list()
        page = self.getPage(resource_res.data.resource_list)
        data = {
            "page": page,
            "env_list_res": env_list_res,
            "resource_res": resource_res,
            "STATUS_RESOURCE_RANGE": [i for i in STATUS_RESOURCE.keys() if isinstance(i, int)]
        }
        logger.info("\t [page]: %s" % [i.user.email for i in page.object_list])
        return self.render_to_string("admin/check/check_list.html", **data)

    @check_perms('pro_resource_apply.check')
    @unblock
    def post(self):
        kw = {"checker_id": self.current_user.id}
        kw.update(self.args)
        svc = ProResourceCheckService(self, kw)
        resource_action_res = svc.do_resource_action()
        if resource_action_res.return_code == 0:
            messages = resource_action_res.data
            for message, level in messages:
                self.add_message(message, level, post_action=True)
        else:
            self.add_message("资源审核失败:(%s)%s" % (resource_action_res.return_code, resource_action_res.return_message))
        resource_res = svc.get_resources_by_status()
        svc = EnvService(self)
        env_list_res = svc.get_list()
        page = self.getPage(resource_res.data.resource_list)
        data = {
            "page": page,
            "env_list_res": env_list_res,
            "resource_res": resource_res,
            "STATUS_RESOURCE_RANGE": [i for i in STATUS_RESOURCE.keys() if isinstance(i, int)]
        }
        tmpl = self.render_to_string("admin/check/check_list_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
