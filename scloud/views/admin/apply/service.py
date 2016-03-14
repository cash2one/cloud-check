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


class GuideStepGetHandler(AuthHandler):
    def get_pro_info_res(self, pro_id):
        kw = {"pro_id": pro_id}
        svc = ProjectService(self, kw)
        pro_info_res = svc.get_project()
        if isinstance(pro_info_res, Exception):
            raise pro_info_res
        data = {
            "pro_info_res": pro_info_res,
            "STATUS_RESOURCE": STATUS_RESOURCE,
        }
        return data


@url("/apply/service/index", name="apply.service", active="apply.service")
class GuideHandler(GuideStepGetHandler):
    u'服务申请'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = ProjectService(self)
        pro_list_res = svc.get_project_list()
        if pro_list_res.return_code < 0:
            raise SystemError(pro_list_res.return_code, pro_list_res.return_message)
        logger.info(pro_list_res)
        return self.render_to_string("admin/apply/service/index.html", pro_list_res=pro_list_res, STATUS_RESOURCE=STATUS_RESOURCE)


#@url("/apply/pro_(?P<pro_id>\d+)/service/add", name="apply.service.add", active="apply.service.add")
@url("/apply/service/add", name="apply.service.add", active="apply.service.add")
class GuideHandler(GuideStepGetHandler):
    u'服务申请'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        svc = ProjectService(self)
        pro_id = self.args.get("pro_id")
        data = self.get_pro_info_res(pro_id)
        pro_list_res = svc.get_project_list()
        if pro_list_res.return_code < 0:
            raise SystemError(pro_list_res.return_code, pro_list_res.return_message)
        logger.info(pro_list_res)
        data.update({
            "pro_list_res": pro_list_res
        })
        return self.render_to_string("admin/apply/service/add.html", **data)
