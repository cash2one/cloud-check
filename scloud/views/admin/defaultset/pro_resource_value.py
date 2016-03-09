# -*- coding: utf-8 -*-

import scloud
from torweb.urls import url
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
from scloud.services.svc_env import EnvService
from scloud.services.svc_env_resource_value import EnvResourceValueService
from scloud.services.svc_act import ActHistoryService
from scloud.utils.unblock import unblock
from scloud.utils.error import SystemError
from scloud.views.admin.defaultset.env_info import BaseEnvHandler
from scloud.models.environment import Env_Resource_Value


@url("/defaultset/env_resource_value", name="defaultset.env_resource_value", active="defaultset.env_resource_value")
class Env_resource_value_Handler(BaseEnvHandler):
    u"""资源申请费用设置"""
    @unblock
    def get(self):
        data = self.get_index_page()
        return self.render_to_string("admin/defaultset/env_resource_value/index.html", **data)


@url("/defaultset/env_resource_value/(?P<env_id>\d+)/edit", name="defaultset.env_resource_value.edit", active="defaultset.env_resource_value")
class Add_Env_resource_value_Handler(BaseEnvHandler):
    u"""编辑资源申请费用"""
    @unblock
    def get(self, **kwargs):
        svc = EnvService(self, kwargs)
        env_res = svc.get_env()
        data = self.get_index_page()
        data.update({
            "env_res": env_res,
            "resource_value": env_res.data.env_resource_value,
            "Env_Resource_Value": Env_Resource_Value
        })
        return self.render_to_string("admin/defaultset/env_resource_value/edit.html", **data)

    @unblock
    def post(self, **kwargs):
        svc = EnvService(self, kwargs)
        env_res = svc.get_env()
        svc = EnvResourceValueService(self, kwargs)
        env_resource_value_res = svc.get_or_create()
        data = self.get_index_page()
        data.update({
            "env_res": env_res,
            "resource_value": env_resource_value_res.data,
            "Env_Resource_Value": Env_Resource_Value
        })
        if env_res.return_code == 0:
            self.add_message(u"环境[%s]对应默认值修改成功！" % env_res.data.name, level="success", post_action=True)
        tmpl = self.render_to_string("admin/defaultset/env_resource_value/edit_pjax.html", **data)
        return simplejson.dumps(self.success(data=tmpl))
