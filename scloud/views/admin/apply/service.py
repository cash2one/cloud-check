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
from scloud.services.svc_apply_service import ApplyService
from scloud.services.svc_pro_resource_apply import ProResourceApplyService
from scloud.async_services import svc_project
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from .base import ApplyHandler


@url("/apply/service/index", name="apply.service", active="apply.service")
class GuideHandler(ApplyHandler):
    u'服务申请'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        data = self.get_pro_data()
        return self.render_to_string("admin/apply/service/index.html", **data)


#@url("/apply/pro_(?P<pro_id>\d+)/service/add", name="apply.service.add", active="apply.service.add")
@url("/apply/service/add", name="apply.service.add", active="apply.service.add")
class GuideHandler(ApplyHandler):
    u'服务申请'
    @check_perms('pro_info.view')
    @unblock
    def get(self):
        pro_id = self.args.get("pro_id")
        data = self.get_pro_data(pro_id=pro_id)
        return self.render_to_string("admin/apply/service/add.html", **data)


@url("/apply/service/publish/add", name="apply.service.publish.add", active="apply.service.add")
class GuideHandler(ApplyHandler):
    u'服务申请'
    @check_perms('pro_info.view')
    @unblock
    def post(self):
        svc = ApplyService(self)
        publish_res = svc.do_publish()
        if publish_res.return_code == 0:
            self.add_message(u"互联网发布信息添加成功！", level="success")
        else:
            self.add_message(u"互联网发布信息添加失败！(%s)(%s)" % (publish_res.return_code, publish_res.return_message), level="warning")
        pro_id = self.args.get("pro_id")
        data = self.get_pro_data(pro_id=pro_id)
        data.update({"publish_res": publish_res})
        tmpl = self.render_to_string("admin/apply/service/add_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
