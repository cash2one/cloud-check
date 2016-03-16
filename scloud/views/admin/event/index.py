# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # created: zhangpeng <zhangpeng1@infohold.com.cn>
# 
# import scloud
# from scloud.shortcuts import url
# from scloud.shortcuts import *
# from scloud.handlers import Handler
# import requests
# import urlparse
# import urllib
# import urllib2
# import time
# 
# 
# @url("/event/index", name="event.index", active="event.index")
# class GuideHandler(Handler):
#     u'事件管理'
#     def get(self):
#         data = {}
#         return self.render("admin/event/index.html", **data)
# 
# 
# @url("/event/add", name="event.add", active="event.add")
# class GuideHandler(Handler):
#     u'添加事件'
#     def get(self):
#         data = {}
#         return self.render("admin/event/add.html", **data)
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


@url("/event/index", name="event.index", active="event.index")
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
        data = {
            "pro_list_res": pro_list_res,
            "STATUS_RESOURCE": STATUS_RESOURCE
        }
        return self.render_to_string("admin/event/index.html", **data)


@url("/event/add", name="event.add", active="event.add")
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
        return self.render_to_string("admin/event/add.html", **data)
